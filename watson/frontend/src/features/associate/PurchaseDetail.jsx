/**
 * PurchaseDetail — detalhe completo de uma compra do associado.
 *
 * Responsabilidades:
 *   - Carregar o detalhe via GET /api/purchases/{case_id}
 *   - Fazer polling a cada 5 s enquanto status === AGUARDANDO_ASSOCIADO
 *   - Renderizar todos os campos do contrato §5 (exceto os proibidos)
 *   - Enviar resposta via POST /api/confirmations/{challenge_id}/response
 *   - Tratar todos os erros estruturados do contrato §6
 *
 * NÃO mostra: score, customer_id, card_id completo, renda, saldo, limite,
 * biometria, aparelho trocado, bloqueio de cartão ou decisão mockada.
 */
import { useEffect, useRef, useState, useCallback } from 'react';
import {
  Button,
  InlineLoading,
  InlineNotification,
  Stack,
} from '@carbon/react';
import { Warning, Information, CheckmarkFilled, CloseFilled, Time } from '@carbon/icons-react';
import { ApiError, getPurchase, getPurchaseStatus, postConfirmationResponse } from '../../api/client.js';
import { formatDate, formatMoney, isTerminal } from './utils.js';
import { PurchaseStatusPanel } from './PurchaseStatus.jsx';
import HumanReviewRequest from './HumanReviewRequest.jsx';

const POLL_INTERVAL_MS = 5000;
const STATUS_PANEL_REPLACES_RESULT = new Set([
  'LIBERADA_AUTOMATICAMENTE',
  'BLOQUEADA_PREVENTIVAMENTE',
]);

// ── Subcomponentes internos ───────────────────────────────────────────────────

function SimulationBadge() {
  return (
    <div className="associate-simulation-badge" role="note" aria-label="Aviso de simulação">
      <Information size={16} aria-hidden />
      <span className="cds--type-label-01">
        Esta é uma simulação. Os dados e ações desta tela são fictícios e não produzem efeito real.
      </span>
    </div>
  );
}

function PurchaseCard({ purchase }) {
  return (
    <section className="associate-purchase-summary" aria-label="Dados da compra">
        <div>
          <p className="cds--type-label-01 associate-purchase-summary__label">
            Estabelecimento
          </p>
          <p className="cds--type-heading-compact-02">{purchase.merchant_display}</p>
          {purchase.merchant_category && (
            <p className="cds--type-label-01" style={{ color: 'var(--cds-text-secondary)' }}>
              Categoria: {purchase.merchant_category.label}
            </p>
          )}
        </div>
        <div className="associate-purchase-grid">
          <div>
            <p className="cds--type-label-01" style={{ color: 'var(--cds-text-helper)' }}>Valor</p>
            <p className="cds--type-heading-03">{formatMoney(purchase.amount)}</p>
          </div>
          <div>
            <p className="cds--type-label-01" style={{ color: 'var(--cds-text-helper)' }}>Data e hora</p>
            <p className="cds--type-body-compact-01">{formatDate(purchase.occurred_at)}</p>
          </div>
          <div>
            <p className="cds--type-label-01" style={{ color: 'var(--cds-text-helper)' }}>Canal</p>
            <p className="cds--type-body-compact-01">{purchase.channel_label}</p>
          </div>
          <div>
            <p className="cds--type-label-01" style={{ color: 'var(--cds-text-helper)' }}>Cartão</p>
            <p className="cds--type-body-compact-01">
              {purchase.card.type} &bull;&bull;&bull;&bull;&nbsp;{purchase.card.last4}
            </p>
          </div>
        </div>
    </section>
  );
}

