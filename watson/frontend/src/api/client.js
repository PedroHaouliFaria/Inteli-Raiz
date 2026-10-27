// Cliente HTTP do backend do Watson (FastAPI). A URL base vem de VITE_API_URL.
// As telas ainda leem de mocks/; cada uma passa para a API quando o endpoint dela existir.
const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

export async function request(path, { method = 'GET', body, headers } = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    method,
    headers: { 'Content-Type': 'application/json', ...headers },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`${method} ${path} failed with ${response.status}: ${detail}`);
  }
  return response.status === 204 ? null : response.json();
}

export const getHealth = () => request('/health');
