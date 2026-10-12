"use client";

import { use, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Activity,
  AlertTriangle,
  ArrowLeft,
  ArrowUpRight,
  Building2,
  Calendar,
  CheckCircle2,
  DollarSign,
  ExternalLink,
  FileText,
  Globe,
  Info,
  Loader2,
  MapPin,
  Network,
  Share2,
  Shield,
  ShieldAlert,
  ShieldCheck,
  Sparkles,
  TrendingDown,
  TrendingUp,
  Users,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ErrorState } from "@/components/ui/ErrorState";
import { fetchCompanyDetail } from "@/lib/companies";
import type { CompanyDetail } from "@/types";

interface PageProps {
  params: Promise<{ id: string }>;
}

export default function CompanyDetailPage({ params }: PageProps) {
  const resolvedParams = use(params);
  const router = useRouter();
  const [company, setCompany] = useState<CompanyDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadDetail = () => {
    setIsLoading(true);
    setError(null);
    fetchCompanyDetail(resolvedParams.id)
      .then((data) => {
        setCompany(data);
      })
      .catch((err) => {
        setError(err.message || "Failed to load company profile");
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  useEffect(() => {
    loadDetail();
  }, [resolvedParams.id]);

  if (isLoading) {
    return (
      <div className="flex min-h-[60vh] flex-col items-center justify-center space-y-4">
        <Loader2 className="h-10 w-10 animate-spin text-blue-500" />
        <p className="text-xs font-mono font-semibold text-slate-400">
          Decrypting institutional entity dossier...
        </p>
      </div>
    );
  }

  if (error || !company) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-16">
        <ErrorState
          title="Company Dossier Not Found"
          message={error || `Unable to locate records for entity "${resolvedParams.id}".`}
          onRetry={loadDetail}
        />
        <div className="text-center mt-6">
          <Link href="/companies">
            <Button variant="outline" className="gap-2 rounded-xl border-white/10 bg-[#0F172A] text-xs font-semibold text-white">
              <ArrowLeft className="h-4 w-4" />
              Back to Companies Directory
            </Button>
          </Link>
        </div>
      </div>
    );
  }

  const latestRisk = company.latest_risk_score || company.risk_scores[0];

  const riskBadgeStyle =
    latestRisk?.risk_level === "LOW"
      ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/30 shadow-[0_0_15px_rgba(34,197,94,0.15)]"
      : latestRisk?.risk_level === "MEDIUM"
      ? "bg-amber-500/10 text-amber-400 border-amber-500/30 shadow-[0_0_15px_rgba(245,158,11,0.15)]"
      : latestRisk?.risk_level === "HIGH"
      ? "bg-orange-500/10 text-orange-400 border-orange-500/30 shadow-[0_0_15px_rgba(249,115,22,0.15)]"
      : "bg-rose-500/10 text-rose-400 border-rose-500/30 shadow-[0_0_15px_rgba(239,68,68,0.15)]";

  const formattedMarketCap = company.market_cap
    ? company.market_cap >= 1000000
      ? `$${(company.market_cap / 1000000).toFixed(2)} Trillion`
      : company.market_cap >= 1000
      ? `$${(company.market_cap / 1000).toFixed(2)} Billion`
      : `$${company.market_cap.toFixed(2)} Million`
    : "Not Disclosed";

  return (
    <div className="min-h-screen pb-20">
      {/* ── Breadcrumbs & Quick Navigation ──────────────────────────────────── */}
      <div className="border-b border-white/[0.06] bg-[#0B1120]/60 backdrop-blur-md">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6">
          <div className="flex items-center gap-3">
            <Link
              href="/companies"
              className="inline-flex items-center gap-1.5 rounded-xl border border-white/10 bg-[#0F172A] px-3 py-1.5 text-xs font-semibold text-slate-300 hover:text-white transition-colors"
            >
              <ArrowLeft className="h-3.5 w-3.5" />
              Companies
            </Link>
            <span className="text-xs text-slate-600">/</span>
            <span className="text-xs font-bold text-white font-mono">{company.ticker}</span>
            <span className="text-xs text-slate-400 hidden sm:inline">({company.name})</span>
          </div>

          <div className="flex items-center gap-3">
            <Link
              href={`/network?company=${company.ticker || company.id}`}
              className="inline-flex items-center gap-1.5 rounded-xl border border-cyan-500/40 bg-cyan-500/10 px-3.5 py-1.5 text-xs font-bold text-cyan-400 hover:bg-cyan-500/20 hover:text-cyan-300 transition-all shadow-[0_0_15px_rgba(6,182,212,0.2)]"
            >
              <Network className="h-3.5 w-3.5" />
              Neo4j Graph
            </Link>

            {company.website && (
              <a
                href={company.website}
                target="_blank"
                rel="noopener noreferrer"
                className="hidden sm:inline-flex items-center gap-1.5 text-xs font-semibold text-blue-400 hover:underline"
              >
                <Globe className="h-3.5 w-3.5" />
                Website
                <ExternalLink className="h-3 w-3" />
              </a>
            )}
          </div>
        </div>
      </div>

      {/* ── Main Container ─────────────────────────────────────────────────── */}
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 space-y-8">
        {/* Company Hero Card */}
        <div className="glass-card relative overflow-hidden rounded-3xl p-6 sm:p-8 border border-white/[0.08] shadow-2xl">
          <div className="relative z-10 flex flex-col justify-between gap-6 md:flex-row md:items-center">
            <div className="space-y-3">
              <div className="flex flex-wrap items-center gap-2">
                <span className="rounded-xl bg-blue-500/15 px-3 py-1 text-sm font-mono font-bold tracking-wider text-blue-400 border border-blue-500/25">
                  {company.ticker}
                </span>
                <span className="rounded-lg bg-white/[0.04] border border-white/[0.06] px-2.5 py-1 text-xs font-semibold text-slate-300">
                  {company.exchange}
                </span>
                <span className="rounded-lg bg-white/[0.04] border border-white/[0.06] px-2.5 py-1 text-xs font-semibold text-slate-300">
                  {company.sector}
                </span>
                <span className="rounded-lg bg-white/[0.04] border border-white/[0.06] px-2.5 py-1 text-xs font-semibold text-slate-300">
                  {company.industry}
                </span>
              </div>

              <h1 className="text-3xl sm:text-4xl font-black tracking-tight text-white">
                {company.name}
              </h1>

              <p className="max-w-3xl text-xs sm:text-sm leading-relaxed text-slate-400 font-normal">
                {company.description || "Leading enterprise profile indexed in OZARK surveillance registry."}
              </p>
            </div>

            {/* Quick Metrics Badge Group */}
            <div className="flex flex-row md:flex-col gap-3 shrink-0">
              <div className="rounded-2xl border border-white/10 bg-[#0B1120]/80 p-4 shadow-sm min-w-[190px]">
                <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 block">
                  Market Capitalization
                </span>
                <p className="mt-1 text-xl font-black text-white font-mono">
                  {formattedMarketCap}
                </p>
              </div>

              {latestRisk && (
                <div className="rounded-2xl border border-white/10 bg-[#0B1120]/80 p-4 shadow-sm min-w-[190px]">
                  <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 block">
                    Composite Risk Score
                  </span>
                  <div className="mt-1 flex items-center justify-between">
                    <span className="text-xl font-black text-white font-mono">
                      {latestRisk.overall_score} <span className="text-xs text-slate-500">/ 100</span>
                    </span>
                    <span className={`rounded-full border px-2.5 py-0.5 text-xs font-bold ${riskBadgeStyle}`}>
                      {latestRisk.risk_level}
                    </span>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Location & Metadata Bar */}
          <div className="mt-6 flex flex-wrap items-center gap-y-2 gap-x-6 border-t border-white/[0.06] pt-5 text-xs text-slate-400">
            <div className="flex items-center gap-1.5">
              <MapPin className="h-4 w-4 text-blue-400" />
              <span>
                {company.city ? `${company.city}, ` : ""}
                {company.state ? `${company.state}, ` : ""}
                {company.country}
              </span>
            </div>

            {company.employees && (
              <div className="flex items-center gap-1.5">
                <Users className="h-4 w-4 text-slate-400" />
                <span>{company.employees.toLocaleString()} Full-time Employees</span>
              </div>
            )}

            {company.founded_year && (
              <div className="flex items-center gap-1.5">
                <Calendar className="h-4 w-4 text-slate-400" />
                <span>Founded in {company.founded_year}</span>
              </div>
            )}
          </div>
        </div>

        {/* ── 2-Column Section: Risk Metrics & Financials ───────────────────── */}
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
          {/* ── Left Column: Risk Analysis Breakdown ────────────────────────── */}
          <div className="lg:col-span-1 space-y-6">
            <Card className="glass-card rounded-3xl border border-white/[0.08] shadow-xl">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Shield className="h-5 w-5 text-blue-400" />
                    <CardTitle className="text-base font-bold text-white">Risk Intelligence</CardTitle>
                  </div>
                  {latestRisk && (
                    <span className={`rounded-full border px-2.5 py-0.5 text-xs font-bold ${riskBadgeStyle}`}>
                      {latestRisk.risk_level}
                    </span>
                  )}
                </div>
                <CardDescription className="text-xs text-slate-400">
                  ML-computed probabilistic risk profile & recommendation
                </CardDescription>
              </CardHeader>

              <CardContent className="space-y-5 pt-2">
                {latestRisk ? (
                  <>
                    {/* Natural Language Recommendation Box */}
                    <div
                      className={`rounded-2xl border p-4 text-xs leading-relaxed space-y-2 shadow-inner transition-all ${
                        latestRisk.risk_level === "LOW"
                          ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-300"
                          : latestRisk.risk_level === "MEDIUM"
                          ? "border-amber-500/30 bg-amber-500/10 text-amber-300"
                          : latestRisk.risk_level === "HIGH"
                          ? "border-orange-500/30 bg-orange-500/10 text-orange-300"
                          : "border-rose-500/30 bg-rose-500/10 text-rose-300"
                      }`}
                    >
                      <div className="flex items-center gap-1.5 font-bold uppercase tracking-wider text-[11px]">
                        <Sparkles className="h-3.5 w-3.5 shrink-0" />
                        <span>Natural Language Recommendation</span>
                      </div>
                      <p className="font-semibold text-white leading-relaxed text-sm">
                        &ldquo;
                        {latestRisk.recommendation || (
                          latestRisk.risk_level === "LOW"
                            ? "This company demonstrates strong financial stability and low fraud indicators."
                            : latestRisk.risk_level === "MEDIUM"
                            ? "This investment requires caution due to moderate compliance risks."
                            : latestRisk.risk_level === "HIGH"
                            ? "This company shows significant fraud indicators and weak financial health."
                            : "This company shows severe fraud indicators, critical governance violations, and highly distressed financial health."
                        )}
                        &rdquo;
                      </p>
                    </div>

                    {/* Gauge Overview */}
                    <div className="rounded-2xl bg-[#0B1120]/60 p-4 border border-white/[0.06] flex items-center justify-between">
                      <div>
                        <span className="text-xs text-slate-400 block font-medium">Overall Vulnerability Score</span>
                        <span className="text-3xl font-black tracking-tight text-white font-mono">
                          {latestRisk.overall_score}
                          <span className="text-sm font-normal text-slate-500"> / 100</span>
                        </span>
                      </div>
                      <div className={`flex h-12 w-12 items-center justify-center rounded-2xl ${riskBadgeStyle}`}>
                        <ShieldAlert className="h-6 w-6" />
                      </div>
                    </div>

                    {/* Sub-scores Progress Bars */}
                    <div className="space-y-3.5">
                      {[
                        { label: "Credit Risk", val: latestRisk.credit_risk ?? 20.0 },
                        { label: "Market Volatility Risk", val: latestRisk.market_risk ?? 25.0 },
                        { label: "Operational Risk", val: latestRisk.operational_risk ?? 18.0 },
                        { label: "Liquidity Risk", val: latestRisk.liquidity_risk ?? 12.0 },
                      ].map(({ label, val }) => {
                        const barColor =
                          val < 25 ? "bg-emerald-500" : val < 50 ? "bg-amber-500" : val < 75 ? "bg-orange-500" : "bg-rose-500";
                        return (
                          <div key={label} className="space-y-1.5">
                            <div className="flex justify-between text-xs font-medium">
                              <span className="text-slate-400">{label}</span>
                              <span className="font-mono font-bold text-white">{val.toFixed(1)}</span>
                            </div>
                            <div className="h-2 w-full overflow-hidden rounded-full bg-slate-800">
                              <div
                                className={`h-full rounded-full transition-all duration-500 ${barColor}`}
                                style={{ width: `${Math.min(val, 100)}%` }}
                              />
                            </div>
                          </div>
                        );
                      })}

                      {latestRisk.esg_score !== undefined && (
                        <div className="mt-4 pt-4 border-t border-white/[0.06] flex items-center justify-between text-xs">
                          <span className="text-slate-400 font-medium">ESG Sustainability Score</span>
                          <span className="font-bold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-0.5 rounded-xl font-mono">
                            {latestRisk.esg_score.toFixed(1)} / 100
                          </span>
                        </div>
                      )}
                    </div>
                  </>
                ) : (
                  <p className="text-xs text-slate-400">No risk score calculations recorded.</p>
                )}
              </CardContent>
            </Card>

            {/* Key Stats Card */}
            <Card className="glass-card rounded-3xl border border-white/[0.08] shadow-xl">
              <CardHeader className="pb-3">
                <CardTitle className="text-base font-bold text-white">Corporate Overview</CardTitle>
              </CardHeader>
              <CardContent>
                <dl className="space-y-2.5 text-xs">
                  <div className="flex justify-between border-b border-white/[0.05] pb-2">
                    <dt className="text-slate-400">Exchange</dt>
                    <dd className="font-semibold text-white">{company.exchange}</dd>
                  </div>
                  <div className="flex justify-between border-b border-white/[0.05] pb-2">
                    <dt className="text-slate-400">Sector</dt>
                    <dd className="font-semibold text-white">{company.sector}</dd>
                  </div>
                  <div className="flex justify-between border-b border-white/[0.05] pb-2">
                    <dt className="text-slate-400">Industry</dt>
                    <dd className="font-semibold text-white">{company.industry}</dd>
                  </div>
                  <div className="flex justify-between border-b border-white/[0.05] pb-2">
                    <dt className="text-slate-400">Headquarters</dt>
                    <dd className="font-semibold text-white">
                      {company.city ? `${company.city}, ` : ""}{company.state || company.country}
                    </dd>
                  </div>
                  <div className="flex justify-between pb-1">
                    <dt className="text-slate-400">Surveillance Status</dt>
                    <dd className="font-semibold text-emerald-400 flex items-center gap-1.5 font-mono">
                      <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
                      Active Monitored
                    </dd>
                  </div>
                </dl>
              </CardContent>
            </Card>
          </div>

          {/* ── Right Column: Financial Performance & Surveillance Alerts ── */}
          <div className="lg:col-span-2 space-y-6">
            {/* Financial Performance Table */}
            <Card className="glass-card rounded-3xl border border-white/[0.08] shadow-xl">
              <CardHeader className="pb-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <DollarSign className="h-5 w-5 text-blue-400" />
                    <CardTitle className="text-base font-bold text-white">Financial Performance</CardTitle>
                  </div>
                  <span className="text-xs text-slate-400 font-mono">Values in $M USD</span>
                </div>
                <CardDescription className="text-xs text-slate-400">
                  Audited financial statements and valuation ratios
                </CardDescription>
              </CardHeader>

              <CardContent>
                {company.financials && company.financials.length > 0 ? (
                  <div className="overflow-x-auto">
                    <table className="w-full text-left text-xs">
                      <thead>
                        <tr className="border-b border-white/10 text-slate-400 font-mono text-[11px] uppercase tracking-wider">
                          <th className="pb-3 font-semibold">Fiscal Period</th>
                          <th className="pb-3 font-semibold text-right">Revenue</th>
                          <th className="pb-3 font-semibold text-right">Gross Profit</th>
                          <th className="pb-3 font-semibold text-right">EBITDA</th>
                          <th className="pb-3 font-semibold text-right">Net Income</th>
                          <th className="pb-3 font-semibold text-right">P/E</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-white/[0.05]">
                        {company.financials.map((fin, idx) => (
                          <tr key={idx} className="hover:bg-white/[0.03] transition-colors">
                            <td className="py-3 font-bold text-white font-mono">
                              FY{fin.fiscal_year} {fin.fiscal_quarter ? `Q${fin.fiscal_quarter}` : "Annual"}
                            </td>
                            <td className="py-3 text-right font-mono font-medium text-slate-200">
                              {fin.revenue ? `$${fin.revenue.toLocaleString()}` : "—"}
                            </td>
                            <td className="py-3 text-right font-mono text-slate-400">
                              {fin.gross_profit ? `$${fin.gross_profit.toLocaleString()}` : "—"}
                            </td>
                            <td className="py-3 text-right font-mono text-slate-400">
                              {fin.ebitda ? `$${fin.ebitda.toLocaleString()}` : "—"}
                            </td>
                            <td className="py-3 text-right font-mono font-bold text-emerald-400">
                              {fin.net_income ? `$${fin.net_income.toLocaleString()}` : "—"}
                            </td>
                            <td className="py-3 text-right font-mono text-slate-200 font-medium">
                              {fin.pe_ratio ? `${fin.pe_ratio}x` : "—"}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <p className="text-xs text-slate-400">No audited financial statements recorded.</p>
                )}
              </CardContent>
            </Card>

            {/* Active Surveillance Alerts */}
            <Card className="glass-card rounded-3xl border border-white/[0.08] shadow-xl">
              <CardHeader className="pb-3">
                <div className="flex items-center gap-2">
                  <Activity className="h-5 w-5 text-amber-400" />
                  <CardTitle className="text-base font-bold text-white">Surveillance Alerts & Filings</CardTitle>
                </div>
                <CardDescription className="text-xs text-slate-400">
                  Regulatory notices, SEC/LODR filings, and market anomalies
                </CardDescription>
              </CardHeader>

              <CardContent className="space-y-3">
                {company.alerts && company.alerts.length > 0 ? (
                  company.alerts.map((alert, idx) => (
                    <div
                      key={idx}
                      className="rounded-2xl border border-white/[0.06] bg-[#0B1120]/60 p-4 text-xs space-y-1.5"
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-white text-sm">{alert.title}</span>
                        <span className="rounded-lg bg-blue-500/10 border border-blue-500/20 px-2 py-0.5 text-[10px] font-mono font-bold text-blue-400">
                          {alert.alert_type}
                        </span>
                      </div>
                      <p className="text-xs text-slate-400 leading-relaxed">{alert.message}</p>
                    </div>
                  ))
                ) : (
                  <div className="flex items-center gap-2 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 p-4 text-xs text-emerald-400">
                    <CheckCircle2 className="h-4 w-4 shrink-0" />
                    <span>Zero active regulatory penalties or high-risk compliance alerts flagged.</span>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}
