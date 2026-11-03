/**
 * PurchaseChat — chat com o agente para uma compra específica.
 *
 * Responsabilidades:
 *   - Carrega histórico ao abrir via GET /api/purchases/{case_id}/chat
 *   - Renderiza mensagens user/assistant de forma acessível
 *   - Mostra tools_used de forma discreta (sem dados internos sensíveis)
 *   - Envia mensagem com loading e impede duplicação
 *   - Respeita máximo de 1000 caracteres
 *   - Se agent_available=false, informa sem afetar botões de confirmação
 *   - Em 503 AGENT_UNAVAILABLE, mostra mensagem e refaz GET (backend já salvou user_message)
 *   - Em 429, mostra mensagem com retry_after_seconds se disponível
 *   - Não inventa resposta local/fallback
 *
 * NÃO expõe score, customer_id, card_id completo nem outros campos internos.
 */
import { useCallback, useEffect, useRef, useState } from 'react';
import {
  Button,
  InlineLoading,
  InlineNotification,
  Stack,
  TextArea,
  Tile,
} from '@carbon/react';
import { Chat, Send } from '@carbon/icons-react';
import { ApiError, getChatHistory, postChatMessage } from '../../api/client.js';
import { formatDate } from './utils.js';

const MAX_CHARS = 1000;

// Mapeamento de nomes de ferramenta para rótulos amigáveis (sem dados internos).
const TOOL_LABELS = {
  consultar_compra: 'consultou dados da compra',
  consultar_status: 'consultou status',
  avaliar_transacao: 'consultou avaliação',
  solicitar_revisao: 'solicitou revisão',
};

function toolLabel(name) {
  return TOOL_LABELS[name] ?? 'consultou contexto';
}

// ── Balão de mensagem ──────────────────────────────────────────────────────────

function MessageBubble({ message }) {
  const isUser = message.role === 'user';
  const tools = message.tools_used ?? [];

  return (
    <div
      className={`purchase-chat__bubble purchase-chat__bubble--${isUser ? 'user' : 'assistant'}`}
      aria-label={isUser ? 'Sua mensagem' : 'Resposta do assistente'}
    >
      <div className="purchase-chat__bubble-header">
        <span className="cds--type-label-01 purchase-chat__bubble-role">
          {isUser ? 'Você' : 'Assistente'}
        </span>
        <span className="cds--type-helper-text-01 purchase-chat__bubble-time">
          {formatDate(message.created_at)}
        </span>
      </div>
      <p className="cds--type-body-01 purchase-chat__bubble-text">{message.content}</p>
      {!isUser && tools.length > 0 && (
        <p
          className="cds--type-helper-text-01 purchase-chat__tools"
          aria-label={`Fontes usadas: ${tools.map(toolLabel).join(', ')}`}
        >
          Fontes: {tools.map(toolLabel).join(', ')}
        </p>
      )}
    </div>
  );
}

// ── Componente principal ───────────────────────────────────────────────────────

