// Dynamic API Base URL resolution for local and production/live deployment
export const API_BASE_URL =
  typeof window !== 'undefined' && window.location.port === '5173'
    ? 'http://localhost:8000'
    : '';

