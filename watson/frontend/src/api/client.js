// Cliente HTTP do backend do Watson (FastAPI).
//
// Rotas /api usam URL relativa: em desenvolvimento o Vite faz proxy para
// http://localhost:8000; em produção o FastAPI serve o build estático. Isso
// mantém a mesma origem para o cookie raiz_session (SameSite=Lax).
//
// Rotas legadas /health e /model-lab ainda usam BASE_URL absoluto para não
// quebrar o build enquanto não migram.
const LEGACY_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

// Erro estruturado com os campos do envelope {"error":{"code","message","details"}}.
export class ApiError extends Error {
  constructor(status, code, message, details) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.code = code;
    this.details = details ?? null;
  }
}

// Requisição genérica para rotas /api (URL relativa, credenciais incluídas).
export async function request(path, { method = 'GET', body, headers } = {}) {
  const response = await fetch(path, {
    method,
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...headers },
    body: body === undefined ? undefined : JSON.stringify(body),
  });

  if (!response.ok) {
    let code = 'INTERNAL_ERROR';
    let message = `${method} ${path} falhou com status ${response.status}.`;
    let details = null;
    try {
      const payload = await response.json();
      if (payload?.error) {
        code = payload.error.code ?? code;
        message = payload.error.message ?? message;
        details = payload.error.details ?? null;
      }
    } catch {
      // Corpo não é JSON; usa defaults acima.
    }
    throw new ApiError(response.status, code, message, details);
  }

  return response.status === 204 ? null : response.json();
}

// Requisição legada para /health e /model-lab (URL absoluta, sem credenciais de sessão).
async function legacyRequest(path, options = {}) {
  const response = await fetch(`${LEGACY_BASE}${path}`, {
    method: options.method ?? 'GET',
    headers: { 'Content-Type': 'application/json', ...options.headers },
    body: options.body === undefined ? undefined : JSON.stringify(options.body),
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`${options.method ?? 'GET'} ${path} failed with ${response.status}: ${detail}`);
  }
  return response.status === 204 ? null : response.json();
}

// ── Funções legadas (health e model-lab) ────────────────────────────────────
export const getHealth = () => legacyRequest('/health');

export const getModelLabInfo = () => legacyRequest('/model-lab/info');
export const searchModelLabSamples = (q, label) =>
  legacyRequest(`/model-lab/samples?${new URLSearchParams({ q, limit: 20, ...(label ? { label } : {}) })}`);
export const getModelLabSample = (id) => legacyRequest(`/model-lab/samples/${encodeURIComponent(id)}`);
export const getRandomModelLabSample = (label) => legacyRequest(`/model-lab/samples/random?label=${label}`);
export const scoreTransaction = (features) => legacyRequest('/model-lab/score', { method: 'POST', body: { features } });

// ── Sessão (§4 do contrato) ──────────────────────────────────────────────────

/** GET /api/session/personas — público, lista personas disponíveis */
export const getPersonas = () => request('/api/session/personas');

/** POST /api/session — cria sessão; devolve SessionResponse */
export const login = (persona_id) => request('/api/session', { method: 'POST', body: { persona_id } });

/** GET /api/session — retorna sessão ativa ou lança ApiError 401 */
export const getSession = () => request('/api/session');

/** DELETE /api/session — encerra sessão (204) */
export const logout = () => request('/api/session', { method: 'DELETE' });

// ── Compras (§5 do contrato) ──────────────────────────────────────────────────

/** GET /api/purchases — lista compras do associado da sessão */
export const getPurchases = () => request('/api/purchases');

/** GET /api/purchases/{case_id} — detalhe completo de uma compra */
export const getPurchase = (caseId) => request(`/api/purchases/${encodeURIComponent(caseId)}`);

/** GET /api/purchases/{case_id}/status — status leve para polling */
export const getPurchaseStatus = (caseId) => request(`/api/purchases/${encodeURIComponent(caseId)}/status`);

// ── Chat (§7 do contrato) ────────────────────────────────────────────────────

/** GET /api/purchases/{case_id}/chat — histórico da conversa */
export const getChatHistory = (caseId) =>
  request(`/api/purchases/${encodeURIComponent(caseId)}/chat`);

/**
 * POST /api/purchases/{case_id}/chat — envia mensagem ao agente
 * @param {string} caseId
 * @param {string} message — 1 a 1000 caracteres
 */
export const postChatMessage = (caseId, message) =>
  request(`/api/purchases/${encodeURIComponent(caseId)}/chat`, {
    method: 'POST',
    body: { message },
  });

// ── Revisão (§8 do contrato) ──────────────────────────────────────────────────

/**
 * POST /api/purchases/{case_id}/review — associado solicita revisão humana
 * @param {string} caseId
 * @param {"NAO_RECONHECE_ESTABELECIMENTO"|"VALOR_DIFERENTE"|"DUVIDA_PROCESSO"|"OUTRO"} reason
 * @param {string|undefined} details — até 500 caracteres, opcional
 */
export const postReview = (caseId, reason, details) =>
  request(`/api/purchases/${encodeURIComponent(caseId)}/review`, {
    method: 'POST',
    body: { reason, ...(details ? { details } : {}) },
  });

/** GET /api/reviews — lista revisões abertas; requer sessão ANALISTA (§8 do contrato) */
export const getReviews = () => request('/api/reviews');

// ── Confirmação (§6 do contrato) ──────────────────────────────────────────────

/**
 * POST /api/confirmations/{challenge_id}/response
 *
 * @param {string} challengeId  — ex.: "CH-007"
 * @param {"AUTHORIZE"|"DENY"|"UNSURE"} response
 * @param {number} version      — versão exibida na tela
 * @param {string} idempotencyKey — UUID v4; manter a mesma para retry após erro de rede
 */
export const postConfirmationResponse = (challengeId, response, version, idempotencyKey) =>
  request(`/api/confirmations/${encodeURIComponent(challengeId)}/response`, {
    method: 'POST',
    body: { response, version },
    headers: { 'Idempotency-Key': idempotencyKey },
  });