function AlertCard({ alert }) {
  if (!alert) return null;
  return (
    <section className="associate-detail-section associate-detail-section--alert" aria-labelledby="purchase-alert-title">
        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'flex-start' }}>
          <Warning size={20} aria-hidden style={{ flexShrink: 0, marginTop: '0.125rem', color: 'var(--cds-support-warning)' }} />
          <div>
            <h2 id="purchase-alert-title" className="cds--type-heading-compact-01">Por que pedimos sua atenção</h2>
            <p className="cds--type-body-01 associate-detail-section__lead">{alert.headline}</p>
          </div>
        </div>
        {alert.signals.length > 0 && (
          <ul className="associate-signals" aria-label="Motivos do alerta">
            {alert.signals.map((s) => (
              <li key={s.code} className="cds--type-body-01">
                <span aria-hidden>•</span> {s.label}
              </li>
            ))}
          </ul>
        )}
        <p className="cds--type-helper-text-01" style={{ color: 'var(--cds-text-helper)' }}>
          {alert.disclaimer}
        </p>
    </section>
  );
}

function ResultCard({ result }) {
  if (!result) return null;
  return (
    <section className="associate-detail-section" aria-label="Resultado da compra">
        <p className="cds--type-heading-compact-02">{result.title}</p>
        <p className="cds--type-body-01">{result.description}</p>
        {result.next_steps.length > 0 && (
          <ul className="associate-next-steps" aria-label="Próximos passos">
            {result.next_steps.map((step, i) => (
              // eslint-disable-next-line react/no-array-index-key
              <li key={i} className="cds--type-body-01">{step}</li>
            ))}
          </ul>
        )}
    </section>
  );
}

function ReviewCard({ review }) {
  if (!review) return null;
  return (
    <section className="associate-detail-section" aria-label="Revisão em andamento">
        <p className="cds--type-label-01" style={{ color: 'var(--cds-text-helper)' }}>
          Revisão em andamento
        </p>
        <p className="cds--type-body-compact-01">
          Protocolo: <strong>{review.protocol}</strong>
        </p>
        <p className="cds--type-label-01" style={{ color: 'var(--cds-text-secondary)' }}>
          {review.kind === 'PROTECAO' && 'Revisão de proteção aberta. O cartão não foi bloqueado.'}
          {review.kind === 'DUVIDA' && 'Revisão de dúvida aberta. Um analista vai revisar este caso.'}
          {review.kind === 'FALHA_AVALIACAO' && 'O sistema não conseguiu avaliar esta compra. Um analista vai revisar.'}
          {review.kind === 'RISCO_ALTO' && 'O reconhecimento foi encaminhado para validação por causa do risco alto.'}
        </p>
    </section>
  );
}

