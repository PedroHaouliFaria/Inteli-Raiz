/**
 * AnalystApp — experiência conectada à API para sessão ANALISTA.
 *
 * Renderiza a lista de revisões abertas (GET /api/reviews) com todos
 * os campos previstos no §8 do contrato:
 *   protocol, case_id, kind, reason, status, created_by, created_at,
 *   case_status, customer_display_name, amount, analysis (score, score_source,
 *   model_version).
 *
 * Score aparece somente aqui, rotulado como "score interno do modelo".
 * O valor é exibido como decimal — nunca convertido em percentual ou
 * "probabilidade de fraude".
 *
 * A analista pode liberar ou recusar a compra na simulação; a ação fecha a
 * revisão, registra auditoria e remove o item da fila aberta.
 * Não tenta GET /api/purchases/{case_id} (rota vinculada à sessão do associado).
 * Sem estado mockado de src/state/store.jsx.
 */
import { useCallback, useEffect, useState } from 'react';
import {
  Button,
  Header,
  HeaderGlobalBar,
  HeaderGlobalAction,
  HeaderName,
  InlineLoading,
  InlineNotification,
  Select,
  SelectItem,
  SkipToContent,
  Stack,
  Tag,
  Theme,
  Tile,
} from '@carbon/react';
import { Renew, Logout } from '@carbon/icons-react';
import { useLocation, useNavigate, useSearchParams } from 'react-router-dom';
import {
  ApiError,
  getAnalystDashboard,
  getAnalystPurchaseFlow,
  getReviews,
} from '../../api/client.js';
import { useSession } from '../session/SessionGate.jsx';
import { formatDate, formatMoney, statusMeta } from '../associate/utils.js';
import { PurchaseStatusBadge } from '../associate/PurchaseStatus.jsx';
import DemoResetButton from '../associate/DemoResetButton.jsx';
import AnalystDashboard from './AnalystDashboard.jsx';

// ── Rótulos legíveis para enums do contrato ─────────────────────────────────

const KIND_LABEL = {
  DUVIDA: 'Dúvida',
  PROTECAO: 'Proteção',
  FALHA_AVALIACAO: 'Falha na avaliação',
  RISCO_ALTO: 'Risco alto',
};

const REASON_LABEL = {
  NAO_RECONHECE_ESTABELECIMENTO: 'Não reconhece o estabelecimento',
  VALOR_DIFERENTE: 'Valor diferente do esperado',
  DUVIDA_PROCESSO: 'Dúvida sobre o processo',
  OUTRO: 'Outro',
};

const CREATED_BY_LABEL = {
  ASSOCIADO: 'Associado',
  AGENTE: 'Agente',
  SISTEMA: 'Sistema',
};

const REVIEW_STATUS_TAG = {
  ABERTA: 'blue',
  FECHADA: 'gray',
};

const DECISION_LABEL = {
  AUTHORIZE: 'Autorizada',
  DENY: 'Recusada',
};

// ── Componente de um item de revisão ────────────────────────────────────────

