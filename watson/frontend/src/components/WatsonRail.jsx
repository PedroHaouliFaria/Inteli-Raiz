import { useState } from 'react';
import { AILabel, AILabelContent, Button, IconButton, Tile, Tag } from '@carbon/react';
import { AiLaunch, Close } from '@carbon/icons-react';
import Term from './Term';
import { useRail } from './RailPreferences';

// Trilho "Pergunte ao Watson": sugestão de contexto (protótipo 3) + perguntas por chips (protótipo 2).
const ANSWERS = {
  'Por que 0,92?': {
    text: 'Quatro sinais fortes concordam: rajada de 3 compras em 7 min, 640 km da região habitual, valor 6,2× a média e dispositivo novo. Sozinho, nenhum passaria de 0,40.',
    source: 'Fatores do modelo para o caso #4821',
  },
  'Compare com o histórico': {
    text: 'Nos últimos 12 meses o associado comprou só em Chapecó (SC) e região, sempre presencialmente, com média de R$ 380. Nunca comprou de madrugada.',
    source: 'Histórico de transações do cartão •••• 4821',
  },
  'Redija a justificativa': {
    text: 'Bloqueio preventivo: rajada de 3 compras em 7 min, a 640 km da região habitual, valor 6,2× a média e dispositivo novo.',
    source: 'Gerado a partir dos fatores do caso',
    insertable: true,
  },
  'Quais casos estão parados?': {
    text: 'Os casos #4990 e #4762 aguardam o associado há mais de 20 minutos. Sugiro reenviar o aviso de compra.',
    source: 'Quadro do processo',
  },
};

export default function WatsonRail({ title, suggestion, reason, confidence, actionLabel, onAccept, chips = [], onInsert }) {
  const [question, setQuestion] = useState(null);
  const [accepted, setAccepted] = useState(false);
  const answer = question && ANSWERS[question];
  const { collapsed, toggle } = useRail();

  if (collapsed) {
    return (
      <Button className="watson-rail-launcher" renderIcon={AiLaunch} onClick={toggle}>
        Pergunte ao Watson
      </Button>
    );
  }

  return (
    <aside className="watson-rail watson-rail--overlay" aria-label="Pergunte ao Watson">
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <h2 className="cds--type-heading-02" style={{ flexGrow: 1 }}>Pergunte ao Watson</h2>
        <AILabel size="xs" aria-label="Conteúdo gerado por IA">
          <AILabelContent>
            <p>Sugestões geradas pelo agente a partir dos sinais. A decisão final é sempre da analista.</p>
          </AILabelContent>
        </AILabel>
        <IconButton kind="ghost" size="sm" label="Fechar o painel do Watson" align="bottom-right" onClick={toggle}>
          <Close />
        </IconButton>
      </div>
      {suggestion && (
        <Tile>
          <p className="cds--type-label-01">{title}</p>
          <p className="cds--type-body-01" style={{ margin: '0.5rem 0' }}>{suggestion}</p>
          {confidence && <p className="cds--type-label-01"><Term id="confidence" />: {confidence}</p>}
          {reason && <p className="cds--type-helper-text-01" style={{ marginTop: '0.5rem' }}>Por que estou sugerindo isso: {reason}</p>}
          <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem', flexWrap: 'wrap' }}>
            {actionLabel && !accepted && <Button size="sm" onClick={() => { setAccepted(true); onAccept?.(); }}>{actionLabel}</Button>}
            {accepted && <Tag type="green" size="sm">Aceita</Tag>}
            {accepted && <Button size="sm" kind="ghost" onClick={() => setAccepted(false)}>Reverter</Button>}
            {!accepted && <Button size="sm" kind="ghost">Agora não</Button>}
          </div>
        </Tile>
      )}
      {chips.length > 0 && (
        <div>
          <p className="cds--type-label-01" style={{ marginBottom: '0.5rem' }}>Pergunte</p>
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            {chips.map((c) => (
              <Button key={c} size="sm" kind={question === c ? 'secondary' : 'tertiary'} onClick={() => setQuestion(c)} aria-pressed={question === c}>
                {c}
              </Button>
            ))}
          </div>
        </div>
      )}
      {answer && (
        <Tile>
          <p className="cds--type-label-01">{question}</p>
          <p className="cds--type-body-01" style={{ margin: '0.5rem 0' }}>{answer.text}</p>
          <p className="cds--type-helper-text-01">Fonte: {answer.source}</p>
          {answer.insertable && onInsert && (
            <Button size="sm" kind="ghost" onClick={() => onInsert(answer.text)}>Inserir na justificativa</Button>
          )}
        </Tile>
      )}
    </aside>
  );
}
