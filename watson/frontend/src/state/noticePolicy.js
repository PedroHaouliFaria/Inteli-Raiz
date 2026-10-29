// Política do aviso de compra (docs/arquitetura/decisoes/0004). Espelha a do backend até a tela ler da API.
// "Fui eu" fechar o caso sozinho e o prazo de resposta ainda aguardam o time, por isso vêm do ambiente.
const env = import.meta.env;

export const NOTICE_POLICY = {
  mediumThreshold: 0.6,
  highThreshold: 0.8,
  autoCloseOnItWasMe: (env.VITE_NOTICE_AUTO_CLOSE_ON_IT_WAS_ME ?? 'true') === 'true',
  responseTimeoutMinutes: Number(env.VITE_NOTICE_RESPONSE_TIMEOUT_MINUTES ?? 10),
};

// Risco médio: o Watson envia o aviso sozinho. Risco alto: vai direto para a analista.
export function initialHandling(score, policy = NOTICE_POLICY) {
  if (score >= policy.highThreshold) return 'route_to_analyst';
  if (score >= policy.mediumThreshold) return 'auto_send_notice';
  return 'no_action';
}