function ReviewCard({ review, onOpen }) {
  const reviewTagType = REVIEW_STATUS_TAG[review.status] ?? 'gray';
  const score = review.analysis?.score;
  const hasScore = score !== null && score !== undefined;

  return (
    <Tile className="analyst-review-card">
      {/* Linha de cabeçalho: protocolo + status da revisão */}
      <div className="analyst-review-card__header">
        <div className="analyst-review-card__title-row">
          <span className="cds--type-heading-compact-02 analyst-review-card__protocol">
            {review.protocol}
          </span>
          <Tag size="sm" type={reviewTagType}>
            {review.status === 'ABERTA' ? 'Aberta' : 'Fechada'}
          </Tag>
        </div>
        <span className="cds--type-label-01 analyst-review-card__meta">
          {KIND_LABEL[review.kind] ?? review.kind}
          {' · '}
          {CREATED_BY_LABEL[review.created_by] ?? review.created_by}
          {' · '}
          {formatDate(review.created_at)}
        </span>
      </div>

      {/* Grade de detalhes */}
      <dl className="analyst-review-card__grid">
        <div className="analyst-review-card__field">
          <dt className="cds--type-label-01 analyst-review-card__label">Associado</dt>
          <dd className="cds--type-body-compact-01">{review.customer_display_name}</dd>
        </div>

        {review.status === 'FECHADA' && (
          <>
            <div className="analyst-review-card__field">
              <dt className="cds--type-label-01 analyst-review-card__label">Decisão</dt>
              <dd className="cds--type-body-compact-01">{DECISION_LABEL[review.decision] ?? review.decision}</dd>
            </div>
            <div className="analyst-review-card__field">
              <dt className="cds--type-label-01 analyst-review-card__label">Responsável</dt>
              <dd className="cds--type-body-compact-01">{review.decided_by ?? 'Não informado'}</dd>
            </div>
            <div className="analyst-review-card__field">
              <dt className="cds--type-label-01 analyst-review-card__label">Encerrada em</dt>
              <dd className="cds--type-body-compact-01">{review.decided_at ? formatDate(review.decided_at) : 'Não informado'}</dd>
            </div>
          </>
        )}
        <div className="analyst-review-card__field">
          <dt className="cds--type-label-01 analyst-review-card__label">Caso</dt>
          <dd className="cds--type-body-compact-01">{review.case_id}</dd>
        </div>
        <div className="analyst-review-card__field">
          <dt className="cds--type-label-01 analyst-review-card__label">Valor</dt>
          <dd className="cds--type-body-compact-01">{formatMoney(review.amount)}</dd>
        </div>
        <div className="analyst-review-card__field">
          <dt className="cds--type-label-01 analyst-review-card__label">Motivo</dt>
          <dd className="cds--type-body-compact-01">{REASON_LABEL[review.reason] ?? review.reason}</dd>
        </div>
        <div className="analyst-review-card__field">
          <dt className="cds--type-label-01 analyst-review-card__label">Status da compra</dt>
          <dd className="analyst-review-card__status-dd">
            <PurchaseStatusBadge
              status={review.case_status}
              label={statusMeta(review.case_status).shortLabel}
            />
          </dd>
        </div>

        {/* Score interno: exibido apenas aqui, para o analista */}
        <div className="analyst-review-card__field analyst-review-card__field--score">
          <dt className="cds--type-label-01 analyst-review-card__label">
            Score interno do modelo
          </dt>
          <dd className="analyst-review-card__score-dd">
            {hasScore ? (
              <>
                <span className="cds--type-heading-compact-02 analyst-review-card__score-value">
                  {score.toFixed(4)}
                </span>
                {review.analysis.score_source && (
                  <span className="cds--type-label-01 analyst-review-card__score-meta">
                    {review.analysis.score_source}
                    {review.analysis.model_version && ` · ${review.analysis.model_version}`}
                  </span>
                )}
              </>
            ) : (
              <span className="cds--type-label-01" style={{ color: 'var(--cds-text-helper)' }}>
                Não disponível
              </span>
            )}
          </dd>
        </div>
      </dl>

      <div className="analyst-review-card__actions" aria-label={`Ações da revisão ${review.protocol}`}>
        <Button
          size="sm"
          kind="primary"
          onClick={() => onOpen(review.review_id)}
        >
          Ver detalhes
        </Button>
      </div>
    </Tile>
  );
}

const FLOW_STATUS_OPTIONS = [
  ['AGUARDANDO_ASSOCIADO', 'Aguardando associado'],
  ['LIBERADA_AUTOMATICAMENTE', 'Liberadas automaticamente'],
  ['BLOQUEADA_PREVENTIVAMENTE', 'Bloqueadas preventivamente'],
  ['CONTESTACAO_ABERTA', 'Contestações abertas'],
  ['REVISAO_PENDENTE', 'Em revisão'],
  ['LIBERADA_SIMULACAO', 'Autorizadas pela analista'],
  ['RECUSADA_SIMULACAO', 'Recusadas pela analista'],
  ['CONFIRMACAO_EXPIRADA', 'Prazo encerrado'],
];

