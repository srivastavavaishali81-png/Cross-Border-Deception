/**
OZARK — Investor Dashboard Mock Data & Analytics
*/

export interface MetricCardData {
  title: string;
  value: string | number;
  change: string;
  isPositive: boolean;
  description: string;
  badge: string;
}

export interface RevenueTrendPoint {
  period: string;
  revenue: number; // in $ Billions
  growthRate: number; // in %
  targetRevenue: number;
}

export interface ProfitTrendPoint {
  period: string;
  grossProfit: number; // in $ Billions
  ebitda: number;
  netIncome: number;
  profitMargin: number; // in %
}

export interface RiskDistributionPoint {
  name: string;
  value: number; // company count
  percentage: number;
  color: string;
  description: string;
}

export interface SectorAnalysisPoint {
  sector: string;
  companyCount: number;
  marketCap: number; // in $ Billions
  avgRiskScore: number;
  color: string;
}

export interface WatchlistCompany {
  id: string;
  name: string;
  ticker: string;
  sector: string;
  marketCap: string;
  riskScore: number;
  riskLevel: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  riskTrend: "up" | "down" | "stable";
  anomalyCatalyst: string;
}

// ── Overview Stat Cards ───────────────────────────────────────────────────────
export const STAT_CARDS_DATA = {
  totalCompanies: {
    title: "Total Companies",
    value: "50",
    change: "+8 this quarter",
    isPositive: true,
    description: "Active enterprise surveillance coverage",
    badge: "100% Monitored",
  },
  highRiskCompanies: {
    title: "High Risk Companies",
    value: "6",
    change: "-2 from last month",
    isPositive: true, // fewer high-risk companies is good
    description: "Scores > 50.0 triggering scrutiny",
    badge: "Action Required",
  },
  lowRiskCompanies: {
    title: "Low Risk Companies",
    value: "34",
    change: "+4 upgraded",
    isPositive: true,
    description: "Resilient balance sheets & steady cash flow",
    badge: "68% of Portfolio",
  },
  activeAlerts: {
    title: "Active Alerts",
    value: "14",
    change: "3 critical unresolved",
    isPositive: false,
    description: "Real-time anomaly & threshold alerts",
    badge: "Live Feed",
  },
};

// ── 1. Revenue Trend Data (5-Year & Quarterly) ────────────────────────────────
export const REVENUE_TREND_DATA: RevenueTrendPoint[] = [
  { period: "Q1 2023", revenue: 840.5, growthRate: 8.4, targetRevenue: 820.0 },
  { period: "Q2 2023", revenue: 895.2, growthRate: 9.1, targetRevenue: 870.0 },
  { period: "Q3 2023", revenue: 945.8, growthRate: 11.2, targetRevenue: 920.0 },
  { period: "Q4 2023", revenue: 1040.0, growthRate: 14.5, targetRevenue: 990.0 },
  { period: "Q1 2024", revenue: 1085.4, growthRate: 12.8, targetRevenue: 1050.0 },
  { period: "Q2 2024", revenue: 1160.2, growthRate: 15.3, targetRevenue: 1110.0 },
  { period: "Q3 2024", revenue: 1245.8, growthRate: 18.2, targetRevenue: 1180.0 },
  { period: "Q4 2024 (E)", revenue: 1380.0, growthRate: 21.0, targetRevenue: 1290.0 },
];

// ── 2. Profit Trend Data ─────────────────────────────────────────────────────
export const PROFIT_TREND_DATA: ProfitTrendPoint[] = [
  { period: "2020", grossProfit: 1450.0, ebitda: 780.0, netIncome: 460.0, profitMargin: 18.2 },
  { period: "2021", grossProfit: 1780.0, ebitda: 980.0, netIncome: 620.0, profitMargin: 21.4 },
  { period: "2022", grossProfit: 2050.0, ebitda: 1120.0, netIncome: 740.0, profitMargin: 20.8 },
  { period: "2023", grossProfit: 2420.0, ebitda: 1390.0, netIncome: 910.0, profitMargin: 23.5 },
  { period: "2024", grossProfit: 2890.0, ebitda: 1680.0, netIncome: 1140.0, profitMargin: 25.8 },
];

