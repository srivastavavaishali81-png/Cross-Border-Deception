"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  ArrowRight,
  BarChart3,
  Building2,
  CheckCircle2,
  Database,
  Globe,
  KeyRound,
  Layers,
  LogIn,
  Network,
  Shield,
  ShieldAlert,
  ShieldCheck,
  Sparkles,
  TrendingUp,
  UserPlus,
  Zap,
} from "lucide-react";
import { SearchBar } from "@/components/SearchBar";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/contexts/AuthContext";

export default function HomePage() {
  const router = useRouter();
  const { login, isAuthenticated } = useAuth();
  const [isDemoLoading, setIsDemoLoading] = useState(false);

  const handleQuickDemo = async () => {
    try {
      setIsDemoLoading(true);
      await login({ email: "demo@ozark.ai", password: "Demo@123" });
      document.cookie = "ozark_authed=1; path=/; max-age=604800; SameSite=Strict";
      router.push("/dashboard");
    } catch (e) {
      console.error(e);
      router.push("/login");
    } finally {
      setIsDemoLoading(false);
    }
  };

  return (
    <main className="relative flex min-h-screen flex-col items-center justify-start overflow-hidden pt-8 pb-24 px-4 sm:px-6 lg:px-8">
      {/* ── Hero Section ─────────────────────────────────────────────────────── */}
      <section className="relative z-10 mx-auto max-w-5xl text-center space-y-8 pt-4 pb-8">
        {/* Pitch Badge */}
        <div className="inline-flex items-center gap-2 rounded-full border border-blue-500/30 bg-blue-500/10 px-4 py-1.5 text-xs font-semibold text-blue-400 shadow-[0_0_20px_rgba(37,99,235,0.25)]">
          <Sparkles className="h-3.5 w-3.5" />
          <span>Next-Gen Enterprise Risk & Knowledge Graph Intelligence</span>
        </div>

        {/* Main Headline */}
        <div className="space-y-4">
          <h1 className="text-4xl sm:text-6xl lg:text-7xl font-black tracking-tight text-white leading-tight">
            Institutional Forensic Intelligence for{" "}
            <span className="bg-gradient-to-r from-blue-400 via-indigo-300 to-emerald-400 bg-clip-text text-transparent">
              High-Stakes Capital
            </span>
          </h1>
          <p className="mx-auto max-w-3xl text-base sm:text-lg text-slate-300 leading-relaxed font-normal">
            Continuous graph surveillance across MCA, SEBI, and exchange registries.
            Detect circular ownership, shell entities, and accounting distress in real time with our 7-factor ML engine.
          </p>
        </div>

        {/* ── Prominent Portal Quick Action Cards (Dashboard / Sign In / Register) ── */}
        <div className="mx-auto max-w-4xl w-full pt-2">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-left">
            {/* 1. Investor Dashboard Card */}
            <div className="glass-card glass-card-hover rounded-2xl p-5 border border-blue-500/30 bg-gradient-to-b from-blue-600/15 via-[#0F172A]/80 to-[#0B1120] flex flex-col justify-between space-y-3 relative group">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-500/20 text-blue-400 border border-blue-500/30">
                    <BarChart3 className="h-5 w-5" />
                  </div>
                  <span className="text-[10px] font-mono font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-300 border border-blue-500/40">
                    Live Analytics
                  </span>
                </div>
                <h3 className="text-base font-bold text-white group-hover:text-blue-300 transition-colors">
                  Investor Dashboard
                </h3>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Real-time portfolio surveillance, 4 financial charts, KPI metrics, and high-risk watchlist.
                </p>
              </div>

              <div className="pt-2 space-y-2">
                <Link href="/dashboard" className="w-full block">
                  <Button className="w-full h-9 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs shadow-[0_0_20px_rgba(37,99,235,0.4)] flex items-center justify-center gap-1.5">
                    <BarChart3 className="h-3.5 w-3.5" />
                    Open Dashboard
                    <ArrowRight className="h-3.5 w-3.5" />
                  </Button>
                </Link>
                {!isAuthenticated && (
                  <Button
                    type="button"
                    variant="outline"
                    onClick={handleQuickDemo}
                    disabled={isDemoLoading}
                    className="w-full h-8 rounded-xl border-amber-500/40 bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 font-bold text-[11px] flex items-center justify-center gap-1"
                  >
                    <Zap className="h-3 w-3 fill-amber-400 text-amber-400" />
                    {isDemoLoading ? "Authenticating..." : "1-Click Demo Login"}
                  </Button>
                )}
              </div>
            </div>

            {/* 2. Sign In Card */}
            <div className="glass-card glass-card-hover rounded-2xl p-5 border border-white/10 bg-gradient-to-b from-white/[0.04] via-[#0F172A]/80 to-[#0B1120] flex flex-col justify-between space-y-3 group">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">
                    <LogIn className="h-5 w-5" />
                  </div>
                  <span className="text-[10px] font-mono font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-slate-700/50 text-slate-300 border border-white/10">
                    Auth Portal
                  </span>
                </div>
                <h3 className="text-base font-bold text-white group-hover:text-indigo-300 transition-colors">
                  Institutional Sign In
                </h3>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Access authorized session with JWT tokens, encrypted endpoints, and user credentials.
                </p>
              </div>

              <div className="pt-2">
                <Link href="/login" className="w-full block">
                  <Button
                    variant="outline"
                    className="w-full h-9 rounded-xl border-white/20 bg-white/[0.06] hover:bg-white/[0.12] text-white font-bold text-xs flex items-center justify-center gap-1.5"
                  >
                    <LogIn className="h-3.5 w-3.5 text-indigo-400" />
                    Sign In to Portal
                    <ArrowRight className="h-3.5 w-3.5" />
                  </Button>
                </Link>
              </div>
            </div>

            {/* 3. Register Card */}
            <div className="glass-card glass-card-hover rounded-2xl p-5 border border-emerald-500/20 bg-gradient-to-b from-emerald-600/10 via-[#0F172A]/80 to-[#0B1120] flex flex-col justify-between space-y-3 group">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                    <UserPlus className="h-5 w-5" />
                  </div>
                  <span className="text-[10px] font-mono font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                    New Account
                  </span>
                </div>
                <h3 className="text-base font-bold text-white group-hover:text-emerald-300 transition-colors">
                  Create Account
                </h3>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Provision new risk analyst credentials to explore enterprise datasets and multi-hop graphs.
                </p>
              </div>

              <div className="pt-2">
                <Link href="/register" className="w-full block">
                  <Button
                    className="w-full h-9 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-[0_0_20px_rgba(16,185,129,0.3)] flex items-center justify-center gap-1.5"
                  >
                    <UserPlus className="h-3.5 w-3.5" />
                    Register Account
                    <ArrowRight className="h-3.5 w-3.5" />
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Global Search Bar Container */}
        <div className="mx-auto max-w-2xl w-full pt-4">
          <div className="glass-card rounded-2xl p-2 border border-white/10 shadow-2xl">
            <SearchBar placeholder="Search 50+ corporate registries (e.g., Apple, NVDA, Apex Cybernetics)..." />
          </div>
          <div className="mt-3 flex flex-wrap items-center justify-center gap-2 text-xs text-slate-400">
            <span className="font-semibold text-slate-300">Quick queries:</span>
            {["NVDA", "AAPL", "MSFT", "TSLA", "APEX", "NOVA"].map((ticker) => (
              <Link
                key={ticker}
                href={`/companies/${ticker}`}
                className="rounded-lg bg-white/[0.06] hover:bg-white/[0.12] px-2.5 py-1 font-mono text-[11px] font-bold text-blue-400 border border-white/[0.08] transition-all"
              >
                {ticker}
              </Link>
            ))}
          </div>
        </div>

        {/* Explore Hub Secondary Buttons */}
        <div className="flex flex-wrap justify-center items-center gap-3 pt-2">
          <Link href="/network?company=AAPL">
            <Button
              variant="outline"
              className="h-10 px-5 rounded-xl border-cyan-500/30 bg-[#0F172A]/80 hover:bg-cyan-500/15 text-cyan-300 font-bold text-xs gap-2 backdrop-blur-md"
            >
              <Network className="h-4 w-4 text-cyan-400" />
              Explore Neo4j Graph
            </Button>
          </Link>
          <Link href="/companies">
            <Button
              variant="ghost"
              className="h-10 px-5 rounded-xl text-slate-300 hover:text-white hover:bg-white/[0.06] text-xs font-semibold border border-white/10"
            >
              <Building2 className="h-4 w-4 mr-1.5 text-slate-400" />
              Browse 50 Companies Directory
            </Button>
          </Link>
        </div>
      </section>

      {/* ── Key Metrics Ticker Grid ─────────────────────────────────────────── */}
      <section className="relative z-10 mx-auto max-w-6xl w-full grid grid-cols-2 md:grid-cols-4 gap-4 py-6">
        {[
          { label: "Surveillance Universe", val: "50+ Blue-Chips", icon: Building2, color: "text-blue-400" },
          { label: "Graph Relationships", val: "5 Enterprise Edges", icon: Network, color: "text-cyan-400" },
          { label: "Weighted ML Formula", val: "7 Risk Dimensions", icon: ShieldCheck, color: "text-emerald-400" },
          { label: "Data Ingestion Feeds", val: "5 Active Connectors", icon: Database, color: "text-amber-400" },
        ].map((stat, idx) => {
          const Icon = stat.icon;
          return (
            <div
              key={idx}
              className="glass-card glass-card-hover rounded-2xl p-5 border border-white/[0.08] flex flex-col justify-between"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{stat.label}</span>
                <Icon className={`h-4 w-4 ${stat.color}`} />
              </div>
              <p className="mt-3 text-2xl font-black text-white font-mono tracking-tight">{stat.val}</p>
            </div>
          );
        })}
      </section>

      {/* ── 4 Core Pillars of OZARK Platform ─────────────────────────────────── */}
      <section className="relative z-10 mx-auto max-w-6xl w-full py-8 space-y-8">
        <div className="text-center space-y-2">
          <span className="text-xs font-bold uppercase tracking-widest text-blue-400">Pillars of Intelligence</span>
          <h2 className="text-3xl font-extrabold text-white tracking-tight">Fintech-Grade Risk Architecture</h2>
          <p className="text-xs sm:text-sm text-slate-400 max-w-xl mx-auto">
            Engineered for quantitative asset managers, compliance officers, and institutional risk committees.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Card 1: Risk Engine */}
          <div className="glass-card glass-card-hover rounded-3xl p-6 border border-white/[0.08] flex flex-col justify-between space-y-4">
            <div className="space-y-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-500/10 text-blue-400 border border-blue-500/20">
                <Shield className="h-6 w-6" />
              </div>
              <h3 className="text-lg font-bold text-white">7-Factor Risk Engine</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Calculates composite scores: Financial Health (25%), Compliance (20%), Fraud Indicators (20%), Market (15%), Network (10%), Sentiment (5%), and Rating (5%).
              </p>
            </div>
            <div className="pt-3 border-t border-white/[0.06] text-[11px] font-mono font-bold text-blue-400">
              GET /companies/&#123;id&#125;/risk
            </div>
          </div>

          {/* Card 2: Fraud Detection */}
          <div className="glass-card glass-card-hover rounded-3xl p-6 border border-white/[0.08] flex flex-col justify-between space-y-4">
            <div className="space-y-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-rose-500/10 text-rose-400 border border-rose-500/20">
                <ShieldAlert className="h-6 w-6" />
              </div>
              <h3 className="text-lg font-bold text-white">Forensic Anomaly Scanner</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Detects rapid director turnover, shell entity patterns, runaway debt expansion, and regulatory penalty histories with automated probabilistic grading.
              </p>
            </div>
            <div className="pt-3 border-t border-white/[0.06] text-[11px] font-mono font-bold text-rose-400">
              GET /companies/&#123;id&#125;/fraud
            </div>
          </div>

          {/* Card 3: Neo4j Knowledge Graph */}
          <div className="glass-card glass-card-hover rounded-3xl p-6 border border-white/[0.08] flex flex-col justify-between space-y-4">
            <div className="space-y-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                <Network className="h-6 w-6" />
              </div>
              <h3 className="text-lg font-bold text-white">Neo4j React Flow Graph</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Multi-hop graph visualizer across 4 entities (Company, Director, Bank, State) and 5 topological relationships (DIRECTS, OWNS, FUNDED_BY, OPERATES_IN, PARTNERS_WITH).
              </p>
            </div>
            <div className="pt-3 border-t border-white/[0.06] text-[11px] font-mono font-bold text-cyan-400">
              GET /api/network/&#123;id&#125;
            </div>
          </div>

          {/* Card 4: Connectors Pipeline */}
          <div className="glass-card glass-card-hover rounded-3xl p-6 border border-white/[0.08] flex flex-col justify-between space-y-4">
            <div className="space-y-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                <Database className="h-6 w-6" />
              </div>
              <h3 className="text-lg font-bold text-white">5 Unified Data Connectors</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Asynchronous unified interface for SEBI, Moneycontrol, Zerodha Kite, MCA, and SMC Global with parallel aggregation and mock/live switching.
              </p>
            </div>
            <div className="pt-3 border-t border-white/[0.06] text-[11px] font-mono font-bold text-emerald-400">
              ConnectorRegistry.aggregate()
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
