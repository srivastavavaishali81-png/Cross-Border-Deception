export interface User {
  id: string;
  name: string;
  email: string;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export type RiskLevel = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";

export interface RiskScoreSummary {
  overall_score: number;
  risk_level: RiskLevel;
  recommendation?: string | null;
  credit_risk?: number;
  market_risk?: number;
  operational_risk?: number;
  liquidity_risk?: number;
  esg_score?: number;
  calculated_at?: string;
}

export interface FinancialOut {
  id?: string;
  fiscal_year: number;
  fiscal_quarter?: number | null;
  revenue?: number | null;
  gross_profit?: number | null;
  ebitda?: number | null;
  net_income?: number | null;
  eps?: number | null;
  total_assets?: number | null;
  total_debt?: number | null;
  cash_and_equivalents?: number | null;
  operating_cash_flow?: number | null;
  capex?: number | null;
  pe_ratio?: number | null;
  debt_to_equity?: number | null;
  current_ratio?: number | null;
  reported_at?: string | null;
}

export interface AlertOut {
  id?: string;
  alert_type: "RISK_THRESHOLD" | "PRICE_MOVEMENT" | "EARNINGS" | "REGULATORY" | "CUSTOM";
  severity: "INFO" | "WARNING" | "ERROR" | "CRITICAL";
  title: string;
  message: string;
  is_read: boolean;
  is_resolved: boolean;
  created_at?: string;
  metadata?: Record<string, unknown> | null;
}

export interface CompanySummary {
  id: string;
  name: string;
  ticker: string;
  sector: string;
  industry: string;
  country: string;
  state?: string | null;
  city?: string | null;
  exchange: string;
  market_cap?: number | null;
  employees?: number | null;
  founded_year?: number | null;
  website?: string | null;
  description?: string | null;
  is_active: boolean;
  created_at?: string;
  latest_risk_score?: RiskScoreSummary | null;
}

export interface CompanyDetail extends CompanySummary {
  financials: FinancialOut[];
  risk_scores: RiskScoreSummary[];
  alerts: AlertOut[];
  key_stats?: Record<string, unknown>;
}

export interface FilterOptions {
  industries: string[];
  states: string[];
  sectors: string[];
  exchanges: string[];
  risk_levels: string[];
}

export interface CompanyListResponse {
  items: CompanySummary[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  facets?: FilterOptions;
}

export interface CompanySearchResponse extends CompanyListResponse {
  query?: string;
}
