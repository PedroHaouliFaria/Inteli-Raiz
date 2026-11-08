import { useCallback, useEffect, useRef, useState } from 'react';
import {
  Button,
  InlineLoading,
  InlineNotification,
  Tag,
  TextArea,
} from '@carbon/react';
import { Close, Report, Search, Send, WatsonxAi } from '@carbon/icons-react';
import { ApiError, getCopilotStatus, postCopilotMessage } from '../../api/client.js';

const MAX_CHARS = 1000;
const TOOL_LABELS = {
  listar_compras: 'Pesquisou suas compras',
  consultar_compra: 'Consultou uma transação',
  gerar_relatorio: 'Gerou um resumo',
  solicitar_revisao: 'Solicitou revisão humana',
};

function nowId(prefix) {
  return `${prefix}-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function inlineMarkdown(text) {
  return text.split(/(\*\*[^*]+\*\*)/g).filter(Boolean).map((part, index) => (
    part.startsWith('**') && part.endsWith('**')
      ? <strong key={`${part}-${index}`}>{part.slice(2, -2)}</strong>
      : part
  ));
}

function MarkdownText({ content }) {
  const blocks = [];
  let bullets = [];
  const flushBullets = () => {
    if (bullets.length === 0) return;
    blocks.push(
      <ul key={`list-${blocks.length}`}>
        {bullets.map((line, index) => <li key={`${line}-${index}`}>{inlineMarkdown(line)}</li>)}
      </ul>,
    );
    bullets = [];
  };

  content.split('\n').forEach((rawLine) => {
    const line = rawLine.trim();
    if (line.startsWith('- ')) {
      bullets.push(line.slice(2));
      return;
    }
    flushBullets();
    if (line) {
      blocks.push(<p key={`paragraph-${blocks.length}`}>{inlineMarkdown(line)}</p>);
    }
  });
  flushBullets();
  return <div className="associate-copilot__content">{blocks}</div>;
}

function Message({ message }) {
  const isUser = message.role === 'user';
  return (
    <article className={`associate-copilot__message associate-copilot__message--${isUser ? 'user' : 'assistant'}`}>
      <span className="cds--type-label-01">{isUser ? 'Você' : 'Copiloto Raiz'}</span>
      <MarkdownText content={message.content} />
      {!isUser && message.tools?.length > 0 && (
        <div className="associate-copilot__tool-events" aria-label="Ferramentas utilizadas">
          {message.tools.map((tool) => (
            <Tag key={tool} size="sm" type={tool === 'solicitar_revisao' ? 'purple' : 'cool-gray'}>
              {TOOL_LABELS[tool] ?? 'Consultou contexto'}
            </Tag>
          ))}
        </div>
      )}
    </article>
  );
}

export default function AssociateCopilot({ selectedCaseId, onClose, onAction }) {
  const [messages, setMessages] = useState([]);
  const [capabilities, setCapabilities] = useState([]);
  const [available, setAvailable] = useState(true);
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState(null);
  const [input, setInput] = useState('');
  const logRef = useRef(null);

  useEffect(() => {
    let active = true;
    getCopilotStatus()
      .then((data) => {
        if (!active) return;
        setCapabilities(data.capabilities ?? []);
        setAvailable(data.agent_available ?? true);
        setMessages([{
          id: 'greeting',
          role: 'assistant',
          content: data.greeting,
          tools: [],
        }]);
      })
      .catch((err) => {
        if (!active) return;
        setError(err instanceof ApiError ? err.message : 'Não foi possível iniciar o copiloto.');
      })
      .finally(() => active && setLoading(false));
    return () => { active = false; };
  }, []);

  useEffect(() => {
    const element = logRef.current;
    if (element) element.scrollTop = element.scrollHeight;
  }, [messages, sending]);

  const send = useCallback(async (rawMessage) => {
    const text = rawMessage.trim();
    if (!text || sending || text.length > MAX_CHARS) return;
    setSending(true);
    setError(null);
    setInput('');
    setMessages((current) => [...current, {
      id: nowId('user'), role: 'user', content: text, tools: [],
    }]);
    try {
      const data = await postCopilotMessage(text);
      setMessages((current) => [...current, {
        id: nowId('assistant'),
        role: 'assistant',
        content: data.content,
        tools: data.tools_used ?? [],
      }]);
      if (data.action_taken) onAction?.();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Erro de rede ao falar com o copiloto.');
    } finally {
      setSending(false);
    }
  }, [onAction, sending]);

  const quickActions = [
    { label: 'O que precisa de atenção?', prompt: 'Quais das minhas compras precisam de atenção agora?', icon: Search },
    { label: 'Gerar resumo', prompt: 'Gere um relatório resumido das minhas compras e revisões.', icon: Report },
    ...(selectedCaseId ? [{
      label: `Explicar ${selectedCaseId}`,
      prompt: `Explique a compra ${selectedCaseId}, o status atual e o que eu posso fazer.`,
      icon: Search,
    }] : []),
  ];

  return (
    <aside className="associate-copilot" aria-label="Copiloto do associado">
      <header className="associate-copilot__header">
        <div className="associate-copilot__identity">
          <span className="associate-copilot__icon"><WatsonxAi size={22} aria-hidden /></span>
          <div>
            <h2 className="cds--type-heading-compact-02">Copiloto Raiz</h2>
            <p className="cds--type-label-01">Apoio para todas as suas compras</p>
          </div>
        </div>
        <Button hasIconOnly kind="ghost" size="sm" renderIcon={Close} iconDescription="Fechar copiloto" onClick={onClose} />
      </header>

      <div className="associate-copilot__status">
        <Tag size="sm" type={available ? 'green' : 'gray'}>{available ? 'Disponível' : 'Offline'}</Tag>
        <span className="cds--type-helper-text-01">Conversa temporária desta sessão</span>
      </div>

      <div className="associate-copilot__quick-actions" aria-label="Atalhos do copiloto">
        {quickActions.map(({ label, prompt, icon }) => (
          <Button key={label} kind="tertiary" size="sm" renderIcon={icon} disabled={!available || sending} onClick={() => send(prompt)}>
            {label}
          </Button>
        ))}
      </div>

      <div ref={logRef} className="associate-copilot__messages" role="log" aria-live="polite">
        {loading && <InlineLoading description="Iniciando copiloto…" status="active" />}
        {messages.map((message) => <Message key={message.id} message={message} />)}
        {sending && <InlineLoading description="Copiloto executando ferramentas…" status="active" />}
      </div>

      {error && (
        <InlineNotification kind="warning" title="Copiloto" subtitle={error} hideCloseButton lowContrast />
      )}

      {!loading && capabilities.length > 0 && messages.length <= 1 && (
        <p className="cds--type-helper-text-01 associate-copilot__capabilities">
          Posso: {capabilities.join(' · ')}
        </p>
      )}

      <div className="associate-copilot__composer">
        <TextArea
          id="associate-copilot-input"
          labelText="Mensagem para o copiloto"
          hideLabel
          placeholder="Ex.: pesquise minhas compras em revisão"
          rows={3}
          value={input}
          maxCount={MAX_CHARS}
          enableCounter
          disabled={!available || sending || loading}
          onChange={(event) => setInput(event.target.value)}
          onKeyDown={(event) => {
            if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
              event.preventDefault();
              send(input);
            }
          }}
        />
        <Button size="sm" renderIcon={Send} disabled={!available || sending || !input.trim()} onClick={() => send(input)}>
          Enviar
        </Button>
      </div>
    </aside>
  );
}
