// Application Type Definitions

export interface HealthStatus {
  status: string;
  app: string;
  version: string;
  environment: string;
  timestamp?: string;
}

export interface WorkspaceSummary {
  id: string;
  name: string;
  created_at: string;
}
