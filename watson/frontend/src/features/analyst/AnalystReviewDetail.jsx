import { useCallback, useEffect, useState } from 'react';
import {
  Button,
  Header,
  HeaderGlobalAction,
  HeaderGlobalBar,
  HeaderName,
  InlineLoading,
  InlineNotification,
  SkipToContent,
  Stack,
  Tag,
  TextArea,
  Theme,
  Tile,
} from '@carbon/react';
import { ArrowLeft, Logout } from '@carbon/icons-react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { ApiError, getReview, postReviewDecision } from '../../api/client.js';
import { useSession } from '../session/SessionGate.jsx';
import { formatDate, formatMoney } from '../associate/utils.js';
import { PurchaseStatusBadge } from '../associate/PurchaseStatus.jsx';

const DECISION_LABEL = {
  AUTHORIZE: 'Autorizar compra',
  DENY: 'Recusar compra',
};

const RESPONSE_LABEL = {
  AUTHORIZE: 'Reconheceu e autorizou',
  DENY: 'Não reconheceu',
  UNSURE: 'Informou dúvida',
};

function Definition({ label, children }) {
  return (
    <div className="analyst-review-card__field">
      <dt className="cds--type-label-01 analyst-review-card__label">{label}</dt>
      <dd className="cds--type-body-compact-01">{children ?? 'Não informado'}</dd>
    </div>
  );
}