function FlowSummary({ data }) {
  const visibleStatusCounts = data.purchases.reduce((counts, purchase) => {
    counts[purchase.status] = (counts[purchase.status] ?? 0) + 1;
    return counts;
  }, {});
  const count = (...statuses) => statuses.reduce(
    (total, status) => total + (visibleStatusCounts[status] ?? 0),
    0,
  );
  const summaries = [
    ['Compras exibidas', data.total, 'neutral'],
    ['Aprovadas', count('LIBERADA_AUTOMATICAMENTE', 'LIBERADA_SIMULACAO'), 'success'],
    ['Rejeitadas', count('RECUSADA_SIMULACAO'), 'danger'],
    ['Em análise', count('CONTESTACAO_ABERTA', 'REVISAO_PENDENTE'), 'review'],
  ];
  return (
    <div className="analyst-flow-summary" aria-label="Resumo do fluxo">
      {summaries.map(([label, value, tone]) => (
        <Tile key={label} className={`analyst-flow-summary__tile analyst-flow-summary__tile--${tone}`}>
          <span className="cds--type-label-01">{label}</span>
          <strong className="cds--type-heading-04">{value}</strong>
        </Tile>
      ))}
    </div>
  );
}

function AnalystFlow({ data }) {
  const groups = data.purchases.reduce((result, purchase) => {
    const current = result.get(purchase.customer_id) ?? {
      name: purchase.customer_display_name,
      purchases: [],
    };
    current.purchases.push(purchase);
    result.set(purchase.customer_id, current);
    return result;
  }, new Map());

  return (
    <>
      <FlowSummary data={data} />
      {data.purchases.length === 0 ? (
        <div className="analyst-empty-state" role="status">
          <p className="cds--type-body-01">Nenhuma compra encontrada para estes filtros.</p>
        </div>
      ) : (
        <div className="analyst-flow-customers">
          {[...groups.entries()].map(([customerId, group]) => (
            <section key={customerId} className="analyst-flow-customer" aria-labelledby={`customer-${customerId}`}>
              <div className="analyst-flow-customer__header">
                <div>
                  <p className="cds--type-label-01">Associado</p>
                  <h2 id={`customer-${customerId}`} className="cds--type-heading-compact-02">{group.name}</h2>
                </div>
                <Tag size="sm" type="gray">{group.purchases.length} compras</Tag>
              </div>
              <div className="analyst-flow-list" role="list">
                {group.purchases.map((purchase) => (
                  <article key={purchase.case_id} className="analyst-flow-item" role="listitem">
                    <div className="analyst-flow-item__main">
                      <div>
                        <span className="cds--type-label-01 analyst-flow-item__case">{purchase.case_id}</span>
                        <h3 className="cds--type-body-compact-02">{purchase.merchant_display}</h3>
                      </div>
                      <strong className="cds--type-heading-compact-01">{formatMoney(purchase.amount)}</strong>
                    </div>
                    <div className="analyst-flow-item__meta">
                      <span className="cds--type-label-01">{formatDate(purchase.occurred_at)}</span>
                      {purchase.review_protocol && (
                        <span className="cds--type-label-01">Protocolo {purchase.review_protocol}</span>
                      )}
                      <PurchaseStatusBadge status={purchase.status} label={purchase.status_label} />
                    </div>
                  </article>
                ))}
              </div>
            </section>
          ))}
        </div>
      )}
    </>
  );
}

// ── Componente principal ─────────────────────────────────────────────────────

