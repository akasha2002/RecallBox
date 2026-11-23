import type { HealthStatus } from '../types';
import { API_BASE_URL } from '../utils/constants';

/**
 * Fetch health status from the backend API.
 */
export async function checkBackendHealth(): Promise<HealthStatus> {
  const response = await fetch(`${API_BASE_URL}/api/v1/health`, {
    headers: {
      'Accept': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Backend health check failed with HTTP ${response.status}`);
  }

  return response.json();
}
