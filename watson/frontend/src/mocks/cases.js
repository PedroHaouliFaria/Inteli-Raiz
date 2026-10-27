// Dados fictícios, inspirados nos sinais do case de prevenção (rajada, distância, horário, valor, cartão não presente).
export const CASES = [
  {
    id: '4821', member: 'Valdir B.', card: '•••• 4821', amount: 2349.9, merchant: 'Loja Exemplo Eletrônicos',
    channel: 'Não presente', score: 0.92, status: 'new', waitTime: '4 min', alertCount: 3,
    factors: [
      { name: 'Rajada: 3 compras em 7 min', weight: 0.31 },
      { name: '640 km da região habitual (Chapecó, SC)', weight: 0.24 },
      { name: 'Valor 6,2× a média do associado', weight: 0.18 },
      { name: 'Horário atípico (03:14)', weight: 0.11 },
      { name: 'Dispositivo novo', weight: 0.08 },
    ],
  },
  { id: '5107', member: 'Marina S.', card: '•••• 4417', amount: 1249.9, merchant: 'Mercado Online Exemplo', channel: 'Não presente', score: 0.88, status: 'new', waitTime: '6 min', alertCount: 1 },
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

export const formatBRL = (v) => v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