export default function AnalystReviewDetail() {
  const { reviewId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const session = useSession();
  const [review, setReview] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [notFound, setNotFound] = useState(false);
  const [pendingDecision, setPendingDecision] = useState(null);
  const [justification, setJustification] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [decisionError, setDecisionError] = useState(null);
  const [notice, setNotice] = useState(null);
  const [loggingOut, setLoggingOut] = useState(false);

  const loadReview = useCallback(async () => {
    setLoading(true);
    setError(null);
    setNotFound(false);
    try {
      const data = await getReview(reviewId);
      setReview(data);
    } catch (err) {
      if (err instanceof ApiError && err.status === 404) {
        setNotFound(true);
        setReview(null);
      } else {
        setError(err instanceof ApiError ? err.message : 'Erro de rede ao carregar a revisão.');
      }
    } finally {
      setLoading(false);
    }
  }, [reviewId]);

  useEffect(() => {
    loadReview();
  }, [loadReview]);

  const normalizedJustification = justification.trim();
  const justificationValid = normalizedJustification.length >= 10
    && normalizedJustification.length <= 500;

  const submitDecision = async () => {
    if (!pendingDecision || !justificationValid) return;
    setSubmitting(true);
    setDecisionError(null);
    try {
      const result = await postReviewDecision(
        reviewId,
        pendingDecision,
        normalizedJustification,
      );
      setNotice(result.message);
      setPendingDecision(null);
      setJustification('');
      await loadReview();
    } catch (err) {
      setDecisionError(
        err instanceof ApiError ? err.message : 'Erro de rede ao registrar a decisão.',
      );
    } finally {
      setSubmitting(false);
    }
  };

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
      <Theme theme="g100">
        <Header aria-label="Raiz · Detalhe da revisão">
          <SkipToContent />
          <HeaderName href="/analyst/reviews/open" prefix="Raiz">Revisões</HeaderName>
          <HeaderGlobalBar>
            <Tag size="sm" type="blue" style={{ marginRight: '0.5rem', alignSelf: 'center' }}>
              {session.display_name}
            </Tag>
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

      <main className="analyst-app" aria-label="Detalhe da revisão">
        <Button
          kind="ghost"
          size="sm"
          renderIcon={ArrowLeft}
          onClick={() => navigate(location.state?.returnTo ?? '/analyst/reviews/open')}
          style={{ marginBottom: '1rem' }}
        >
          Voltar para pendentes
        </Button>

        {loading && <InlineLoading description="Carregando revisão…" status="active" />}

        {!loading && notFound && (
          <InlineNotification
            kind="warning"
            title="Revisão não encontrada"
            subtitle="O registro solicitado não existe ou não está disponível."
            hideCloseButton
            lowContrast
          />
        )}

        {!loading && error && (
          <Stack gap={4}>
            <InlineNotification kind="error" title="Erro ao carregar revisão" subtitle={error} hideCloseButton lowContrast />
            <Button kind="secondary" size="sm" onClick={loadReview}>Tentar novamente</Button>
          </Stack>
        )}

        {!loading && review && (
          <Stack gap={6}>
            <div className="analyst-page-header">
              <div>
                <h1 className="cds--type-heading-04">{review.protocol}</h1>
                <p className="cds--type-body-01">Detalhe disponível antes da decisão.</p>
              </div>
              <Tag type={review.status === 'ABERTA' ? 'blue' : 'gray'}>
                {review.status === 'ABERTA' ? 'Pendente' : 'Encerrada'}
              </Tag>
            </div>

            {notice && (
              <InlineNotification kind="success" title="Decisão registrada" subtitle={notice} lowContrast />
            )}

            <Tile>
              <h2 className="cds--type-heading-compact-02">Revisão e compra</h2>
              <dl className="analyst-review-card__grid" style={{ marginTop: '1rem' }}>
                <Definition label="Associado">{review.purchase.customer_display_name}</Definition>
                <Definition label="Caso">{review.purchase.case_id}</Definition>
                <Definition label="Valor">{formatMoney(review.purchase.amount)}</Definition>
                <Definition label="Data da compra">{formatDate(review.purchase.occurred_at)}</Definition>
                <Definition label="Status da compra">
                  <PurchaseStatusBadge
                    status={review.purchase.status}
                    label={review.purchase.status_label}
                  />
                </Definition>
                <Definition label="Categoria">{review.purchase.merchant_category}</Definition>
                <Definition label="Canal">{review.purchase.channel_label}</Definition>
                <Definition label="Cartão">Final {review.purchase.card_last4}</Definition>
                <Definition label="Motivo da revisão">{review.reason}</Definition>
                <Definition label="Detalhes informados">{review.details}</Definition>
                <Definition label="Aberta em">{formatDate(review.created_at)}</Definition>
              </dl>
            </Tile>

            <Tile>
              <h2 className="cds--type-heading-compact-02">Informações para análise</h2>
              <p className="cds--type-label-01" style={{ marginTop: '1rem' }}>Sinais registrados</p>
              {review.signals.length > 0 ? (
                <ul style={{ margin: '0.5rem 0 0 1.25rem' }}>
                  {review.signals.map((signal) => <li key={signal.code}>{signal.label}</li>)}
                </ul>
              ) : <p className="cds--type-body-01">Nenhum sinal específico registrado.</p>}

              <dl className="analyst-review-card__grid" style={{ marginTop: '1rem' }}>
                <Definition label="Score interno do modelo">
                  {review.analysis.score === null ? 'Não disponível' : review.analysis.score.toFixed(4)}
                </Definition>
                <Definition label="Origem do score">{review.analysis.score_source}</Definition>
                <Definition label="Versão do modelo">{review.analysis.model_version}</Definition>
                <Definition label="Resposta do associado">
                  {review.associate_response
                    ? `${RESPONSE_LABEL[review.associate_response.response] ?? review.associate_response.response} · ${formatDate(review.associate_response.answered_at)}`
                    : 'Ainda não respondeu'}
                </Definition>
              </dl>
            </Tile>

            <Tile>
              <h2 className="cds--type-heading-compact-02">Linha do tempo de auditoria</h2>
              {review.timeline.length > 0 ? (
                <ol style={{ margin: '1rem 0 0 1.25rem' }}>
                  {review.timeline.map((event, index) => (
                    <li key={`${event.event_type}-${event.created_at}-${index}`} style={{ marginBottom: '0.75rem' }}>
                      <strong>{event.label}</strong>
                      <br />
                      <span className="cds--type-label-01">{formatDate(event.created_at)}</span>
                    </li>
                  ))}
                </ol>
              ) : <p className="cds--type-body-01">Nenhum evento disponível.</p>}
            </Tile>

            {review.status === 'ABERTA' ? (
              <Tile>
                <h2 className="cds--type-heading-compact-02">Registrar decisão</h2>
                {!pendingDecision ? (
                  <div className="analyst-review-card__actions" style={{ marginTop: '1rem' }}>
                    <Button onClick={() => setPendingDecision('AUTHORIZE')}>Autorizar compra</Button>
                    <Button kind="danger--tertiary" onClick={() => setPendingDecision('DENY')}>Recusar compra</Button>
                  </div>
                ) : (
                  <Stack gap={4} style={{ marginTop: '1rem', maxWidth: '40rem' }}>
                    <p className="cds--type-body-01">
                      Confirme: <strong>{DECISION_LABEL[pendingDecision]}</strong>.
                    </p>
                    <TextArea
                      id="review-justification"
                      labelText="Justificativa interna"
                      helperText={`${normalizedJustification.length}/500 caracteres; mínimo de 10.`}
                      value={justification}
                      onChange={(event) => setJustification(event.target.value)}
                      invalid={justification.length > 0 && !justificationValid}
                      invalidText="Informe uma justificativa entre 10 e 500 caracteres."
                      maxLength={500}
                      disabled={submitting}
                    />
                    {decisionError && (
                      <InlineNotification kind="error" title="Não foi possível registrar" subtitle={decisionError} hideCloseButton lowContrast />
                    )}
                    <div className="analyst-review-card__actions">
                      <Button
                        kind={pendingDecision === 'DENY' ? 'danger' : 'primary'}
                        disabled={!justificationValid || submitting}
                        onClick={submitDecision}
                      >
                        {submitting ? 'Registrando…' : DECISION_LABEL[pendingDecision]}
                      </Button>
                      <Button
                        kind="ghost"
                        disabled={submitting}
                        onClick={() => { setPendingDecision(null); setDecisionError(null); }}
                      >
                        Voltar
                      </Button>
                    </div>
                  </Stack>
                )}
              </Tile>
            ) : (
              <Tile>
                <h2 className="cds--type-heading-compact-02">Decisão registrada</h2>
                <dl className="analyst-review-card__grid" style={{ marginTop: '1rem' }}>
                  <Definition label="Decisão">{DECISION_LABEL[review.decision] ?? review.decision}</Definition>
                  <Definition label="Justificativa">{review.decision_reason}</Definition>
                  <Definition label="Responsável">{review.decided_by}</Definition>
                  <Definition label="Horário">{review.decided_at ? formatDate(review.decided_at) : null}</Definition>
                </dl>
              </Tile>
            )}
          </Stack>
        )}
      </main>
    </Theme>
  );
}
