"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Activity,
  AlertOctagon,
  AlertTriangle,
  ArrowRight,
  ArrowUpRight,
  Building2,
  CheckCircle2,
  Cpu,
  Database,
  Download,
  Filter,
  Layers,
  Loader2,
  LogIn,
  Network,
  RefreshCw,
  Search,
  Shield,
  ShieldAlert,
  ShieldCheck,
  Sparkles,
  TrendingDown,
  TrendingUp,
  User,
  UserPlus,
  Zap,
} from "lucide-react";

import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { MetricCard } from "@/components/dashboard/MetricCard";
import { RevenueTrendChart } from "@/components/dashboard/RevenueTrendChart";
import { ProfitTrendChart } from "@/components/dashboard/ProfitTrendChart";
import { RiskDistributionChart } from "@/components/dashboard/RiskDistributionChart";
import { SectorAnalysisChart } from "@/components/dashboard/SectorAnalysisChart";
import { STAT_CARDS_DATA, WATCHLIST_COMPANIES } from "@/lib/dashboard-mock-data";

export default function InvestorDashboardPage() {
  const { user, isLoading, isAuthenticated, login } = useAuth();
  const router = useRouter();
  const [activeTimeframe, setActiveTimeframe] = useState<"1Y" | "3Y" | "5Y" | "ALL">("1Y");
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [isDemoLoading, setIsDemoLoading] = useState(false);

  const handleQuickDemo = async () => {
    try {
      setIsDemoLoading(true);
      await login({ email: "demo@ozark.ai", password: "Demo@123" });
      document.cookie = "ozark_authed=1; path=/; max-age=604800; SameSite=Strict";
    } catch (e) {
      console.error(e);
      router.push("/login");
    } finally {
      setIsDemoLoading(false);
    }
  };

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => {
      setIsRefreshing(false);
    }, 600);
  };

  if (isLoading) {
    return (
      <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4">
        <div className="h-10 w-10 animate-spin rounded-full border-4 border-blue-500 border-t-transparent shadow-[0_0_20px_rgba(37,99,235,0.4)]" />
        <span className="text-xs font-mono text-slate-400">Loading portfolio surveillance data...</span>
      </div>
    );
  }

  // ── Unauthenticated Access Gate ──────────────────────────────────────────
  if (!isAuthenticated && !user) {
    return (
      <div className="min-h-[80vh] flex items-center justify-center px-4 py-12">
        <Card className="glass-card rounded-3xl border border-white/[0.12] shadow-2xl max-w-lg w-full p-6 text-center space-y-6 bg-[#0F172A]/90 backdrop-blur-xl">
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-700 shadow-[0_0_30px_rgba(37,99,235,0.5)]">
            <Shield className="h-8 w-8 text-white" />
          </div>

          <div className="space-y-2">
            <span className="text-[11px] font-mono font-bold uppercase tracking-widest text-blue-400">
              Institutional Gate
            </span>
            <h2 className="text-2xl font-black text-white tracking-tight">
              Investor Dashboard Access Required
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 leading-relaxed max-w-sm mx-auto">
              Please sign in or use 1-click instant demo access to enter the multi-dimensional risk monitoring platform.
            </p>
          </div>

          <div className="space-y-3 pt-2">
            <Button
              onClick={handleQuickDemo}
              disabled={isDemoLoading}
              className="w-full h-11 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs shadow-[0_0_25px_rgba(245,158,11,0.35)] transition-all flex items-center justify-center gap-2"
            >
              {isDemoLoading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin text-slate-950" />
                  <span>Authorizing instant demo session...</span>
                </>
              ) : (
                <>
                  <Zap className="h-4 w-4 fill-slate-950" />
                  <span>Instant Demo Access (No Password Needed)</span>
                </>
              )}
            </Button>

            <div className="grid grid-cols-2 gap-3 pt-1">
              <Link href="/login?callbackUrl=/dashboard">
                <Button
                  variant="outline"
                  className="w-full h-10 rounded-xl text-xs font-bold border-white/20 bg-white/[0.05] hover:bg-white/[0.12] text-white flex items-center justify-center gap-1.5"
                >
                  <LogIn className="h-3.5 w-3.5 text-blue-400" />
                  Sign In
                </Button>
              </Link>
              <Link href="/register">
                <Button
                  className="w-full h-10 rounded-xl text-xs font-bold bg-blue-600 hover:bg-blue-500 text-white shadow-[0_0_15px_rgba(37,99,235,0.4)] flex items-center justify-center gap-1.5"
                >
                  <UserPlus className="h-3.5 w-3.5" />
                  Register
                </Button>
              </Link>
            </div>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen pb-20">
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 space-y-8">
        {/* Welcome Hero & Controls */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-white/[0.08] pb-6">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-mono font-bold uppercase tracking-widest text-blue-400">
                Institutional Portfolio Monitor
              </span>
              <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 px-2.5 py-0.5 text-xs font-mono font-bold text-emerald-400">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
                Live Feed
              </span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-black tracking-tight text-white">
              Executive Investor Dashboard
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 max-w-2xl">
              Real-time multi-dimensional surveillance of 50 enterprise assets, revenue trajectories, and probabilistic risk metrics.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2.5">
            {/* Timeframe selector */}
            <div className="flex items-center rounded-xl border border-white/10 bg-[#0F172A] p-1 text-xs">
              {(["1Y", "3Y", "5Y", "ALL"] as const).map((tf) => (
                <button
                  key={tf}
                  type="button"
                  onClick={() => setActiveTimeframe(tf)}
                  className={`rounded-lg px-3 py-1 font-bold text-xs transition-all ${
                    activeTimeframe === tf
                      ? "bg-blue-600 text-white shadow-[0_0_15px_rgba(37,99,235,0.4)]"
                      : "text-slate-400 hover:text-white"
                  }`}
                >
                  {tf}
                </button>
              ))}
            </div>

            <Button
              variant="outline"
              size="sm"
              onClick={handleRefresh}
              className="h-9 rounded-xl text-xs font-semibold gap-1.5 border-white/10 bg-[#0F172A] text-slate-300 hover:text-white"
            >
              <RefreshCw className={`h-3.5 w-3.5 ${isRefreshing ? "animate-spin text-blue-400" : ""}`} />
              Sync
            </Button>

            <Link href="/companies">
              <Button size="sm" className="h-9 rounded-xl text-xs gap-1.5 font-bold bg-blue-600 hover:bg-blue-500 text-white shadow-[0_0_20px_rgba(37,99,235,0.35)]">
                <Building2 className="h-3.5 w-3.5" />
                Directory
              </Button>
            </Link>
          </div>
        </div>

        {/* ── 1. Dashboard KPI Metric Cards ──────────────────────────────────── */}
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <MetricCard
            title={STAT_CARDS_DATA.totalCompanies.title}
            value={STAT_CARDS_DATA.totalCompanies.value}
            change={STAT_CARDS_DATA.totalCompanies.change}
            isPositive={STAT_CARDS_DATA.totalCompanies.isPositive}
            description={STAT_CARDS_DATA.totalCompanies.description}
            badge={STAT_CARDS_DATA.totalCompanies.badge}
            icon={Building2}
            iconColor="text-blue-400"
            iconBg="bg-blue-500/10"
          />

          <MetricCard
            title={STAT_CARDS_DATA.highRiskCompanies.title}
            value={STAT_CARDS_DATA.highRiskCompanies.value}
            change={STAT_CARDS_DATA.highRiskCompanies.change}
            isPositive={STAT_CARDS_DATA.highRiskCompanies.isPositive}
            description={STAT_CARDS_DATA.highRiskCompanies.description}
            badge={STAT_CARDS_DATA.highRiskCompanies.badge}
            icon={ShieldAlert}
            iconColor="text-rose-400"
            iconBg="bg-rose-500/10"
          />

          <MetricCard
            title={STAT_CARDS_DATA.lowRiskCompanies.title}
            value={STAT_CARDS_DATA.lowRiskCompanies.value}
            change={STAT_CARDS_DATA.lowRiskCompanies.change}
            isPositive={STAT_CARDS_DATA.lowRiskCompanies.isPositive}
            description={STAT_CARDS_DATA.lowRiskCompanies.description}
            badge={STAT_CARDS_DATA.lowRiskCompanies.badge}
            icon={ShieldCheck}
            iconColor="text-emerald-400"
            iconBg="bg-emerald-500/10"
          />

          <MetricCard
            title={STAT_CARDS_DATA.activeAlerts.title}
            value={STAT_CARDS_DATA.activeAlerts.value}
            change={STAT_CARDS_DATA.activeAlerts.change}
            isPositive={STAT_CARDS_DATA.activeAlerts.isPositive}
            description={STAT_CARDS_DATA.activeAlerts.description}
            badge={STAT_CARDS_DATA.activeAlerts.badge}
            icon={AlertTriangle}
            iconColor="text-amber-400"
            iconBg="bg-amber-500/10"
          />
        </div>

        {/* ── 2. Recharts Financial Visualizations (2x2 Grid) ───────────────── */}
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <RevenueTrendChart />
          <ProfitTrendChart />
          <RiskDistributionChart />
          <SectorAnalysisChart />
        </div>

        {/* ── 3. High Risk Surveillance Watchlist & Live Alerts ──────────────── */}
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          {/* Watchlist Table */}
          <div className="lg:col-span-2">
            <Card className="glass-card rounded-3xl border border-white/[0.08] shadow-xl h-full flex flex-col justify-between">
              <CardHeader className="flex flex-row items-center justify-between pb-3">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <ShieldAlert className="h-5 w-5 text-amber-400" />
                    <CardTitle className="text-base font-bold text-white">
                      High Risk Surveillance Watchlist
                    </CardTitle>
                  </div>
                  <CardDescription className="text-xs text-slate-400">
                    Companies requiring active portfolio monitoring based on ML risk scores
                  </CardDescription>
                </div>

                <Link
                  href="/companies?risk_level=HIGH"
                  className="text-xs font-semibold text-blue-400 hover:text-blue-300 flex items-center gap-1 transition-colors"
                >
                  View all
                  <ArrowRight className="h-3.5 w-3.5" />
                </Link>
              </CardHeader>

              <CardContent>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs">
                    <thead>
                      <tr className="border-b border-white/10 text-slate-400 font-mono text-[11px] uppercase tracking-wider">
                        <th className="pb-3 font-semibold">Entity</th>
                        <th className="pb-3 font-semibold">Sector</th>
                        <th className="pb-3 font-semibold text-right">Market Cap</th>
                        <th className="pb-3 font-semibold text-center">Risk Score</th>
                        <th className="pb-3 font-semibold">Surveillance Catalyst</th>
                        <th className="pb-3 font-semibold text-right">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-white/[0.05]">
                      {WATCHLIST_COMPANIES.map((item) => (
                        <tr key={item.ticker} className="hover:bg-white/[0.03] transition-colors">
                          <td className="py-3.5">
                            <div className="flex items-center gap-2">
                              <span className="font-bold font-mono bg-blue-500/10 text-blue-400 border border-blue-500/20 px-1.5 py-0.5 rounded text-[11px]">
                                {item.ticker}
                              </span>
                              <span className="font-semibold text-slate-200 truncate max-w-[120px]">
                                {item.name}
                              </span>
                            </div>
                          </td>
                          <td className="py-3.5 text-slate-400">{item.sector}</td>
                          <td className="py-3.5 text-right font-mono font-medium text-slate-200">
                            {item.marketCap}
                          </td>
                          <td className="py-3.5 text-center">
                            <span
                              className={`inline-flex items-center rounded-full border px-2 py-0.5 text-[10px] font-bold font-mono ${
                                item.riskLevel === "HIGH"
                                  ? "bg-rose-500/10 text-rose-400 border-rose-500/20 shadow-[0_0_10px_rgba(239,68,68,0.15)]"
                                  : "bg-amber-500/10 text-amber-400 border-amber-500/20 shadow-[0_0_10px_rgba(245,158,11,0.15)]"
                              }`}
                            >
                              {item.riskScore}
                            </span>
                          </td>
                          <td className="py-3.5 text-slate-400 max-w-[180px] truncate text-[11px]" title={item.anomalyCatalyst}>
                            {item.anomalyCatalyst}
                          </td>
                          <td className="py-3.5 text-right">
                            <div className="flex items-center justify-end gap-2">
                              <Link
                                href={`/network?company=${item.ticker}`}
                                className="text-[11px] font-semibold text-cyan-400 hover:text-cyan-300 transition-colors"
                                title="Relationship Network"
                              >
                                <Network className="h-3.5 w-3.5" />
                              </Link>
                              <Link
                                href={`/companies/${item.ticker}`}
                                className="inline-flex items-center gap-0.5 text-xs font-semibold text-blue-400 hover:text-blue-300"
                              >
                                Analyze
                                <ArrowUpRight className="h-3 w-3" />
                              </Link>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Real-time Alerts & System Infrastructure */}
          <div className="lg:col-span-1 space-y-6">
            <Card className="glass-card rounded-3xl border border-white/[0.08] shadow-xl">
              <CardHeader className="pb-3">
                <div className="flex items-center gap-2">
                  <Activity className="h-5 w-5 text-blue-400" />
                  <CardTitle className="text-base font-bold text-white">Active Anomaly Stream</CardTitle>
                </div>
                <CardDescription className="text-xs text-slate-400">
                  Triggered algorithmic surveillance alerts
                </CardDescription>
              </CardHeader>

              <CardContent className="space-y-3">
                {[
                  {
                    title: "Tesla (TSLA) Volatility Surge",
                    time: "12m ago",
                    severity: "WARNING",
                    desc: "Market risk score spiked above 70.0 on options implied volume.",
                    badgeColor: "border-amber-500/30 bg-amber-500/10 text-amber-400",
                  },
                  {
                    title: "NVIDIA (NVDA) Guidance Revision",
                    time: "1h ago",
                    severity: "INFO",
                    desc: "Data center revenue consensus revisions adjusted upwards by +18%.",
                    badgeColor: "border-blue-500/30 bg-blue-500/10 text-blue-400",
                  },
                  {
                    title: "Exxon (XOM) Carbon Boundary",
                    time: "4h ago",
                    severity: "WARNING",
                    desc: "European carbon border adjustment vulnerability highlighted in risk model.",
                    badgeColor: "border-rose-500/30 bg-rose-500/10 text-rose-400",
                  },
                ].map((alert, i) => (
                  <div
                    key={i}
                    className="rounded-2xl border border-white/[0.06] bg-[#0B1120]/60 p-3.5 text-xs space-y-1.5"
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-slate-200 truncate">{alert.title}</span>
                      <span className="text-[10px] font-mono text-slate-400 whitespace-nowrap">{alert.time}</span>
                    </div>
                    <p className="text-[11px] text-slate-400 leading-relaxed">{alert.desc}</p>
                  </div>
                ))}
              </CardContent>
            </Card>

            <Card className="glass-card rounded-3xl border border-white/[0.08] shadow-xl">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-bold text-white">Platform Ingestion Nodes</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div className="rounded-xl bg-[#0B1120]/60 p-3 border border-white/[0.05]">
                    <span className="text-slate-400 block text-[10px] uppercase font-semibold">PostgreSQL Store</span>
                    <span className="font-mono font-bold text-emerald-400 mt-1 flex items-center gap-1.5">
                      <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
                      50 Assets
                    </span>
                  </div>
                  <div className="rounded-xl bg-[#0B1120]/60 p-3 border border-white/[0.05]">
                    <span className="text-slate-400 block text-[10px] uppercase font-semibold">Neo4j Driver</span>
                    <span className="font-mono font-bold text-emerald-400 mt-1 flex items-center gap-1.5">
                      <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
                      v5 Connected
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}
