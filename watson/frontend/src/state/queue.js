// Casos que precisam da analista, ordenados por risco × valor.
// Os de risco médio com aviso automático aguardando o associado ficam com o Watson e saem da fila.
export function isWithWatson(c) {
  return c.autoNotice && c.status === 'awaiting_member';
}

export function analystQueue(cases) {
  return cases
    .filter((c) => c.status !== 'resolved' && !isWithWatson(c))
    .sort((a, b) => b.score * b.amount - a.score * a.amount);
}
