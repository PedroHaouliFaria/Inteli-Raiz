import { useNavigate } from 'react-router-dom';
import {
  DataTable, Table, TableHead, TableRow, TableHeader, TableBody, TableCell, TableContainer,
  TableToolbar, TableToolbarContent, TableToolbarSearch, Tag, Tile, Button,
} from '@carbon/react';
import { STATUS_LABELS, ESCALATION_LABELS, riskLevel, formatBRL } from '../../mocks/cases';
import { useWatson } from '../../state/store';
import { analystQueue, isWithWatson } from '../../state/queue';
import Term from '../../components/Term';
import WatsonRail from '../../components/WatsonRail';

const HEADERS = [
  { key: 'id', header: 'Caso' },
  { key: 'member', header: 'Associado' },
  { key: 'amount', header: 'Valor' },
  { key: 'merchant', header: 'Estabelecimento' },
  { key: 'channel', header: 'Canal' },
  { key: 'score', header: 'Score' },
  { key: 'risk', header: 'Risco' },
  { key: 'status', header: 'Estado' },
  { key: 'escalation', header: 'Por que está com você' },
  { key: 'waitTime', header: 'Na fila' },
];

export default function QueuePage({ phoneSlot }) {
  const navigate = useNavigate();
  const { state } = useWatson();
  // Casos de risco médio aguardando o associado ficam com o Watson; a fila mostra só o que precisa da analista.
  const withWatson = state.cases.filter(isWithWatson);
  const open = analystQueue(state.cases);
  const resolvedCount = state.cases.filter((c) => c.status === 'resolved').length;
  const rows = open.map((c) => ({ ...c, amount: formatBRL(c.amount), score: c.score.toFixed(2).replace('.', ','), risk: c.score, status: STATUS_LABELS[c.status], escalation: ESCALATION_LABELS[c.escalationReason] ?? '—' }));
  const kpis = [
    { termId: 'case', label: 'Casos abertos', value: String(open.length) },
    { termId: 'alert', label: 'Alertas em casos abertos', value: String(open.reduce((n, c) => n + c.alertCount, 0)) },
    { termId: 'timeToDecision', label: 'Tempo até a decisão', value: '3 min 40 s', note: 'valor fictício no protótipo' },
    { termId: 'awaitingMember', label: 'Aguardando associado', value: String(open.filter((c) => c.status === 'awaiting_member').length) },
    { termId: 'purchaseNotice', label: 'Conduzidos pelo Watson', value: String(withWatson.length), note: 'risco médio, aviso enviado sozinho' },
  ];
  const first = open[0];

  return (
    <div className="watson-layout">
      <main className="watson-main" id="main-content">
        <h1 className="cds--type-heading-04">Fila de <Term id="case">casos</Term></h1>
        <div className="watson-kpis">
          {kpis.map((k) => (
            <Tile key={k.label}>
              <p className="cds--type-label-01"><Term id={k.termId}>{k.label}</Term></p>
              <p className="watson-kpi">{k.value}</p>
              {k.note && <p className="cds--type-helper-text-01">{k.note}</p>}
            </Tile>
          ))}
        </div>
        <DataTable rows={rows} headers={HEADERS}>
          {({ rows: rs, headers, getTableProps, getHeaderProps, getRowProps, onInputChange }) => (
            <TableContainer title="Ordenada por risco × valor" description={`Cada caso junta os alertas do mesmo cartão. ${resolvedCount} resolvidos hoje.`}>
              <TableToolbar>
                <TableToolbarContent>
                  <TableToolbarSearch onChange={onInputChange} placeholder="Buscar associado, cartão ou caso" persistent />
                  {first && <Button onClick={() => navigate(`/cases/${first.id}`)}>Abrir caso #{first.id}</Button>}
                </TableToolbarContent>
              </TableToolbar>
              <Table {...getTableProps()}>
                <TableHead>
                  <TableRow>
                    {headers.map((h) => (
                      <TableHeader key={h.key} {...getHeaderProps({ header: h })}>
                        {h.key === 'score' ? <Term id="score">Score</Term> : h.header}
                      </TableHeader>
                    ))}
                  </TableRow>
                </TableHead>
                <TableBody>
                  {rs.map((row) => (
                    <TableRow key={row.id} {...getRowProps({ row })} onClick={() => navigate(`/cases/${row.id}`)} style={{ cursor: 'pointer' }}>
                      {row.cells.map((cell) => (
                        <TableCell key={cell.id}>
                          {cell.info.header === 'risk' ? (
                            <Tag type={riskLevel(cell.value).tagType} size="sm">{riskLevel(cell.value).label}</Tag>
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
        title="Próximo caso sugerido"
        suggestion={first ? `Comece pelo #${first.id}: ${formatBRL(first.amount)}, score ${first.score.toFixed(2).replace('.', ',')}.` : 'Fila vazia.'}
        reason="maior combinação de score e valor da fila."
        actionLabel={first ? `Abrir #${first.id}` : null}
        onAccept={() => first && navigate(`/cases/${first.id}`)}
        chips={['Quais casos estão parados?']}
      />
      {phoneSlot}
    </div>
  );
}
