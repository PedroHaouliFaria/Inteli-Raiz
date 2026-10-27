import { useState } from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import {
  Breadcrumb, BreadcrumbItem, Tag, Tile, Button, Modal, TextArea, ProgressBar,
  AILabel, AILabelContent, InlineNotification,
} from '@carbon/react';
import { ESTADOS, nivelRisco, brl } from '../data/casos';
import { useWatson } from '../state/store';
import Termo from '../components/Termo';
import WatsonRail from '../components/WatsonRail';

const JUSTIFICATIVA_WATSON =
  'Bloqueio preventivo: rajada de 3 compras em 7 min, a 640 km da região habitual, valor 6,2× a média e dispositivo novo.';

const DECISAO_TAG = {
  bloqueado: { type: 'red', texto: 'Cartão bloqueado' },
  liberado: { type: 'green', texto: 'Compra liberada' },
  escalado: { type: 'purple', texto: 'Escalado' },
};

export default function Caso({ comCelular }) {
  const { id } = useParams();
  const { state, dispatch } = useWatson();
  const caso = state.casos.find((c) => c.id === id) ?? state.casos[0];
  const eventos = state.eventos[caso.id] ?? [];
  const [modal, setModal] = useState(null);
  const [justificativa, setJustificativa] = useState(JUSTIFICATIVA_WATSON);
  const risco = nivelRisco(caso.score);
  const decidir = (decisao) => dispatch({ tipo: 'decidir', casoId: caso.id, decisao, justificativa });
  const resolvido = caso.estado === 'resolvido';
  const aguardando = caso.estado === 'aguardando';
  const voltou = caso.estado === 'analise' && eventos.some((e) => e.tipo === 'alerta');

  return (
    <div className="watson-layout">
      <main className="watson-main" id="main-content">
        <Breadcrumb noTrailingSlash>
          <BreadcrumbItem><RouterLink to="/">Fila</RouterLink></BreadcrumbItem>
          <BreadcrumbItem isCurrentPage>Caso #{caso.id}</BreadcrumbItem>
        </Breadcrumb>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <div style={{ flexGrow: 1 }}>
            <p className="cds--type-label-01"><Termo chave="caso">Caso</Termo> #{caso.id} · {caso.cartao} · {caso.canal} · {caso.alertas} <Termo chave="alerta">alertas</Termo></p>
            <h1 className="cds--type-heading-04">{caso.associado} · {brl(caso.valor)} · {caso.estabelecimento}</h1>
            <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem' }}>
              <Tag type="outline" size="sm">{ESTADOS[caso.estado]}</Tag>
              {caso.decisao && <Tag type={DECISAO_TAG[caso.decisao].type} size="sm">{DECISAO_TAG[caso.decisao].texto} · {caso.por}</Tag>}
            </div>
          </div>
          <Tile>
            <p className="cds--type-label-01"><Termo chave="score">Score de risco</Termo></p>
            <p className="watson-kpi">{caso.score.toFixed(2).replace('.', ',')}</p>
            <Tag type={risco.tipo} size="sm">{risco.texto} risco</Tag>
          </Tile>
        </div>

        {aguardando && (
          <InlineNotification kind="info" lowContrast hideCloseButton title="Aguardando o associado."
            subtitle="Se ele não reconhecer, o Watson bloqueia na hora. Se confirmar com biometria em aparelho conhecido, libera." />
        )}
        {voltou && (
          <InlineNotification kind="warning" lowContrast hideCloseButton title="Voltou para você."
            subtitle="O associado confirmou, mas de um aparelho trocado há 2 dias. O Watson não libera sozinho nesse caso." />
        )}

        <div className="watson-colunas">
          <Tile>
            <h2 className="cds--type-heading-02" style={{ marginBottom: '1rem' }}>Por que é suspeito</h2>
            {(caso.fatores ?? []).map((f) => (
              <ProgressBar key={f.nome} label={f.nome} helperText={`peso ${f.peso.toFixed(2).replace('.', ',')}`} value={f.peso * 100} max={35} size="small" />
            ))}
            {!caso.fatores && <p className="cds--type-body-01">Fatores detalhados só no caso #4821 neste protótipo.</p>}
          </Tile>
          <Tile>
            <h2 className="cds--type-heading-02" style={{ marginBottom: '1rem' }}>Linha do tempo</h2>
            <ol className="watson-timeline">
              <li>
                <span className="watson-timeline__hora">03:14</span>
                <div><p className="cds--type-heading-compact-01">{caso.alertas} <Termo chave="alerta">alertas</Termo> agrupados neste caso</p>
                  <p className="cds--type-helper-text-01">Mesmo cartão, mesma janela de tempo.</p></div>
              </li>
              {eventos.map((e, i) => (
                <li key={i}>
                  <span className="watson-timeline__hora">{e.hora}</span>
                  <div>
                    <p className="cds--type-heading-compact-01">{e.titulo} {e.ia && <Tag type="blue" size="sm">Watson</Tag>}</p>
                    {e.detalhe && <p className="cds--type-helper-text-01">{e.detalhe}</p>}
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
          <TextArea labelText="Justificativa" value={justificativa} onChange={(e) => setJustificativa(e.target.value)} rows={3} disabled={resolvido} />
          <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem', flexWrap: 'wrap', justifyContent: 'flex-end' }}>
            <Button kind="ghost" disabled={resolvido} onClick={() => decidir('escalado')}>Escalar</Button>
            <Button kind="tertiary" disabled={resolvido} onClick={() => decidir('liberado')}>Liberar</Button>
            <Button kind="secondary" disabled={resolvido || aguardando} onClick={() => setModal('perguntar')}>Perguntar ao associado</Button>
            <Button kind="danger" disabled={resolvido} onClick={() => setModal('bloquear')}>Bloquear cartão</Button>
          </div>
        </Tile>

        <Modal
          open={modal === 'perguntar'}
          modalHeading="Perguntar ao associado pelo app?"
          primaryButtonText="Enviar aviso de compra"
          secondaryButtonText="Cancelar"
          onRequestClose={() => setModal(null)}
          onRequestSubmit={() => { setModal(null); dispatch({ tipo: 'enviarAviso', casoId: caso.id }); }}
        >
          <p style={{ marginBottom: '1rem' }}>O Watson envia o <Termo chave="avisoCompra">aviso de compra</Termo> pelo app e aplica esta regra com a resposta:</p>
          <ul style={{ listStyle: 'disc', paddingLeft: '1.25rem' }}>
            <li>“Não reconheço”: bloqueia o cartão na hora.</li>
            <li>“Sim, fui eu” com biometria em aparelho conhecido: libera a compra.</li>
            <li>Aparelho trocado ou sem resposta em 30 min: o caso volta para você.</li>
          </ul>
        </Modal>

        <Modal
          open={modal === 'bloquear'}
          danger
          modalHeading={`Bloquear o cartão ${caso.cartao}?`}
          primaryButtonText="Bloquear cartão"
          secondaryButtonText="Cancelar"
          onRequestClose={() => setModal(null)}
          onRequestSubmit={() => { setModal(null); decidir('bloqueado'); }}
        >
          <p>O associado recebe um aviso explicando o bloqueio. A justificativa fica registrada no caso e pode ser revista.</p>
        </Modal>
      </main>
      <WatsonRail
        key={caso.id + caso.estado}
        titulo="Recomendação"
        sugestao={resolvido ? 'Caso resolvido. Abra o próximo da fila.'
          : voltou ? 'Ligar para o associado pelo número cadastrado antes de liberar. Não confio na confirmação vinda do aparelho novo.'
          : 'Perguntar ao associado pelo app antes de bloquear. Se ele não reconhecer, eu bloqueio na hora.'}
        confianca={resolvido ? null : voltou ? 'média · 61%' : 'alta · 87%'}
        porque={resolvido ? null : voltou ? 'o aparelho foi trocado há 2 dias, sinal comum de troca de chip (anti-persona).' : 'os 4 sinais mais fortes concordam, mas ainda não sei se o associado está viajando.'}
        acao={resolvido || aguardando || voltou ? null : 'Preparar aviso'}
        onAceitar={() => setModal('perguntar')}
        chips={['Por que 0,92?', 'Compare com o histórico', 'Redija a justificativa']}
        onInserir={setJustificativa}
      />
      {comCelular}
    </div>
  );
}
