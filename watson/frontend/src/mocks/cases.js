// Dados fictícios, inspirados nos sinais do case de prevenção (rajada, distância, horário, valor, cartão não presente).
// Linha do tempo (docs/dados/linha-do-tempo.md): no case a rajada só existe como contador (velocity1h, de
// cp_card_term_vel_1h), então cardHistory traz as compras reais do cartão e, quando velocity1h ≥ 10, até 5
// tentativas simuladas (simulated: true) nos 15 min antes da compra, com valor de 0,3 a 1,5× o real.
export const CASES = [
  {
    id: '4821', member: 'Valdir B.', card: '•••• 4821', amount: 2349.9, merchant: 'Loja Exemplo Eletrônicos',
    channel: 'Não presente', score: 0.92, status: 'new', waitTime: '4 min', alertCount: 3,
    factors: [
      { name: 'Rajada: 47 tentativas no terminal na última hora', weight: 0.31 },
      { name: '640 km da região habitual (Chapecó, SC)', weight: 0.24 },
      { name: 'Valor 6,2× a média do associado', weight: 0.18 },
      { name: 'Horário atípico (03:14)', weight: 0.11 },
      { name: 'Dispositivo novo', weight: 0.08 },
    ],
    velocity1h: 47,
    cardHistory: [
      { id: 't-7710', occurredAt: '2025-07-14T18:42', amount: 412.3, merchant: 'Supermercado Exemplo', city: 'Chapecó, SC', channel: 'Presente', status: 'approved' },
      { id: 't-8034', occurredAt: '2025-08-30T11:05', amount: 356.0, merchant: 'Agropecuária Exemplo', city: 'Chapecó, SC', channel: 'Presente', status: 'approved' },
      { id: 's-1', occurredAt: '2025-09-26T03:00', amount: 1880.0, merchant: 'Loja Exemplo Eletrônicos', city: 'São Paulo, SP', channel: 'Não presente', status: 'declined', simulated: true },
      { id: 's-2', occurredAt: '2025-09-26T03:03', amount: 3249.9, merchant: 'Loja Exemplo Eletrônicos', city: 'São Paulo, SP', channel: 'Não presente', status: 'declined', simulated: true },
      { id: 's-3', occurredAt: '2025-09-26T03:06', amount: 979.0, merchant: 'Loja Exemplo Eletrônicos', city: 'São Paulo, SP', channel: 'Não presente', status: 'held', simulated: true },
      { id: 's-4', occurredAt: '2025-09-26T03:09', amount: 2899.0, merchant: 'Loja Exemplo Eletrônicos', city: 'São Paulo, SP', channel: 'Não presente', status: 'declined', simulated: true },
      { id: 's-5', occurredAt: '2025-09-26T03:12', amount: 1349.9, merchant: 'Loja Exemplo Eletrônicos', city: 'São Paulo, SP', channel: 'Não presente', status: 'held', simulated: true },
      { id: 't-9121', occurredAt: '2025-09-26T03:14', amount: 2349.9, merchant: 'Loja Exemplo Eletrônicos', city: 'São Paulo, SP', channel: 'Não presente', status: 'held', current: true },
    ],
  },
  {
    id: '5107', member: 'Marina S.', card: '•••• 4417', amount: 1249.9, merchant: 'Mercado Online Exemplo', channel: 'Não presente', score: 0.88, status: 'new', waitTime: '6 min', alertCount: 1,
    velocity1h: 3,
    cardHistory: [
      { id: 't-9204', occurredAt: '2025-09-26T02:51', amount: 1249.9, merchant: 'Mercado Online Exemplo', city: 'Porto Alegre, RS', channel: 'Não presente', status: 'held', current: true },
    ],
  },
  { id: '4990', member: 'João P.', card: '•••• 1180', amount: 89.9, merchant: 'Assinatura Exemplo', channel: 'Não presente', score: 0.81, status: 'awaiting_member', waitTime: '22 min', alertCount: 4 },
  { id: '4875', member: 'Ana L.', card: '•••• 3302', amount: 560.0, merchant: 'Posto Exemplo', channel: 'Presente', score: 0.74, status: 'in_review', waitTime: '9 min', alertCount: 1 },
  { id: '4762', member: 'Carlos M.', card: '•••• 7745', amount: 3120.0, merchant: 'Agropecuária Exemplo', channel: 'Presente', score: 0.66, status: 'awaiting_member', waitTime: '25 min', alertCount: 1 },
  { id: '4701', member: 'Rita F.', card: '•••• 9031', amount: 45.5, merchant: 'Farmácia Exemplo', channel: 'Presente', score: 0.41, status: 'resolved', waitTime: '—', alertCount: 1 },
];

export const STATUS_LABELS = {
  new: 'Novo · alto risco',
  awaiting_member: 'Aguardando associado',
  in_review: 'Em análise',
  resolved: 'Resolvido hoje',
};

// Por que o caso está com a analista (escalation_reason no modelo de dados).
export const ESCALATION_LABELS = {
  high_risk: 'Alto risco',
  device_changed: 'Aparelho trocado',
  confirmation_review: 'Confirmação para conferir',
  not_recognized: 'Não reconheço',
  no_response: 'Sem resposta',
  talk_to_person: 'Pediu atendimento',
};

export function riskLevel(score) {
  if (score >= 0.8) return { label: 'Alto', tagType: 'red' };
  if (score >= 0.6) return { label: 'Médio', tagType: 'warm-gray' };
  return { label: 'Baixo', tagType: 'cool-gray' };
}

export const TRANSACTION_STATUS = {
  approved: { label: 'Aprovada', tagType: 'green' },
  held: { label: 'Retida', tagType: 'warm-gray' },
  declined: { label: 'Recusada', tagType: 'red' },
};

export const formatBRL = (v) => v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