export default function AnalystApp({ mode = 'open' }) {
  const session = useSession();
  const navigate = useNavigate();
  const location = useLocation();
  const [searchParams, setSearchParams] = useSearchParams();

  const [reviews, setReviews] = useState(null);
  const [flowData, setFlowData] = useState(null);
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [loggingOut, setLoggingOut] = useState(false);
  const [pagination, setPagination] = useState({ total: 0, totalPages: 0 });

  const isHistory = mode === 'history';
  const isFlow = mode === 'flow';
  const isDashboard = mode === 'dashboard';
  const decisionFilter = isHistory ? searchParams.get('decision') ?? '' : '';
  const customerFilter = isFlow ? searchParams.get('customer') ?? '' : '';
  const statusFilter = isFlow ? searchParams.get('status') ?? '' : '';
  const parsedPage = Number.parseInt(searchParams.get('page') ?? '1', 10);
  const page = Number.isFinite(parsedPage) && parsedPage > 0 ? parsedPage : 1;

  const updateHistoryQuery = (nextDecision, nextPage) => {
    const params = new URLSearchParams();
    if (nextDecision) params.set('decision', nextDecision);
    if (nextPage > 1) params.set('page', String(nextPage));
    setSearchParams(params);
  };

  const updateFlowQuery = (nextCustomer, nextStatus) => {
    const params = new URLSearchParams();
    if (nextCustomer) params.set('customer', nextCustomer);
    if (nextStatus) params.set('status', nextStatus);
    setSearchParams(params);
  };

  const loadContent = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      if (isDashboard) {
        setDashboardData(await getAnalystDashboard());
        return;
      }
      if (isFlow) {
        const data = await getAnalystPurchaseFlow({
          customerId: customerFilter || undefined,
          status: statusFilter || undefined,
        });
        setFlowData(data);
        return;
      }
      const data = await getReviews({
        status: isHistory ? 'FECHADA' : 'ABERTA',
        decision: isHistory ? decisionFilter || undefined : undefined,
        page,
      });
      setReviews(data.reviews);
      setPagination({ total: data.total, totalPages: data.total_pages });
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Erro de rede ao carregar revisões.');
    } finally {
      setLoading(false);
    }
  }, [customerFilter, decisionFilter, isDashboard, isFlow, isHistory, page, statusFilter]);

  useEffect(() => {
    loadContent();
  }, [loadContent]);

  const handleLogout = async () => {
    setLoggingOut(true);
    try {
      await session.endSession();
    } finally {
      setLoggingOut(false);
    }
  };

  return (
    <Theme theme="g10">
      {/* Cabeçalho */}
      <Theme theme="g100">
        <Header aria-label="Raiz · Revisões">
          <SkipToContent />
          <HeaderName href="/analyst/reviews/open" prefix="Raiz">
            Revisões
          </HeaderName>
          <HeaderGlobalBar>
            <Tag
              size="sm"
              type="blue"
              style={{ marginRight: '0.5rem', alignSelf: 'center' }}
              aria-label={`Sessão: ${session.display_name}`}
            >
              {session.display_name}
            </Tag>
            <HeaderGlobalAction
              aria-label="Atualizar lista de revisões"
              onClick={loadContent}
              disabled={loading}
            >
              <Renew size={20} />
            </HeaderGlobalAction>
            <HeaderGlobalAction
              aria-label="Sair da sessão"
              onClick={handleLogout}
              disabled={loggingOut}
              tooltipAlignment="end"
            >
              <Logout size={20} />
            </HeaderGlobalAction>
          </HeaderGlobalBar>
        </Header>
      </Theme>

      <main
        className="analyst-app"
        aria-label={isDashboard ? 'Dados e indicadores' : isFlow ? 'Fluxo atual das compras' : 'Lista de revisões'}
      >
        <nav className="analyst-tabs" aria-label="Áreas do analista">
          <Button
            kind={!isHistory && !isFlow && !isDashboard ? 'primary' : 'ghost'}
            size="sm"
            onClick={() => navigate('/analyst/reviews/open')}
          >
            Pendentes
          </Button>
          <Button
            kind={isHistory ? 'primary' : 'ghost'}
            size="sm"
            onClick={() => navigate('/analyst/reviews/history')}
          >
            Histórico
          </Button>
          <Button
            kind={isFlow ? 'primary' : 'ghost'}
            size="sm"
            onClick={() => navigate('/analyst/purchases')}
          >
            Fluxo atual
          </Button>
          <Button
            kind={isDashboard ? 'primary' : 'ghost'}
            size="sm"
            onClick={() => navigate('/analyst/dashboard')}
          >
            Dados
          </Button>
        </nav>

        {/* Cabeçalho da página */}
        <div className="analyst-page-header">
          <div>
            <h1 className="cds--type-heading-compact-02">
              {isDashboard
                ? 'Dados e indicadores'
                : isFlow
                ? 'Fluxo atual das compras'
                : isHistory
                  ? 'Histórico de revisões'
                  : 'Revisões pendentes'}
            </h1>
            <p
              className="cds--type-label-01"
              style={{ color: 'var(--cds-text-helper)', marginTop: '0.25rem' }}
            >
              {isDashboard
                ? 'Visão consolidada da operação, com volume, clientes, status e revisões.'
                : isFlow
                ? 'Acompanhe todas as compras por associado, sem misturá-las à fila de decisão.'
                : isHistory
                  ? 'Consulte revisões encerradas e as decisões registradas.'
                  : 'Somente compras cuja revisão foi solicitada e ainda precisa de decisão.'}
            </p>
            {session.demo_mode && (
              <div style={{ marginTop: '0.75rem' }}>
                <DemoResetButton variant="button" onReset={loadContent} />
              </div>
            )}
          </div>
          {/* Aviso de simulação visível */}
          <div className="analyst-simulation-badge" role="note" aria-label="Aviso de simulação">
            <span className="cds--type-label-01">
              ⚠ Dados e decisões simulados. Nenhuma ação financeira real é executada.
            </span>
          </div>
        </div>

        {isHistory && (
          <div style={{ maxWidth: '18rem', marginBottom: '1rem' }}>
            <Select
              id="history-decision-filter"
              labelText="Filtrar por decisão"
              value={decisionFilter}
              onChange={(event) => updateHistoryQuery(event.target.value, 1)}
            >
              <SelectItem value="" text="Todas" />
              <SelectItem value="AUTHORIZE" text="Autorizadas" />
              <SelectItem value="DENY" text="Recusadas" />
            </Select>
          </div>
        )}

        {isFlow && (
          <div className="analyst-flow-filters" aria-label="Filtros do fluxo atual">
            <Select
              id="flow-customer-filter"
              labelText="Associado"
              value={customerFilter}
              onChange={(event) => updateFlowQuery(event.target.value, statusFilter)}
            >
              <SelectItem value="" text="Todos os associados" />
              {(flowData?.customers ?? []).map((customer) => (
                <SelectItem
                  key={customer.customer_id}
                  value={customer.customer_id}
                  text={`${customer.display_name} (${customer.purchase_count})`}
                />
              ))}
            </Select>
            <Select
              id="flow-status-filter"
              labelText="Status da compra"
              value={statusFilter}
              onChange={(event) => updateFlowQuery(customerFilter, event.target.value)}
            >
              <SelectItem value="" text="Todos os status" />
              {FLOW_STATUS_OPTIONS.map(([value, label]) => (
                <SelectItem key={value} value={value} text={label} />
              ))}
            </Select>
          </div>
        )}

        {/* Estado: carregando */}
        {loading && (
          <div style={{ padding: '2rem' }} role="status" aria-live="polite">
            <InlineLoading description="Carregando revisões…" status="active" />
          </div>
        )}

        {/* Estado: erro */}
        {!loading && error && (
          <div style={{ padding: '2rem', maxWidth: '40rem' }}>
            <Stack gap={4}>
              <InlineNotification
                kind="error"
                title="Erro ao carregar revisões"
                subtitle={error}
                hideCloseButton
                lowContrast
              />
              <Button kind="secondary" size="sm" onClick={loadContent}>
                Tentar novamente
              </Button>
            </Stack>
          </div>
        )}

        {/* Estado: vazio */}
        {!isFlow && !isDashboard && !loading && !error && reviews !== null && reviews.length === 0 && (
          <div className="analyst-empty-state" role="status">
            <p className="cds--type-body-01">
              {isHistory ? 'Nenhuma revisão encerrada para este filtro.' : 'Não há revisões pendentes no momento.'}
            </p>
          </div>
        )}

        {/* Lista de revisões */}
        {!isFlow && !isDashboard && !loading && !error && reviews !== null && reviews.length > 0 && (
          <div className="analyst-reviews-list" role="list" aria-label="Revisões">
            {reviews.map((rev) => (
              <div key={rev.review_id} role="listitem">
                <ReviewCard
                  review={rev}
                  onOpen={(reviewId) => navigate(
                    `/analyst/reviews/${encodeURIComponent(reviewId)}`,
                    { state: { returnTo: `${location.pathname}${location.search}` } },
                  )}
                />
              </div>
            ))}
          </div>
        )}

        {isFlow && !loading && !error && flowData && (
          <AnalystFlow data={flowData} />
        )}

        {isDashboard && !loading && !error && dashboardData && (
          <AnalystDashboard data={dashboardData} />
        )}

        {!isFlow && !isDashboard && !loading && !error && pagination.totalPages > 1 && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginTop: '1rem' }}>
            <Button kind="ghost" size="sm" disabled={page <= 1} onClick={() => updateHistoryQuery(decisionFilter, page - 1)}>
              Anterior
            </Button>
            <span className="cds--type-label-01">
              Página {page} de {pagination.totalPages} · {pagination.total} registros
            </span>
            <Button
              kind="ghost"
              size="sm"
              disabled={page >= pagination.totalPages}
              onClick={() => updateHistoryQuery(decisionFilter, page + 1)}
            >
              Próxima
            </Button>
          </div>
        )}
      </main>
    </Theme>
  );
}
