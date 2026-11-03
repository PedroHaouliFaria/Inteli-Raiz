/**
 * utils.js — funções de formatação e metadados de status compartilhados pelo fluxo do associado.
 * Sem dependências externas: só o runtime do browser.
 */

/** Formata um objeto Money {value, currency} para pt-BR. */
export function formatMoney({ value, currency }) {
  try {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency }).format(Number(value));
  } catch {
    return `${currency} ${value}`;
  }
}

/**
 * Formata uma string ISO 8601 UTC para data e hora no fuso do browser.
 * Exemplo: "2026-10-25T06:12:00Z" → "25/10/2026 às 03:12" (BRT)
 */
export function formatDate(iso) {
  if (!iso) return '—';
  try {
    return new Intl.DateTimeFormat('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(new Date(iso));
  } catch {
    return iso;
  }
}

/** Metadados visuais por status (rótulos e tipo de tag Carbon). */
const STATUS_META = {
  RECEBIDA:              { tagType: 'gray',    terminal: false },
  EM_AVALIACAO:          { tagType: 'blue',    terminal: false },
  AGUARDANDO_ASSOCIADO:  { tagType: 'magenta', terminal: false },
  LIBERADA_SIMULACAO:    { tagType: 'green',   terminal: true  },
  RECUSADA_SIMULACAO:    { tagType: 'red',     terminal: true  },
  REVISAO_PENDENTE:      { tagType: 'warm-gray', terminal: true },
  CONFIRMACAO_EXPIRADA:  { tagType: 'cool-gray', terminal: true },
};

export function statusMeta(status) {
  return STATUS_META[status] ?? { tagType: 'gray', terminal: false };
}

export function isTerminal(status) {
  return statusMeta(status).terminal;
}
