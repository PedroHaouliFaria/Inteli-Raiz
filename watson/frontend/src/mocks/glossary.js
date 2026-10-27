// Fonte: docs/design/glossario.md (decisão do Leo, 26/10/2026)
export const GLOSSARY = {
  alert: {
    term: 'Alerta',
    definition: 'Transação que o modelo marcou como suspeita (score acima do limite). É gerado automaticamente, um por compra.',
    where: 'Fila, Quadro e Caso',
  },
  case: {
    term: 'Caso',
    definition: 'Unidade de trabalho da analista. Junta os alertas do mesmo cartão e guarda investigação, contato com o associado, decisão e justificativa. Ex.: 3 compras em rajada = 3 alertas, 1 caso.',
    where: 'Fila, Quadro e Caso',
  },
  score: {
    term: 'Score de risco',
    definition: 'Probabilidade estimada de fraude, de 0 a 1. Acima de 0,80 é alto risco.',
    where: 'Fila e Caso',
  },
  timeToDecision: {
    term: 'Tempo até a decisão',
    definition: 'Tempo médio entre o caso entrar na fila e a analista registrar a decisão (bloquear, liberar ou escalar). Medido pelo Watson a partir do registro de eventos do caso.',
    where: 'Indicadores da Fila',
  },
  awaitingMember: {
    term: 'Aguardando associado',
    definition: 'Enviamos um aviso de compra ao associado e esperamos a resposta no app.',
    where: 'Quadro e Caso',
  },
  confidence: {
    term: 'Confiança do agente',
    definition: 'Quanto o Watson confia na recomendação, com base na força e na concordância dos sinais. A decisão final é sempre da analista.',
    where: 'Painel do Watson',
  },
  purchaseNotice: {
    term: 'Aviso de compra',
    definition: 'Mensagem no app pedindo ao associado que confirme uma compra diferente do costume.',
    where: 'App do associado',
  },
};
