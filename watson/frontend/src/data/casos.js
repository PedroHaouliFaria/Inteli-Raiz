// Dados fictícios, inspirados nos sinais do case de prevenção (rajada, distância, horário, valor, cartão não presente).
export const CASOS = [
  {
    id: '4821', associado: 'Valdir B.', cartao: '•••• 4821', valor: 2349.9, estabelecimento: 'Loja Exemplo Eletrônicos',
    canal: 'Não presente', score: 0.92, estado: 'novo', naFila: '4 min', alertas: 3,
    fatores: [
      { nome: 'Rajada: 3 compras em 7 min', peso: 0.31 },
      { nome: '640 km da região habitual (Chapecó, SC)', peso: 0.24 },
      { nome: 'Valor 6,2× a média do associado', peso: 0.18 },
      { nome: 'Horário atípico (03:14)', peso: 0.11 },
      { nome: 'Dispositivo novo', peso: 0.08 },
    ],
  },
  { id: '5107', associado: 'Marina S.', cartao: '•••• 4417', valor: 1249.9, estabelecimento: 'Mercado Online Exemplo', canal: 'Não presente', score: 0.88, estado: 'novo', naFila: '6 min', alertas: 1 },
  { id: '4990', associado: 'João P.', cartao: '•••• 1180', valor: 89.9, estabelecimento: 'Assinatura Exemplo', canal: 'Não presente', score: 0.81, estado: 'aguardando', naFila: '22 min', alertas: 4 },
  { id: '4875', associado: 'Ana L.', cartao: '•••• 3302', valor: 560.0, estabelecimento: 'Posto Exemplo', canal: 'Presente', score: 0.74, estado: 'analise', naFila: '9 min', alertas: 1 },
  { id: '4762', associado: 'Carlos M.', cartao: '•••• 7745', valor: 3120.0, estabelecimento: 'Agropecuária Exemplo', canal: 'Presente', score: 0.66, estado: 'aguardando', naFila: '25 min', alertas: 1 },
  { id: '4701', associado: 'Rita F.', cartao: '•••• 9031', valor: 45.5, estabelecimento: 'Farmácia Exemplo', canal: 'Presente', score: 0.41, estado: 'resolvido', naFila: '—', alertas: 1 },
];

export const ESTADOS = {
  novo: 'Novo · alto risco',
  aguardando: 'Aguardando associado',
  analise: 'Em análise',
  resolvido: 'Resolvido hoje',
};

export function nivelRisco(score) {
  if (score >= 0.8) return { texto: 'Alto', tipo: 'red' };
  if (score >= 0.6) return { texto: 'Médio', tipo: 'warm-gray' };
  return { texto: 'Baixo', tipo: 'cool-gray' };
}

export const brl = (v) => v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
