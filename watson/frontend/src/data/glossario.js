// Fonte: watson/design/glossario.md (decisão do Leo, 26/10/2026)
export const GLOSSARIO = {
  alerta: {
    termo: 'Alerta',
    definicao: 'Transação que o modelo marcou como suspeita (score acima do limite). É gerado automaticamente, um por compra.',
    onde: 'Fila, Quadro e Caso',
  },
  caso: {
    termo: 'Caso',
    definicao: 'Unidade de trabalho da analista. Junta os alertas do mesmo cartão e guarda investigação, contato com o associado, decisão e justificativa. Ex.: 3 compras em rajada = 3 alertas, 1 caso.',
    onde: 'Fila, Quadro e Caso',
  },
  score: {
    termo: 'Score de risco',
    definicao: 'Probabilidade estimada de fraude, de 0 a 1. Acima de 0,80 é alto risco.',
    onde: 'Fila e Caso',
  },
  tempoDecisao: {
    termo: 'Tempo até a decisão',
    definicao: 'Tempo médio entre o caso entrar na fila e a analista registrar a decisão (bloquear, liberar ou escalar). Medido pelo Watson a partir do registro de eventos do caso.',
    onde: 'Indicadores da Fila',
  },
  aguardandoAssociado: {
    termo: 'Aguardando associado',
    definicao: 'Enviamos um aviso de compra ao associado e esperamos a resposta no app.',
    onde: 'Quadro e Caso',
  },
  confianca: {
    termo: 'Confiança do agente',
    definicao: 'Quanto o Watson confia na recomendação, com base na força e na concordância dos sinais. A decisão final é sempre da analista.',
    onde: 'Painel do Watson',
  },
  avisoCompra: {
    termo: 'Aviso de compra',
    definicao: 'Mensagem no app pedindo ao associado que confirme uma compra diferente do costume.',
    onde: 'App do associado',
  },
};
