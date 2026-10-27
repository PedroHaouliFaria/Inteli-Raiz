import { useNavigate } from 'react-router-dom';
import {
  DataTable, Table, TableHead, TableRow, TableHeader, TableBody, TableCell, TableContainer,
  TableToolbar, TableToolbarContent, TableToolbarSearch, Tag, Tile, Button,
} from '@carbon/react';
import { ESTADOS, nivelRisco, brl } from '../data/casos';
import { useWatson } from '../state/store';
import Termo from '../components/Termo';
import WatsonRail from '../components/WatsonRail';

const HEADERS = [
  { key: 'id', header: 'Caso' },
  { key: 'associado', header: 'Associado' },
  { key: 'valor', header: 'Valor' },
  { key: 'estabelecimento', header: 'Estabelecimento' },
  { key: 'canal', header: 'Canal' },
  { key: 'score', header: 'Score' },
  { key: 'risco', header: 'Risco' },
  { key: 'estado', header: 'Estado' },
  { key: 'naFila', header: 'Na fila' },
];

export default function Fila({ comCelular }) {
  const navigate = useNavigate();
  const { state } = useWatson();
  const abertos = state.casos.filter((c) => c.estado !== 'resolvido').sort((a, b) => b.score * b.valor - a.score * a.valor);
  const resolvidos = state.casos.filter((c) => c.estado === 'resolvido').length;
  const rows = abertos.map((c) => ({ ...c, valor: brl(c.valor), score: c.score.toFixed(2).replace('.', ','), risco: c.score, estado: ESTADOS[c.estado] }));
  const kpis = [
    { chave: 'caso', rotulo: 'Casos abertos', valor: String(abertos.length) },
    { chave: 'alerta', rotulo: 'Alertas em casos abertos', valor: String(abertos.reduce((n, c) => n + c.alertas, 0)) },
    { chave: 'tempoDecisao', rotulo: 'Tempo até a decisão', valor: '3 min 40 s', nota: 'valor fictício no protótipo' },
    { chave: 'aguardandoAssociado', rotulo: 'Aguardando associado', valor: String(abertos.filter((c) => c.estado === 'aguardando').length) },
  ];
  const primeiro = abertos[0];

  return (
    <div className="watson-layout">
      <main className="watson-main" id="main-content">
        <h1 className="cds--type-heading-04">Fila de <Termo chave="caso">casos</Termo></h1>
        <div className="watson-kpis">
          {kpis.map((k) => (
            <Tile key={k.rotulo}>
              <p className="cds--type-label-01"><Termo chave={k.chave}>{k.rotulo}</Termo></p>
              <p className="watson-kpi">{k.valor}</p>
              {k.nota && <p className="cds--type-helper-text-01">{k.nota}</p>}
            </Tile>
          ))}
        </div>
        <DataTable rows={rows} headers={HEADERS}>
          {({ rows: rs, headers, getTableProps, getHeaderProps, getRowProps, onInputChange }) => (
            <TableContainer title="Ordenada por risco × valor" description={`Cada caso junta os alertas do mesmo cartão. ${resolvidos} resolvidos hoje.`}>
              <TableToolbar>
                <TableToolbarContent>
                  <TableToolbarSearch onChange={onInputChange} placeholder="Buscar associado, cartão ou caso" persistent />
                  {primeiro && <Button onClick={() => navigate(`/caso/${primeiro.id}`)}>Abrir caso #{primeiro.id}</Button>}
                </TableToolbarContent>
              </TableToolbar>
              <Table {...getTableProps()}>
                <TableHead>
                  <TableRow>
                    {headers.map((h) => (
                      <TableHeader key={h.key} {...getHeaderProps({ header: h })}>
                        {h.key === 'score' ? <Termo chave="score">Score</Termo> : h.header}
                      </TableHeader>
                    ))}
                  </TableRow>
                </TableHead>
                <TableBody>
                  {rs.map((row) => (
                    <TableRow key={row.id} {...getRowProps({ row })} onClick={() => navigate(`/caso/${row.id}`)} style={{ cursor: 'pointer' }}>
                      {row.cells.map((cell) => (
                        <TableCell key={cell.id}>
                          {cell.info.header === 'risco' ? (
                            <Tag type={nivelRisco(cell.value).tipo} size="sm">{nivelRisco(cell.value).texto}</Tag>
                          ) : cell.info.header === 'id' ? `#${cell.value}` : cell.value}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </DataTable>
      </main>
      <WatsonRail
        titulo="Próximo caso sugerido"
        sugestao={primeiro ? `Comece pelo #${primeiro.id}: ${brl(primeiro.valor)}, score ${primeiro.score.toFixed(2).replace('.', ',')}.` : 'Fila vazia.'}
        porque="maior combinação de score e valor da fila."
        acao={primeiro ? `Abrir #${primeiro.id}` : null}
        onAceitar={() => primeiro && navigate(`/caso/${primeiro.id}`)}
        chips={['Quais casos estão parados?']}
      />
      {comCelular}
    </div>
  );
}