// ── 3. Risk Distribution Data ────────────────────────────────────────────────
export const RISK_DISTRIBUTION_DATA: RiskDistributionPoint[] = [
  {
    name: "Low Risk",
    value: 34,
    percentage: 68,
    color: "#10b981", // emerald-500
    description: "Scores 0–24. Strong liquidity, low leverage",
  },
  {
    name: "Medium Risk",
    value: 10,
    percentage: 20,
    color: "#f59e0b", // amber-500
    description: "Scores 25–49. Moderate volatility or market cyclicality",
  },
  {
    name: "High Risk",
    value: 5,
    percentage: 10,
    color: "#f97316", // orange-500
    description: "Scores 50–74. Elevated debt or margin compression",
  },
  {
    name: "Critical Risk",
    value: 1,
    percentage: 2,
    color: "#ef4444", // rose-500
    description: "Scores 75+. Severe anomaly flags or restructuring risk",
  },
];

// ── 4. Sector Analysis Data ──────────────────────────────────────────────────
export const SECTOR_ANALYSIS_DATA: SectorAnalysisPoint[] = [
  { sector: "Technology", companyCount: 16, marketCap: 15400, avgRiskScore: 24.8, color: "#6366f1" },
  { sector: "Healthcare", companyCount: 8, marketCap: 2850, avgRiskScore: 23.4, color: "#06b6d4" },
  { sector: "Financials", companyCount: 7, marketCap: 3420, avgRiskScore: 31.2, color: "#8b5cf6" },
  { sector: "Consumer Cyclical", companyCount: 5, marketCap: 3280, avgRiskScore: 36.5, color: "#ec4899" },
  { sector: "Communication", companyCount: 4, marketCap: 4070, avgRiskScore: 26.0, color: "#3b82f6" },
  { sector: "Energy", companyCount: 3, marketCap: 765, avgRiskScore: 43.1, color: "#f59e0b" },
  { sector: "Industrials", companyCount: 4, marketCap: 705, avgRiskScore: 31.8, color: "#10b981" },
  { sector: "Consumer Defensive", companyCount: 3, marketCap: 1135, avgRiskScore: 18.5, color: "#14b8a6" },
];

// ── High Risk Watchlist ───────────────────────────────────────────────────────
export const WATCHLIST_COMPANIES: WatchlistCompany[] = [
  {
    id: "c0000000-0000-0000-0000-000000000009",
    name: "Tesla Inc.",
    ticker: "TSLA",
    sector: "Consumer Cyclical",
    marketCap: "$750.0B",
    riskScore: 58.2,
    riskLevel: "HIGH",
    riskTrend: "up",
    anomalyCatalyst: "Elevated market volatility & margin contraction",
  },
  {
    id: "c0000000-0000-0000-0000-000000000050",
    name: "Palantir Technologies",
    ticker: "PLTR",
    sector: "Technology",
    marketCap: "$115.0B",
    riskScore: 46.0,
    riskLevel: "MEDIUM",
    riskTrend: "down",
    anomalyCatalyst: "High forward valuation multiple (95x P/E)",
  },
  {
    id: "c0000000-0000-0000-0000-000000000013",
    name: "Exxon Mobil",
    ticker: "XOM",
    sector: "Energy",
    marketCap: "$495.0B",
    riskScore: 44.2,
    riskLevel: "MEDIUM",
    riskTrend: "up",
    anomalyCatalyst: "Commodity spot price fluctuations & ESG transition",
  },
  {
    id: "c0000000-0000-0000-0000-000000000026",
    name: "Chevron Corporation",
    ticker: "CVX",
    sector: "Energy",
    marketCap: "$270.0B",
    riskScore: 42.0,
    riskLevel: "MEDIUM",
    riskTrend: "stable",
    anomalyCatalyst: "Refining crack spread cyclical pressure",
  },
  {
    id: "c0000000-0000-0000-0000-000000000027",
    name: "Advanced Micro Devices",
    ticker: "AMD",
    sector: "Technology",
    marketCap: "$245.0B",
    riskScore: 41.5,
    riskLevel: "MEDIUM",
    riskTrend: "down",
    anomalyCatalyst: "Competitive AI accelerator cycle cadence",
  },
];
