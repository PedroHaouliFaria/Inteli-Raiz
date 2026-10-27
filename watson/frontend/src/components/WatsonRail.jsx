import { useState } from 'react';
import { AILabel, AILabelContent, Button, Tile, Tag } from '@carbon/react';
import Termo from './Termo';

// Trilho "Pergunte ao Watson": sugestão de contexto (protótipo 3) + perguntas por chips (protótipo 2).
const RESPOSTAS = {
  'Por que 0,92?': {
    texto: 'Quatro sinais fortes concordam: rajada de 3 compras em 7 min, 640 km da região habitual, valor 6,2× a média e dispositivo novo. Sozinho, nenhum passaria de 0,40.',
    fonte: 'Fatores do modelo para o caso #4821',
  },
  'Compare com o histórico': {
    texto: 'Nos últimos 12 meses o associado comprou só em Chapecó (SC) e região, sempre presencialmente, com média de R$ 380. Nunca comprou de madrugada.',
    fonte: 'Histórico de transações do cartão •••• 4821',
  },
  'Redija a justificativa': {
    texto: 'Bloqueio preventivo: rajada de 3 compras em 7 min, a 640 km da região habitual, valor 6,2× a média e dispositivo novo.',
    fonte: 'Gerado a partir dos fatores do caso',
    inserir: true,
  },
  'Quais casos estão parados?': {
    texto: 'Os casos #4990 e #4762 aguardam o associado há mais de 20 minutos. Sugiro reenviar o aviso de compra.',
    fonte: 'Quadro do processo',
  },
};

export default function WatsonRail({ titulo, sugestao, porque, confianca, acao, onAceitar, chips = [], onInserir }) {
  const [pergunta, setPergunta] = useState(null);
  const [aceita, setAceita] = useState(false);
  const resp = pergunta && RESPOSTAS[pergunta];
  return (
    <aside className="watson-rail" aria-label="Pergunte ao Watson">
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <h2 className="cds--type-heading-02" style={{ flexGrow: 1 }}>Pergunte ao Watson</h2>
        <AILabel size="xs" aria-label="Conteúdo gerado por IA">
          <AILabelContent>
            <p>Sugestões geradas pelo agente a partir dos sinais. A decisão final é sempre da analista.</p>
          </AILabelContent>
        </AILabel>
      </div>
      {sugestao && (
        <Tile>
          <p className="cds--type-label-01">{titulo}</p>
          <p className="cds--type-body-01" style={{ margin: '0.5rem 0' }}>{sugestao}</p>
          {confianca && <p className="cds--type-label-01"><Termo chave="confianca" />: {confianca}</p>}
          {porque && <p className="cds--type-helper-text-01" style={{ marginTop: '0.5rem' }}>Por que estou sugerindo isso: {porque}</p>}
          <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem', flexWrap: 'wrap' }}>
            {acao && !aceita && <Button size="sm" onClick={() => { setAceita(true); onAceitar?.(); }}>{acao}</Button>}
            {aceita && <Tag type="green" size="sm">Aceita</Tag>}
            {aceita && <Button size="sm" kind="ghost" onClick={() => setAceita(false)}>Reverter</Button>}
            {!aceita && <Button size="sm" kind="ghost">Agora não</Button>}
          </div>
        </Tile>
      )}
      {chips.length > 0 && (
        <div>
          <p className="cds--type-label-01" style={{ marginBottom: '0.5rem' }}>Pergunte</p>
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            {chips.map((c) => (
              <Button key={c} size="sm" kind={pergunta === c ? 'secondary' : 'tertiary'} onClick={() => setPergunta(c)} aria-pressed={pergunta === c}>
                {c}
              </Button>
            ))}
          </div>
        </div>
      )}
      {resp && (
        <Tile>
          <p className="cds--type-label-01">{pergunta}</p>
          <p className="cds--type-body-01" style={{ margin: '0.5rem 0' }}>{resp.texto}</p>
          <p className="cds--type-helper-text-01">Fonte: {resp.fonte}</p>
          {resp.inserir && onInserir && (
            <Button size="sm" kind="ghost" onClick={() => onInserir(resp.texto)}>Inserir na justificativa</Button>
          )}
        </Tile>
      )}
    </aside>
  );
}
