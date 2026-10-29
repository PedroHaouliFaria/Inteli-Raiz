import { useState } from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import {
  Breadcrumb, BreadcrumbItem, Tag, Tile, Button, Modal, TextArea, ProgressBar,
  AILabel, AILabelContent, InlineNotification, Layer,
} from '@carbon/react';
import { STATUS_LABELS, riskLevel, formatBRL } from '../../mocks/cases';
import { useWatson } from '../../state/store';
import { NOTICE_POLICY } from '../../state/noticePolicy';
import Term from '../../components/Term';
import WatsonRail from '../../components/WatsonRail';
import CaseQueue from './CaseQueue';
import CardTimeline, { BurstIndicator } from './CardTimeline';

const WATSON_JUSTIFICATION =
  'Bloqueio preventivo: 47 tentativas do cartão no terminal na última hora, a 640 km da região habitual, valor 6,2× a média e dispositivo novo.';

const DECISION_TAG = {
  blocked: { type: 'red', label: 'Cartão bloqueado' },
  released: { type: 'green', label: 'Compra liberada' },
  escalated: { type: 'purple', label: 'Escalado' },
};

// Trocar de caso pela fila lateral recria a tela, para a justificativa e os modais não passarem de um caso para o outro.
export default function CasePage({ phoneSlot }) {
  const { id } = useParams();
  return <CaseView key={id} id={id} phoneSlot={phoneSlot} />;
}