function ExpiryCountdown({ expiresAt }) {
  const [secondsLeft, setSecondsLeft] = useState(() => {
    if (!expiresAt) return null;
    return Math.max(0, Math.floor((new Date(expiresAt) - Date.now()) / 1000));
  });

  useEffect(() => {
    if (!expiresAt) return;
    const tick = () => {
      const s = Math.max(0, Math.floor((new Date(expiresAt) - Date.now()) / 1000));
      setSecondsLeft(s);
    };
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, [expiresAt]);

  if (secondsLeft === null) return null;

  const days = Math.floor(secondsLeft / 86400);
  const hours = Math.floor((secondsLeft % 86400) / 3600);
  const minutes = Math.floor((secondsLeft % 3600) / 60);
  const secs = secondsLeft % 60;
  const visualTime = days > 0
    ? `${days}d ${hours}h ${minutes}min`
    : hours > 0
      ? `${hours}h ${minutes}min`
      : `${minutes}m ${String(secs).padStart(2, '0')}s`;
  const accessibleTime = days > 0
    ? `${days} dias, ${hours} horas e ${minutes} minutos`
    : hours > 0
      ? `${hours} horas e ${minutes} minutos`
      : `${minutes} minutos e ${secs} segundos`;

  return (
    <div className="associate-expiry" role="timer" aria-live="off" aria-label={`Tempo restante: ${accessibleTime}`}>
      <Time size={16} aria-hidden />
      <span className="cds--type-label-01">
        {secondsLeft > 0
          ? `Prazo para responder: ${visualTime}`
          : 'Prazo encerrado'}
      </span>
    </div>
  );
}

// ── Botões de confirmação ──────────────────────────────────────────────────────

function ConfirmationButtons({ confirmation, onRespond, submitting }) {
  if (!confirmation || confirmation.allowed_responses.length === 0) return null;

  const kindMap = {
    AUTHORIZE: 'primary',
    DENY: 'danger--tertiary',
    UNSURE: 'tertiary',
  };

  const iconMap = {
    AUTHORIZE: CheckmarkFilled,
    DENY: CloseFilled,
    UNSURE: Warning,
  };

  return (
    <fieldset className="associate-confirmation-buttons" aria-label="Responda à compra">
      <legend className="cds--type-heading-compact-01" style={{ marginBottom: '1rem' }}>
        {confirmation.question}
      </legend>
      <div className="associate-buttons-row">
        {confirmation.allowed_responses.map(({ response, label }) => {
          const Icon = iconMap[response];
          return (
            <Button
              key={response}
              kind={kindMap[response] ?? 'secondary'}
              renderIcon={Icon}
              onClick={() => onRespond(response)}
              disabled={submitting}
              aria-disabled={submitting}
            >
              {label}
            </Button>
          );
        })}
      </div>
    </fieldset>
  );
}

// ── Componente principal ───────────────────────────────────────────────────────

export default function PurchaseDetail({ caseId, onPurchaseChanged }) {
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(null);

  // Estado do POST de confirmação
  const [submitting, setSubmitting] = useState(false);
  const [actionError, setActionError] = useState(null);
  const [actionResult, setActionResult] = useState(null);

  // Tentativa idempotente: { response, version, key }
  // Reutiliza key apenas se response e version forem iguais ao tentar de novo.
  // Erro de rede preserva a tentativa; sucesso e conflitos de estado limpam.
  const attemptRef = useRef(null);

  // Carrega o detalhe completo
  const loadDetail = useCallback(async () => {
    setLoadError(null);
    try {
      const data = await getPurchase(caseId);
      setDetail(data);
    } catch (err) {
      setLoadError(err instanceof ApiError ? err.message : 'Erro de rede ao carregar a compra.');
    } finally {
      setLoading(false);
    }
  }, [caseId]);

  // Monta e reseta ao trocar de compra
  useEffect(() => {
    setDetail(null);
    setLoading(true);
    setLoadError(null);
    setActionError(null);
    setActionResult(null);
    attemptRef.current = null;
    loadDetail();
  }, [caseId, loadDetail]);

  // Polling enquanto o associado ainda pode responder ou contestar.
  useEffect(() => {
    if (!detail) return;
    if (!['AGUARDANDO_ASSOCIADO', 'LIBERADA_AUTOMATICAMENTE', 'BLOQUEADA_PREVENTIVAMENTE'].includes(detail.status)) return;

    const id = setInterval(async () => {
      try {
        const statusData = await getPurchaseStatus(caseId);
        // Se version ou status mudou, recarrega o detalhe completo
        if (statusData.version !== detail.version || statusData.status !== detail.status) {
          await loadDetail();
          onPurchaseChanged?.();
        }
      } catch {
        // Erro de rede no polling: silencioso — a tela já mostra os dados
      }
    }, POLL_INTERVAL_MS);

    return () => clearInterval(id);
  }, [caseId, detail, loadDetail, onPurchaseChanged]);

  // Envia resposta à confirmação
  const handleRespond = async (response) => {
    if (!detail?.confirmation) return;
    const { challenge_id } = detail.confirmation;

    // Reutiliza key somente se response e version são idênticos à tentativa anterior
    const prev = attemptRef.current;
    if (!prev || prev.response !== response || prev.version !== detail.version) {
      attemptRef.current = { response, version: detail.version, key: crypto.randomUUID() };
    }

    setSubmitting(true);
    setActionError(null);
    setActionResult(null);

    try {
      const out = await postConfirmationResponse(
        challenge_id,
        response,
        detail.version,
        attemptRef.current.key,
      );
      // Sucesso: limpa a tentativa, mostra resultado, recarrega detalhe, notifica pai
      attemptRef.current = null;
      setActionResult(out.result);
      await loadDetail();
      onPurchaseChanged?.();
    } catch (err) {
      if (err instanceof ApiError) {
        const retriable = ['VERSION_MISMATCH', 'ALREADY_ANSWERED', 'NOT_AWAITING_RESPONSE', 'CONFIRMATION_EXPIRED'].includes(err.code);
        if (retriable) {
          // Estado desatualizado: recarregar e mostrar mensagem estruturada
          attemptRef.current = null;
          setActionError(err.message);
          await loadDetail();
        } else if (err.code === 'IDEMPOTENCY_KEY_REUSED') {
          // Chave reusada com corpo diferente: gera nova no próximo clique
          attemptRef.current = null;
          setActionError(err.message);
        } else {
          // Erro de rede ou interno: mantém a tentativa para retry
          setActionError(err.message);
        }
      } else {
        // Erro de rede puro: mantém a tentativa para retry
        setActionError('Erro de rede. Tente novamente. Sua resposta anterior será preservada se você reenviar.');
      }
    } finally {
      setSubmitting(false);
    }
  };

  // ── Render ────────────────────────────────────────────────────────────────

  if (loading) {
    return (
      <div className="associate-detail-loading" role="status" aria-live="polite">
        <InlineLoading description="Carregando compra…" status="active" />
      </div>
    );
  }

  if (loadError) {
    return (
      <div className="associate-detail-error">
        <InlineNotification
          kind="error"
          title="Erro ao carregar compra"
          subtitle={loadError}
          hideCloseButton
          lowContrast
        />
        <Button kind="secondary" size="sm" onClick={loadDetail} style={{ marginTop: '1rem' }}>
          Tentar novamente
        </Button>
      </div>
    );
  }

  if (!detail) return null;

  const isWaiting = detail.status === 'AGUARDANDO_ASSOCIADO';

  return (
    <section className="associate-detail" aria-label={`Detalhe da compra ${detail.case_id}`}>
      <Stack gap={5}>
        <SimulationBadge />

        <div className="associate-detail__hero">
          <p className="cds--type-label-01 associate-detail__case-id">Compra {detail.case_id}</p>
          <PurchaseStatusPanel
            status={detail.status}
            label={detail.status_label}
            aside={isWaiting && detail.confirmation?.expires_at
              ? <ExpiryCountdown expiresAt={detail.confirmation.expires_at} />
              : null}
          />
          <PurchaseCard purchase={detail.purchase} />
        </div>

        <AlertCard alert={detail.alert} />

        {detail.review && <ReviewCard review={detail.review} />}

        {actionResult && !detail.result && (
          <ResultCard result={actionResult} />
        )}

        {detail.result && !STATUS_PANEL_REPLACES_RESULT.has(detail.status) && (
          <ResultCard result={detail.result} />
        )}

        {actionError && (
          <InlineNotification
            kind="warning"
            title="Atenção"
            subtitle={actionError}
            hideCloseButton
            lowContrast
            onClose={() => setActionError(null)}
          />
        )}

        {submitting && (
          <InlineLoading description="Enviando sua resposta…" status="active" />
        )}

        {/* ── Botões de confirmação ─────────────────────────────────────────── */}
        <ConfirmationButtons
          confirmation={detail.confirmation}
          onRespond={handleRespond}
          submitting={submitting}
        />

        {detail.confirmation?.allowed_responses.length === 0 && detail.confirmation?.answered && (
          <section className="associate-detail-section">
            <p className="cds--type-label-01" style={{ color: 'var(--cds-text-helper)', marginBottom: '0.25rem' }}>
              Resposta registrada em
            </p>
            <p className="cds--type-body-compact-01">{formatDate(detail.confirmation.answered.answered_at)}</p>
          </section>
        )}

        {/* ── Separador visual ─────────────────────────────────────────────── */}
        <hr className="associate-detail__divider" aria-hidden />

        {/* ── Revisão por analista ─────────────────────────────────────────── */}
        <HumanReviewRequest
          caseId={caseId}
          onSuccess={() => {
            loadDetail();
            onPurchaseChanged?.();
          }}
        />
      </Stack>
    </section>
  );
}