export default function PurchaseChat({ caseId, onReviewProtocol }) {
  const [messages, setMessages] = useState(null);      // null = ainda carregando
  const [agentAvailable, setAgentAvailable] = useState(true);
  const [historyLoading, setHistoryLoading] = useState(true);
  const [historyError, setHistoryError] = useState(null);

  const [inputText, setInputText] = useState('');
  const [sending, setSending] = useState(false);
  const [sendError, setSendError] = useState(null);

  const bottomRef = useRef(null);

  // Carrega (ou recarrega) o histórico
  const loadHistory = useCallback(async () => {
    setHistoryError(null);
    try {
      const data = await getChatHistory(caseId);
      setMessages(data.messages ?? []);
      setAgentAvailable(data.agent_available ?? true);
    } catch (err) {
      setHistoryError(err instanceof ApiError ? err.message : 'Erro de rede ao carregar o histórico.');
    } finally {
      setHistoryLoading(false);
    }
  }, [caseId]);

  // Carrega ao montar
  useEffect(() => {
    setMessages(null);
    setHistoryLoading(true);
    setHistoryError(null);
    setSendError(null);
    setInputText('');
    loadHistory();
  }, [caseId, loadHistory]);

  // Rola para o fim quando chegam mensagens novas
  useEffect(() => {
    if (messages && messages.length > 0) {
      bottomRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
    }
  }, [messages]);

  const handleSend = async () => {
    const text = inputText.trim();
    if (!text || sending) return;
    if (text.length > MAX_CHARS) return;

    setSending(true);
    setSendError(null);

    try {
      const data = await postChatMessage(caseId, text);
      setInputText('');

      // Atualiza mensagens com a resposta do servidor
      setMessages((prev) => [
        ...(prev ?? []),
        data.user_message,
        data.reply,
      ]);

      // Se o agente abriu uma revisão, notifica o pai
      if (data.review_protocol) {
        onReviewProtocol?.(data.review_protocol);
      }
    } catch (err) {
      if (err instanceof ApiError) {
        if (err.code === 'AGENT_UNAVAILABLE') {
          // Backend já salvou a mensagem do usuário antes do 503: recarrega histórico
          setSendError(err.message);
          await loadHistory();
        } else if (err.code === 'RATE_LIMITED') {
          const retry = err.details?.retry_after_seconds;
          setSendError(
            retry
              ? `${err.message} Tente novamente em ${retry} segundos.`
              : err.message,
          );
        } else {
          setSendError(err.message);
        }
      } else {
        setSendError('Erro de rede. Tente novamente.');
      }
    } finally {
      setSending(false);
    }
  };

  const handleKeyDown = (e) => {
    // Ctrl+Enter ou Cmd+Enter envia; Enter sozinho insere nova linha (padrão do textarea)
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      handleSend();
    }
  };

  // ── Render ────────────────────────────────────────────────────────────────

  return (
    <section className="purchase-chat" aria-label="Chat com o assistente">
      <Tile>
        <Stack gap={4}>
          <div className="purchase-chat__header">
            <Chat size={20} aria-hidden />
            <h2 className="cds--type-heading-compact-01">Assistente virtual</h2>
          </div>

          {!agentAvailable && (
            <InlineNotification
              kind="info"
              title="Assistente indisponível"
              subtitle="O assistente está offline no momento. Você ainda pode responder na seção de confirmação."
              hideCloseButton
              lowContrast
            />
          )}

          {/* Área de mensagens */}
          <div
            className="purchase-chat__messages"
            role="log"
            aria-live="polite"
            aria-label="Conversa com o assistente"
          >
            {historyLoading && (
              <div role="status" style={{ padding: '0.5rem 0' }}>
                <InlineLoading description="Carregando conversa…" status="active" />
              </div>
            )}

            {historyError && (
              <>
                <InlineNotification
                  kind="error"
                  title="Erro ao carregar histórico"
                  subtitle={historyError}
                  hideCloseButton
                  lowContrast
                />
                <Button kind="ghost" size="sm" onClick={loadHistory} style={{ marginTop: '0.25rem' }}>
                  Tentar novamente
                </Button>
              </>
            )}

            {!historyLoading && !historyError && messages !== null && messages.length === 0 && (
              <p className="cds--type-body-01" style={{ color: 'var(--cds-text-secondary)' }}>
                Nenhuma mensagem ainda.
              </p>
            )}

            {messages?.map((m) => (
              <MessageBubble key={m.message_id} message={m} />
            ))}

            {sending && (
              <div role="status" style={{ padding: '0.5rem 0' }}>
                <InlineLoading description="Aguardando resposta do assistente…" status="active" />
              </div>
            )}

            <div ref={bottomRef} aria-hidden />
          </div>

          {sendError && (
            <InlineNotification
              kind="warning"
              title="Atenção"
              subtitle={sendError}
              hideCloseButton
              lowContrast
              onClose={() => setSendError(null)}
            />
          )}

          {/* Área de entrada — desabilitada se o agente não está disponível */}
          {agentAvailable && (
            <div className="purchase-chat__input-area">
              <TextArea
                id={`chat-input-${caseId}`}
                labelText="Escreva uma mensagem"
                hideLabel
                placeholder="Escreva sua mensagem (máx. 1000 caracteres) — Ctrl+Enter para enviar"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyDown={handleKeyDown}
                maxCount={MAX_CHARS}
                enableCounter
                disabled={sending || historyLoading}
                rows={3}
              />
              <Button
                kind="primary"
                size="sm"
                renderIcon={Send}
                iconDescription="Enviar"
                onClick={handleSend}
                disabled={sending || !inputText.trim() || inputText.length > MAX_CHARS || historyLoading}
                style={{ alignSelf: 'flex-end', marginTop: '0.5rem' }}
              >
                Enviar
              </Button>
            </div>
          )}
        </Stack>
      </Tile>
    </section>
  );
}
