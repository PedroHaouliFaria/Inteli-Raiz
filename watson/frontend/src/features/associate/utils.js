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

/** Metadados visuais e de orientação por status. */
const STATUS_META = {
  RECEBIDA: {
    tagType: 'gray', tone: 'neutral', icon: 'info', shortLabel: 'Recebida', terminal: false,
    description: 'A compra foi recebida e será avaliada.', nextStep: 'aguarde a avaliação',
  },
  EM_AVALIACAO: {
    tagType: 'blue', tone: 'info', icon: 'time', shortLabel: 'Em avaliação', terminal: false,
    description: 'O modelo está avaliando os sinais disponíveis.', nextStep: 'aguarde o resultado',
  },
  AGUARDANDO_ASSOCIADO: {
    tagType: 'magenta', tone: 'attention', icon: 'time', shortLabel: 'Responder', terminal: false,
    description: 'Precisamos saber se você reconhece esta compra.', nextStep: 'responda antes do prazo',
  },
  LIBERADA_AUTOMATICAMENTE: {
    tagType: 'green', tone: 'success', icon: 'check', shortLabel: 'Liberada automática', terminal: false,
    description: 'A compra foi liberada automaticamente por apresentar baixo risco.',
    nextStep: 'conteste caso não reconheça',
  },
  BLOQUEADA_PREVENTIVAMENTE: {
    tagType: 'red', tone: 'danger', icon: 'warning', shortLabel: 'Bloqueada', terminal: false,
    description: 'A compra foi bloqueada preventivamente por apresentar risco alto.',
    nextStep: 'informe se reconhece a compra',
  },
  CONTESTACAO_ABERTA: {
    tagType: 'purple', tone: 'review', icon: 'warning', shortLabel: 'Contestação aberta', terminal: true,
    description: 'Você informou que não reconhece a compra. A analista fará a decisão final.',
    nextStep: 'acompanhe a análise',
  },
  LIBERADA_SIMULACAO: {
    tagType: 'green', tone: 'success', icon: 'check', shortLabel: 'Liberada', terminal: true,
    description: 'A compra foi liberada na simulação.', nextStep: null,
  },
  RECUSADA_SIMULACAO: {
    tagType: 'red', tone: 'danger', icon: 'close', shortLabel: 'Recusada', terminal: true,
    description: 'A compra foi recusada após a análise.', nextStep: null,
  },
  REVISAO_PENDENTE: {
    tagType: 'warm-gray', tone: 'review', icon: 'time', shortLabel: 'Em revisão', terminal: true,
    description: 'A compra está aguardando a decisão de uma analista.', nextStep: 'acompanhe a análise',
  },
  CONFIRMACAO_EXPIRADA: {
    tagType: 'cool-gray', tone: 'neutral', icon: 'time', shortLabel: 'Prazo encerrado', terminal: true,
    description: 'O prazo de confirmação terminou e a compra não foi autorizada.',
    nextStep: 'solicite revisão se reconhecer a compra',
  },
};

export function statusMeta(status) {
  return STATUS_META[status] ?? {
    tagType: 'gray', tone: 'neutral', icon: 'info', shortLabel: status,
    description: 'Consulte os detalhes desta compra.', nextStep: null, terminal: false,
  };
}

export function isTerminal(status) {
  return statusMeta(status).terminal;
}
