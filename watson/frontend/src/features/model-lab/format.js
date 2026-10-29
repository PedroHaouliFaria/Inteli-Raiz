// Formatação dos valores do Laboratório do modelo, sempre em pt-BR.

export const BANDS = {
  low: { label: 'Baixo risco', short: 'Baixo', tag: 'green' },
  medium: { label: 'Médio risco', short: 'Médio', tag: 'warm-gray' },
  high: { label: 'Alto risco', short: 'Alto', tag: 'red' },
};

export const formatScore = (score) =>
  score.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

export const formatDelta = (delta) => `${delta >= 0 ? '+' : '−'}${formatScore(Math.abs(delta))}`;

export function formatValue(feature, value) {
  if (value === null || value === undefined) return 'vazio';
  if (feature.kind === 'binary') return value ? 'Sim' : 'Não';
  if (feature.kind === 'categorical') return value === 'nan' ? 'vazio' : String(value).replaceAll('_', ' ');
  return Number(value).toLocaleString('pt-BR', { maximumFractionDigits: 2 });
}

export const formatTime = (date) => date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
