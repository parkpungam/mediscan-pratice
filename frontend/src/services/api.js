const API_BASE = process.env.VUE_APP_API_BASE_URL || 'http://localhost:3000'
let unauthorizedHandler = null
export function setUnauthorizedHandler(handler) { unauthorizedHandler = handler }
export async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, { credentials: 'include', headers: { 'Content-Type': 'application/json', ...(options.headers || {}) }, ...options })
  const data = response.status === 204 ? null : await response.json().catch(() => null)
  if (!response.ok) {
    const error = new Error(data?.code || 'REQUEST_FAILED'); error.code = data?.code; error.status = response.status; error.retryAfter = Number(response.headers.get('Retry-After') || 0)
    if (response.status === 401 && error.code === 'UNAUTHENTICATED' && !['/login', '/signup'].includes(window.location.pathname)) unauthorizedHandler?.()
    throw error
  }
  return data
}