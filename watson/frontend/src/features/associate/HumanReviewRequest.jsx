/**
 * HumanReviewRequest — ação "Prefiro falar com uma pessoa".
 *
 * Responsabilidades:
 *   - Usa POST /api/purchases/{case_id}/review
 *   - Permite escolher reason entre NAO_RECONHECE_ESTABELECIMENTO, VALOR_DIFERENTE,
 *     DUVIDA_PROCESSO, OUTRO, com campo details opcional
 *   - Mostra protocolo/mensagem retornados pelo backend
 *   - Não muda o estado local da compra (callback onSuccess para pai recarregar)
 *   - Não esconde nem desabilita os botões AUTHORIZE/DENY/UNSURE
 *   - Não expõe score nem IDs internos desnecessários
 */
import { useState } from 'react';
import {
  Button,
  InlineLoading,
  InlineNotification,
  RadioButton,
  RadioButtonGroup,
  Stack,
  TextArea,
  Tile,
} from '@carbon/react';
import { UserMultiple } from '@carbon/icons-react';
import { ApiError, postReview } from '../../api/client.js';

const REASONS = [
  { value: 'NAO_RECONHECE_ESTABELECIMENTO', label: 'Não reconheço o estabelecimento' },
  { value: 'VALOR_DIFERENTE',               label: 'O valor está diferente' },
  { value: 'DUVIDA_PROCESSO',               label: 'Tenho dúvida sobre o processo' },
  { value: 'OUTRO',                         label: 'Outro motivo' },
];

const MAX_DETAILS = 500;

export default function HumanReviewRequest({ caseId, onSuccess }) {
  const [open, setOpen] = useState(false);
  const [reason, setReason] = useState('');
  const [details, setDetails] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState(null);
  const [result, setResult] = useState(null); // sucesso: objeto com protocol/message

  const handleOpen = () => {
    setOpen(true);
    setSubmitError(null);
    setResult(null);
  };

  const handleCancel = () => {
    setOpen(false);
    setReason('');
    setDetails('');
    setSubmitError(null);
  };

  const handleSubmit = async () => {
    if (!reason || submitting) return;

    setSubmitting(true);
    setSubmitError(null);

    try {
      const data = await postReview(caseId, reason, details.trim() || undefined);
      setResult(data);
      setOpen(false);
      setReason('');
      setDetails('');
      // Notifica o pai para atualizar detalhe e lista
      onSuccess?.();
    } catch (err) {
      setSubmitError(err instanceof ApiError ? err.message : 'Erro de rede. Tente novamente.');
    } finally {
      setSubmitting(false);
    }
  };

  // ── Render ────────────────────────────────────────────────────────────────

  return (
    <section className="human-review" aria-label="Pedir revisão por analista">
      <Tile>
        <Stack gap={4}>
          <div className="human-review__header">
            <UserMultiple size={20} aria-hidden />
            <h2 className="cds--type-heading-compact-01">Prefiro falar com uma pessoa</h2>
          </div>

          <p className="cds--type-body-01" style={{ color: 'var(--cds-text-secondary)' }}>
            Um analista pode revisar esta compra. Enquanto aguarda, você ainda pode responder
            na seção de confirmação.
          </p>

          {/* Resultado de revisão já criada */}
          {result && (
            <InlineNotification
              kind="success"
              title="Revisão solicitada"
              subtitle={
                <>
                  Protocolo: <strong>{result.protocol}</strong>
                  {result.message ? ` — ${result.message}` : ''}
                </>
              }
              hideCloseButton
              lowContrast
            />
          )}

          {/* Botão para abrir formulário (apenas quando ainda não enviou ou fechou) */}
          {!open && !result && (
            <Button kind="tertiary" size="sm" renderIcon={UserMultiple} onClick={handleOpen}>
              Solicitar revisão por analista
            </Button>
          )}

          {/* Botão para abrir novamente após sucesso (caso queira ver o protocolo de novo) */}
          {!open && result && (
            <Button kind="ghost" size="sm" onClick={handleOpen}>
              Enviar outra solicitação
            </Button>
          )}

          {/* Formulário */}
          {open && (
            <Stack gap={4}>
              <RadioButtonGroup
                legendText="Qual é o motivo da sua dúvida?"
                name={`review-reason-${caseId}`}
                valueSelected={reason}
                onChange={(val) => setReason(val)}
                orientation="vertical"
              >
                {REASONS.map(({ value, label }) => (
                  <RadioButton key={value} labelText={label} value={value} id={`reason-${caseId}-${value}`} />
                ))}
              </RadioButtonGroup>

              <TextArea
                id={`review-details-${caseId}`}
                labelText="Detalhes adicionais (opcional)"
                placeholder="Descreva melhor sua dúvida se quiser (máx. 500 caracteres)"
                value={details}
                onChange={(e) => setDetails(e.target.value)}
                maxCount={MAX_DETAILS}
                enableCounter
                rows={3}
                disabled={submitting}
              />

              {submitError && (
                <InlineNotification
                  kind="error"
                  title="Erro ao solicitar revisão"
                  subtitle={submitError}
                  hideCloseButton
                  lowContrast
                />
              )}

              {submitting && (
                <InlineLoading description="Enviando solicitação…" status="active" />
              )}

              <div className="human-review__actions">
                <Button
                  kind="primary"
                  size="sm"
                  onClick={handleSubmit}
                  disabled={!reason || submitting || details.length > MAX_DETAILS}
                >
                  Confirmar solicitação
                </Button>
                <Button
                  kind="ghost"
                  size="sm"
                  onClick={handleCancel}
                  disabled={submitting}
                >
                  Cancelar
                </Button>
              </div>
            </Stack>
          )}
        </Stack>
      </Tile>
    </section>
  );
}
