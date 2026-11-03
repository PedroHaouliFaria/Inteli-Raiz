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
 * Ações de resolução/fechamento NÃO existem (contrato é somente leitura no v1).
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
  SkipToContent,
  Stack,
  Tag,
  Theme,
  Tile,
} from '@carbon/react';
import { Renew, Logout } from '@carbon/icons-react';
import { ApiError, getReviews, logout } from '../../api/client.js';
import { useSession } from '../session/SessionGate.jsx';
import { formatDate, formatMoney, statusMeta } from '../associate/utils.js';

// ── Rótulos legíveis para enums do contrato ─────────────────────────────────

const KIND_LABEL = {
  DUVIDA: 'Dúvida',
  PROTECAO: 'Proteção',
  FALHA_AVALIACAO: 'Falha na avaliação',
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

// ── Componente de um item de revisão ────────────────────────────────────────

function ReviewCard({ review }) {
  const caseMeta = statusMeta(review.case_status);
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
            <Tag size="sm" type={caseMeta.tagType}>{review.case_status}</Tag>
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
    </Tile>
  );
}

// ── Componente principal ─────────────────────────────────────────────────────

export default function AnalystApp() {
  const session = useSession();

  const [reviews, setReviews] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [loggingOut, setLoggingOut] = useState(false);

  const loadReviews = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getReviews();
      setReviews(data.reviews);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Erro de rede ao carregar revisões.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadReviews();
  }, [loadReviews]);

  const handleLogout = async () => {
    setLoggingOut(true);
    try {
      await logout();
    } catch {
      // Se o servidor falhar, recarrega a página para limpar o estado
    } finally {
      window.location.reload();
    }
  };

  return (
    <Theme theme="g10">
      {/* Cabeçalho */}
      <Theme theme="g100">
        <Header aria-label="Raiz · Revisões">
          <SkipToContent />
          <HeaderName href="#" prefix="Raiz">
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
              onClick={loadReviews}
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

      <main className="analyst-app" aria-label="Lista de revisões">
        {/* Cabeçalho da página */}
        <div className="analyst-page-header">
          <div>
            <h1 className="cds--type-heading-compact-02">Fila de revisões</h1>
            <p
              className="cds--type-label-01"
              style={{ color: 'var(--cds-text-helper)', marginTop: '0.25rem' }}
            >
              Simulação — Inteli Raiz · somente leitura no v1
            </p>
          </div>
          {/* Aviso de simulação visível */}
          <div className="analyst-simulation-badge" role="note" aria-label="Aviso de simulação">
            <span className="cds--type-label-01">
              ⚠ Dados simulados. Nenhuma ação real disponível nesta versão.
            </span>
          </div>
        </div>

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
              <Button kind="secondary" size="sm" onClick={loadReviews}>
                Tentar novamente
              </Button>
            </Stack>
          </div>
        )}

        {/* Estado: vazio */}
        {!loading && !error && reviews !== null && reviews.length === 0 && (
          <div className="analyst-empty-state" role="status">
            <p className="cds--type-body-01">Não há revisões no momento.</p>
          </div>
        )}

        {/* Lista de revisões */}
        {!loading && !error && reviews !== null && reviews.length > 0 && (
          <div className="analyst-reviews-list" role="list" aria-label="Revisões">
            {reviews.map((rev) => (
              <div key={rev.review_id} role="listitem">
                <ReviewCard review={rev} />
              </div>
            ))}
          </div>
        )}
      </main>
    </Theme>
  );
}
