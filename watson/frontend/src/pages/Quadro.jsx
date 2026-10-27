import { useNavigate } from 'react-router-dom';
import { Tile, Tag, Button } from '@carbon/react';
import { ESTADOS, nivelRisco, brl } from '../data/casos';
import { useWatson } from '../state/store';
import Termo from '../components/Termo';
import WatsonRail from '../components/WatsonRail';

export default function Quadro({ comCelular }) {
  const navigate = useNavigate();
  const { state, dispatch } = useWatson();
  const parados = state.casos.filter((c) => c.estado === 'aguardando' && parseInt(c.naFila, 10) > 20).map((c) => c.id);
  return (
    <div className="watson-layout">
      <main className="watson-main" id="main-content">
        <h1 className="cds--type-heading-04">Quadro do processo</h1>
        <div style={{ overflowX: 'auto' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, minmax(220px, 1fr))', gap: '1rem', minWidth: 940 }}>
            {Object.entries(ESTADOS).map(([estado, nome]) => {
              const lista = state.casos.filter((c) => c.estado === estado);
              return (
                <section key={estado} aria-label={nome} className="watson-coluna">
                  <h2 className="cds--type-heading-compact-01">
                    {estado === 'aguardando' ? <Termo chave="aguardandoAssociado">{nome}</Termo> : nome} · {lista.length}
                  </h2>
                  {lista.map((c) => (
                    <Tile key={c.id}>
                      <p className="cds--type-label-01">
                        Caso #{c.id} · {c.alertas} <Termo chave="alerta">{c.alertas > 1 ? 'alertas' : 'alerta'}</Termo>
                      </p>
                      <p className="cds--type-heading-03">{brl(c.valor)}</p>
                      <p className="cds--type-body-compact-01">{c.estabelecimento}</p>
                      <div style={{ display: 'flex', gap: '0.25rem', margin: '0.5rem 0', flexWrap: 'wrap' }}>
                        <Tag type={nivelRisco(c.score).tipo} size="sm">{nivelRisco(c.score).texto} · {c.score.toFixed(2).replace('.', ',')}</Tag>
                        <Tag type="outline" size="sm">{c.canal}</Tag>
                        {c.decisao && <Tag type={c.decisao === 'bloqueado' ? 'red' : 'green'} size="sm">{c.decisao === 'bloqueado' ? 'Bloqueado' : 'Liberado'} por {c.por}</Tag>}
                      </div>
                      <div style={{ display: 'flex', gap: '0.25rem', flexWrap: 'wrap' }}>
                        <Button kind="ghost" size="sm" onClick={() => navigate(`/caso/${c.id}`)}>Abrir caso</Button>
                        {c.id === '5107' && !c.grupoDesfeito && (
                          <Button kind="ghost" size="sm" onClick={() => dispatch({ tipo: 'desagrupar', casoId: c.id })}>Desagrupar</Button>
                        )}
                      </div>
                    </Tile>
                  ))}
                </section>
              );
            })}
          </div>
        </div>
      </main>
      <WatsonRail
        titulo="Gargalo"
        sugestao={parados.length ? `${parados.length} casos aguardam o associado há mais de 20 min. Sugiro reenviar o aviso de compra.` : 'Nenhum caso parado.'}
        porque="sem resposta, a compra segue pausada e o associado pode ser barrado no balcão."
        acao={parados.length ? `Reenviar aviso aos ${parados.length}` : null}
        onAceitar={() => dispatch({ tipo: 'reenviarAvisos', ids: parados })}
        chips={['Quais casos estão parados?']}
      />
      {comCelular}
    </div>
  );
}