function CaseView({ id, phoneSlot }) {
  const { state, dispatch } = useWatson();
  const fraudCase = state.cases.find((c) => c.id === id) ?? state.cases[0];
  const events = state.events[fraudCase.id] ?? [];
  const [modal, setModal] = useState(null);
  const [justification, setJustification] = useState(WATSON_JUSTIFICATION);
  const risk = riskLevel(fraudCase.score);
  const decide = (decision) => dispatch({ type: 'decide', caseId: fraudCase.id, decision, justification });
  const resolved = fraudCase.status === 'resolved';
  const awaiting = fraudCase.status === 'awaiting_member';
  const returned = fraudCase.status === 'in_review' && events.some((e) => e.type === 'alert');

  return (
    <div className="watson-layout">
      <CaseQueue currentId={fraudCase.id} />
      <main className="watson-main" id="main-content">
        <Breadcrumb noTrailingSlash>
          <BreadcrumbItem><RouterLink to="/">Fila</RouterLink></BreadcrumbItem>
          <BreadcrumbItem isCurrentPage>Caso #{fraudCase.id}</BreadcrumbItem>
        </Breadcrumb>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <div style={{ flexGrow: 1 }}>
            <p className="cds--type-label-01"><Term id="case">Caso</Term> #{fraudCase.id} · {fraudCase.card} · {fraudCase.channel} · {fraudCase.alertCount} <Term id="alert">alertas</Term></p>
            <h1 className="cds--type-heading-04">{fraudCase.member} · {formatBRL(fraudCase.amount)} · {fraudCase.merchant}</h1>
            <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem' }}>
              <Tag type="outline" size="sm">{STATUS_LABELS[fraudCase.status]}</Tag>
              {fraudCase.decision && <Tag type={DECISION_TAG[fraudCase.decision].type} size="sm">{DECISION_TAG[fraudCase.decision].label} · {fraudCase.by}</Tag>}
            </div>
          </div>
          <Tile>
            <p className="cds--type-label-01"><Term id="score">Score de risco</Term></p>
            <p className="watson-kpi">{fraudCase.score.toFixed(2).replace('.', ',')}</p>
            <Tag type={risk.tagType} size="sm">{risk.label} risco</Tag>
          </Tile>
        </div>

        {awaiting && fraudCase.autoNotice && (
          <InlineNotification kind="info" lowContrast hideCloseButton title="O Watson enviou o aviso sozinho (risco médio)."
            subtitle={`Você só entra se o associado não reconhecer, pedir atendimento ou não responder em ${NOTICE_POLICY.responseTimeoutMinutes} min.`} />
        )}
        {awaiting && !fraudCase.autoNotice && (
          <InlineNotification kind="info" lowContrast hideCloseButton title="Aguardando o associado."
            subtitle="Se ele não reconhecer, o Watson bloqueia na hora. Se confirmar com biometria em aparelho conhecido, libera." />
        )}
        {returned && (
          <InlineNotification kind="warning" lowContrast hideCloseButton title="Voltou para você."
            subtitle="O associado confirmou, mas de um aparelho trocado há 2 dias. O Watson não libera sozinho nesse caso." />
        )}

        <div className="watson-columns">
          <Tile>
            <h2 className="cds--type-heading-02" style={{ marginBottom: '1rem' }}>Por que é suspeito</h2>
            {(fraudCase.factors ?? []).map((f) => (
              <ProgressBar key={f.name} label={f.name} helperText={`peso ${f.weight.toFixed(2).replace('.', ',')}`} value={f.weight * 100} max={35} size="small" />
            ))}
            {!fraudCase.factors && <p className="cds--type-body-01">Fatores detalhados só no caso #4821 neste protótipo.</p>}
          </Tile>
          <Tile>
            <h2 className="cds--type-heading-02" style={{ marginBottom: '1rem' }}>Linha do tempo</h2>
            <BurstIndicator velocity1h={fraudCase.velocity1h} />
            <CardTimeline history={fraudCase.cardHistory} />
            <h3 className="cds--type-heading-compact-01" style={{ margin: '1rem 0 0.5rem' }}>Eventos do caso</h3>
            <ol className="watson-timeline">
              <li>
                <span className="watson-timeline__time">03:14</span>
                <div><p className="cds--type-heading-compact-01">{fraudCase.alertCount} <Term id="alert">alertas</Term> agrupados neste caso</p>
                  <p className="cds--type-helper-text-01">Mesmo cartão, mesma janela de tempo.</p></div>
              </li>
              {events.map((e, i) => (
                <li key={i}>
                  <span className="watson-timeline__time">{e.time}</span>
                  <div>
                    <p className="cds--type-heading-compact-01">{e.title} {e.ai && <Tag type="blue" size="sm">Watson</Tag>}</p>
                    {e.detail && <p className="cds--type-helper-text-01">{e.detail}</p>}
                  </div>
                </li>
              ))}
            </ol>
          </Tile>
        </div>

        <Tile>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <h2 className="cds--type-heading-02" style={{ flexGrow: 1 }}>Sua decisão</h2>
            <AILabel size="xs" aria-label="Justificativa gerada por IA">
              <AILabelContent><p>Texto redigido pelo Watson. Edite antes de registrar.</p></AILabelContent>
            </AILabel>
          </div>
          {/* Layer: dentro do Tile o campo usa o fundo de field da camada seguinte, para ler como caixa de texto. */}
          <Layer>
            <TextArea id="decision-justification" labelText="Justificativa" helperText="Escrita pelo Watson a partir dos sinais. Revise e edite antes de registrar a decisão."
              value={justification} onChange={(e) => setJustification(e.target.value)} rows={4} enableCounter maxCount={500} disabled={resolved} />
          </Layer>
          <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem', flexWrap: 'wrap', justifyContent: 'flex-end' }}>
            <Button kind="ghost" disabled={resolved} onClick={() => decide('escalated')}>Escalar</Button>
            <Button kind="tertiary" disabled={resolved} onClick={() => decide('released')}>Liberar</Button>
            <Button kind="secondary" disabled={resolved || awaiting} onClick={() => setModal('ask')}>Perguntar ao associado</Button>
            <Button kind="danger" disabled={resolved} onClick={() => setModal('block')}>Bloquear cartão</Button>
          </div>
        </Tile>

        <Modal
          open={modal === 'ask'}
          modalHeading="Perguntar ao associado pelo app?"
          primaryButtonText="Enviar aviso de compra"
          secondaryButtonText="Cancelar"
          onRequestClose={() => setModal(null)}
          onRequestSubmit={() => { setModal(null); dispatch({ type: 'sendNotice', caseId: fraudCase.id }); }}
        >
          <p style={{ marginBottom: '1rem' }}>O Watson envia o <Term id="purchaseNotice">aviso de compra</Term> pelo app e aplica esta regra com a resposta:</p>
          <ul style={{ listStyle: 'disc', paddingLeft: '1.25rem' }}>
            <li>“Não reconheço”: bloqueia o cartão na hora.</li>
            <li>“Sim, fui eu” com biometria em aparelho conhecido: libera a compra.</li>
            <li>Aparelho trocado ou sem resposta em {NOTICE_POLICY.responseTimeoutMinutes} min: o caso volta para você.</li>
          </ul>
        </Modal>

        <Modal
          open={modal === 'block'}
          danger
          modalHeading={`Bloquear o cartão ${fraudCase.card}?`}
          primaryButtonText="Bloquear cartão"
          secondaryButtonText="Cancelar"
          onRequestClose={() => setModal(null)}
          onRequestSubmit={() => { setModal(null); decide('blocked'); }}
        >
          <p>O associado recebe um aviso explicando o bloqueio. A justificativa fica registrada no caso e pode ser revista.</p>
        </Modal>
      </main>
      <WatsonRail
        key={fraudCase.id + fraudCase.status}
        title="Recomendação"
        suggestion={resolved ? 'Caso resolvido. Abra o próximo da fila.'
          : awaiting && fraudCase.autoNotice ? 'Nada a fazer agora: enviei o aviso de compra e te chamo se houver exceção.'
          : returned ? 'Ligar para o associado pelo número cadastrado antes de liberar. Não confio na confirmação vinda do aparelho novo.'
          : 'Perguntar ao associado pelo app antes de bloquear. Se ele não reconhecer, eu bloqueio na hora.'}
        confidence={resolved || fraudCase.autoNotice ? null : returned ? 'média · 61%' : 'alta · 87%'}
        reason={resolved ? null : fraudCase.autoNotice ? 'risco médio: pela política, eu mesmo pergunto ao associado.'  : returned ? 'o aparelho foi trocado há 2 dias, sinal comum de troca de chip (anti-persona).' : 'os 4 sinais mais fortes concordam, mas ainda não sei se o associado está viajando.'}
        actionLabel={resolved || awaiting || returned ? null : 'Preparar aviso'}
        onAccept={() => setModal('ask')}
        chips={['Por que 0,92?', 'Compare com o histórico', 'Redija a justificativa']}
        onInsert={setJustification}
      />
      {phoneSlot}
    </div>
  );
}
