const API_BASE = process.env.VUE_APP_API_BASE_URL || 'http://localhost:3000'

export async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, { credentials: 'include', headers: { 'Content-Type': 'application/json', ...(options.headers || {}) }, ...options })
  const data = response.status === 204 ? null : await response.json().catch(() => null)
  if (!response.ok) { const error = new Error(data?.code || 'REQUEST_FAILED'); error.code = data?.code; throw error }
  return data
}
