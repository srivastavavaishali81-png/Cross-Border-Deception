"use client";

import Link from "next/link";
import {
  ArrowUpRight,
  Building2,
  Calendar,
  Globe,
  MapPin,
  Network,
  ShieldAlert,
  ShieldCheck,
  TrendingUp,
  Users,
} from "lucide-react";
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";
import type { CompanySummary } from "@/types";

interface CompanyCardProps {
  company: CompanySummary;
}

export function CompanyCard({ company }: CompanyCardProps) {
  const risk = company.latest_risk_score;

  const riskBadgeStyle =
    risk?.risk_level === "LOW"
      ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/30 shadow-[0_0_15px_rgba(34,197,94,0.15)]"
      : risk?.risk_level === "MEDIUM"
      ? "bg-amber-500/10 text-amber-400 border-amber-500/30 shadow-[0_0_15px_rgba(245,158,11,0.15)]"
      : risk?.risk_level === "HIGH"
      ? "bg-orange-500/10 text-orange-400 border-orange-500/30 shadow-[0_0_15px_rgba(249,115,22,0.15)]"
      : "bg-rose-500/10 text-rose-400 border-rose-500/30 shadow-[0_0_15px_rgba(239,68,68,0.15)]";

  const riskMeterColor =
    risk?.risk_level === "LOW"
      ? "bg-emerald-500"
      : risk?.risk_level === "MEDIUM"
      ? "bg-amber-500"
      : risk?.risk_level === "HIGH"
      ? "bg-orange-500"
      : "bg-rose-500";

  const formattedMarketCap = company.market_cap
    ? company.market_cap >= 1000000
      ? `$${(company.market_cap / 1000000).toFixed(2)}T`
      : company.market_cap >= 1000
      ? `$${(company.market_cap / 1000).toFixed(2)}B`
      : `$${company.market_cap.toFixed(2)}M`
    : "N/A";

  return (
    <Card className="glass-card glass-card-hover group relative flex flex-col justify-between overflow-hidden rounded-2xl border border-white/[0.08] shadow-xl">
      {/* Top ambient colored gradient indicator */}
      <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500/40 via-indigo-500/30 to-blue-500/0 opacity-0 transition-opacity group-hover:opacity-100" />

      <CardHeader className="pb-3 pt-5">
        <div className="flex items-start justify-between gap-3">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center rounded-lg bg-blue-500/15 px-2.5 py-0.5 text-xs font-mono font-bold text-blue-400 border border-blue-500/20">
                {company.ticker}
              </span>
              <span className="text-[11px] font-medium text-slate-400">
                {company.exchange}
              </span>
            </div>
            <Link
              href={`/companies/${company.ticker || company.id}`}
              className="text-base font-bold text-white transition-colors hover:text-blue-400 line-clamp-1 block pt-1"
            >
              {company.name}
            </Link>
          </div>

          {risk && (
            <div className="text-right shrink-0">
              <span className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-[11px] font-bold ${riskBadgeStyle}`}>
                <span className="h-1.5 w-1.5 rounded-full bg-current" />
                {risk.risk_level} ({risk.overall_score})
              </span>
            </div>
          )}
        </div>

        <p className="mt-2 text-xs text-slate-400 line-clamp-2 leading-relaxed font-normal">
          {company.description || "Leading enterprise profile indexed in OZARK surveillance registry."}
        </p>
      </CardHeader>

      <CardContent className="space-y-3 pb-4 pt-0">
        {/* Risk meter mini bar */}
        {risk && (
          <div className="space-y-1">
            <div className="flex justify-between text-[10px] text-slate-400 font-medium">
              <span>Risk Vulnerability</span>
              <span className="font-mono font-bold text-slate-300">{risk.overall_score} / 100</span>
            </div>
            <div className="h-1.5 w-full overflow-hidden rounded-full bg-slate-800">
              <div
                className={`h-full rounded-full transition-all duration-500 ${riskMeterColor}`}
                style={{ width: `${Math.min(risk.overall_score, 100)}%` }}
              />
            </div>
          </div>
        )}

        <div className="grid grid-cols-2 gap-2 text-xs">
          <div className="rounded-xl bg-[#0B1120]/60 p-2.5 border border-white/[0.05]">
            <span className="text-slate-400 block text-[10px] uppercase font-semibold tracking-wider">Industry</span>
            <span className="font-semibold text-slate-200 truncate block mt-0.5" title={company.industry}>
              {company.industry}
            </span>
          </div>

          <div className="rounded-xl bg-[#0B1120]/60 p-2.5 border border-white/[0.05]">
            <span className="text-slate-400 block text-[10px] uppercase font-semibold tracking-wider">Market Cap</span>
            <span className="font-semibold text-slate-200 truncate block mt-0.5 font-mono">
              {formattedMarketCap}
            </span>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-y-1 gap-x-3 text-[11px] text-slate-400 pt-1">
          <div className="flex items-center gap-1">
            <MapPin className="h-3 w-3 text-blue-400" />
            <span>
              {company.city ? `${company.city}, ` : ""}
              {company.state ? `${company.state}, ` : ""}
              {company.country}
            </span>
          </div>

          {company.employees && (
            <div className="flex items-center gap-1">
              <Users className="h-3 w-3 text-slate-500" />
              <span>{company.employees.toLocaleString()} emp</span>
            </div>
          )}
        </div>
      </CardContent>

      <CardFooter className="border-t border-white/[0.06] bg-[#0B1120]/40 px-5 py-3 flex items-center justify-between">
        <Link
          href={`/network?company=${company.ticker || company.id}`}
          className="inline-flex items-center gap-1 text-[11px] font-semibold text-cyan-400 hover:text-cyan-300 transition-colors"
        >
          <Network className="h-3 w-3" />
          Graph View
        </Link>

        <Link
          href={`/companies/${company.ticker || company.id}`}
          className="inline-flex items-center gap-1 text-xs font-semibold text-blue-400 transition-all hover:translate-x-0.5 hover:text-blue-300"
        >
          Full Profile
          <ArrowUpRight className="h-3.5 w-3.5" />
        </Link>
      </CardFooter>
    </Card>
  );
}
