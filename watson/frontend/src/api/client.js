// Cliente HTTP do backend do Watson (FastAPI). A URL base vem de VITE_API_URL.
// As telas ainda leem de mocks/; cada uma passa para a API quando o endpoint dela existir.
const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

/**
 * Erro retornado pela API: carrega o status HTTP, o code do envelope de erro (§2) e a
 * mensagem legível. Se o corpo não for o envelope esperado, code fica null.
 */
export class ApiError extends Error {
  /**
   * @param {number} status  - Código HTTP (ex.: 401, 404, 409)
   * @param {string|null} code  - Valor de error.code do envelope (ex.: 'NOT_AUTHENTICATED')
   * @param {string} message - Mensagem legível para o usuário
   */
  constructor(status, code, message) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.code = code;
  }
}

export async function request(path, { method = 'GET', body, headers } = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    method,
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...headers },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  if (!response.ok) {
    let code = null;
    let message;
    try {
      const payload = await response.json();
      code = payload?.error?.code ?? null;
      message = payload?.error?.message ?? response.statusText;
    } catch {
      message = await response.text().catch(() => response.statusText);
    }
    throw new ApiError(response.status, code, message);
  }
  return response.status === 204 ? null : response.json();
}

export const getHealth = () => request('/health');

// Laboratório do modelo (ambiente experimental do modelo de risco)
export const getModelLabInfo = () => request('/model-lab/info');
export const searchModelLabSamples = (q, label) =>
  request(`/model-lab/samples?${new URLSearchParams({ q, limit: 20, ...(label ? { label } : {}) })}`);
export const getModelLabSample = (id) => request(`/model-lab/samples/${encodeURIComponent(id)}`);
export const getRandomModelLabSample = (label) => request(`/model-lab/samples/random?label=${label}`);
export const scoreTransaction = (features) => request('/model-lab/score', { method: 'POST', body: { features } });

// §4 — Sessão

/** Lista as personas fictícias disponíveis para login. */
export const getPersonas = () => request('/api/session/personas');

/** Retorna a sessão ativa ou lança ApiError 401 NOT_AUTHENTICATED se não há sessão. */
export const getSession = () => request('/api/session');

/**
 * Cria uma sessão para a persona informada.
 * @param {string} personaId  - Ex.: 'ana', 'bruno', 'carla'
 */
export const login = (personaId) =>
  request('/api/session', { method: 'POST', body: { persona_id: personaId } });

/** Encerra a sessão (apaga o cookie). Retorna null (204). */
export const logout = () => request('/api/session', { method: 'DELETE' });

// §5 — Compras

/** Lista as compras do associado da sessão, da mais recente para a mais antiga. */
export const getPurchases = () => request('/api/purchases');

/**
 * Detalhes completos de uma compra (alerta, confirmação, resultado etc.).
 * @param {string} caseId  - Ex.: 'T-007'
 */
export const getPurchase = (caseId) => request(`/api/purchases/${encodeURIComponent(caseId)}`);

/**
 * Versão leve para atualizar o status sem recarregar o detalhe completo.
 * @param {string} caseId  - Ex.: 'T-007'
 */
export const getPurchaseStatus = (caseId) =>
  request(`/api/purchases/${encodeURIComponent(caseId)}/status`);

// §6 — Resposta à confirmação

/**
 * Registra a resposta do associado a uma confirmação de compra.
 * A chave de idempotência deve ser um UUID v4 gerado pelo front a cada clique novo.
 *
 * @param {string} challengeId     - Ex.: 'CH-007'
 * @param {'AUTHORIZE'|'DENY'|'UNSURE'} response - Resposta do associado
 * @param {string} idempotencyKey  - UUID v4 único por clique
 * @param {number} version         - Versão atual da compra exibida na tela
 */
export const respondToConfirmation = (challengeId, response, idempotencyKey, version) =>
  request(`/api/confirmations/${encodeURIComponent(challengeId)}/response`, {
    method: 'POST',
    headers: { 'Idempotency-Key': idempotencyKey },
    body: { response, version },
  });

// §7 — Chat com o agente

/**
 * Histórico da conversa ligada a uma compra.
 * @param {string} caseId  - Ex.: 'T-007'
 */
export const getChat = (caseId) => request(`/api/purchases/${encodeURIComponent(caseId)}/chat`);

/**
 * Envia uma mensagem do associado para o agente e devolve a resposta.
 * @param {string} caseId  - Ex.: 'T-007'
 * @param {string} text    - Texto de 1 a 1.000 caracteres, sem HTML
 */
export const sendChatMessage = (caseId, text) =>
  request(`/api/purchases/${encodeURIComponent(caseId)}/chat`, {
    method: 'POST',
    body: { message: text },
  });
