/**
 * (auth) group layout — shared shell for login & register pages.
 * Fintech-grade split panel with ambient glows & institutional security highlights.
 */

import Link from "next/link";
import { Shield, Sparkles, Network, Activity, Database, CheckCircle2 } from "lucide-react";

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-[calc(100vh-100px)]">
      {/* ── Left panel — brand / hero ───────────────────────────────────── */}
      <div className="relative hidden w-1/2 overflow-hidden lg:flex lg:flex-col lg:items-center lg:justify-center p-12 border-r border-white/[0.06]">
        {/* Animated ambient blooms */}
        <div className="absolute h-[500px] w-[500px] animate-blob rounded-full bg-blue-600/15 blur-[120px]" />
        <div className="absolute h-[400px] w-[400px] animate-blob animation-delay-2000 rounded-full bg-indigo-600/10 blur-[130px]" />

        {/* Content */}
        <div className="relative z-10 flex flex-col items-start gap-8 max-w-lg text-left">
          <div className="flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-700 shadow-[0_0_25px_rgba(37,99,235,0.4)]">
              <Shield className="h-6 w-6 text-white" />
            </div>
            <div>
              <span className="font-mono font-black text-2xl tracking-wider text-white">OZARK</span>
              <p className="text-xs text-blue-400 font-semibold tracking-wide">ENTERPRISE RISK INTELLIGENCE</p>
            </div>
          </div>

          <div className="space-y-3">
            <h2 className="text-3xl font-black text-white tracking-tight leading-tight">
              Institutional Forensic Surveillance Portal
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">
              Continuous graph monitoring, automated SEBI/MCA compliance extraction, and weighted ML risk assessment for investment teams.
            </p>
          </div>

          {/* Feature highlights */}
          <div className="space-y-3 w-full">
            {[
              { title: "Neo4j Multi-Hop Knowledge Graph", desc: "Maps circular holdings, shell companies & director interlocks." },
              { title: "Calibrated 7-Factor Risk Engine", desc: "Financial health, compliance, fraud probability & sentiment." },
              { title: "Deterministic Natural Language AI", desc: "Automated clear thesis summaries for risk committees." },
            ].map((item, idx) => (
              <div
                key={idx}
                className="glass-card rounded-2xl p-4 border border-white/[0.07] flex items-start gap-3"
              >
                <CheckCircle2 className="h-4 w-4 text-blue-400 shrink-0 mt-0.5" />
                <div className="space-y-0.5 text-xs">
                  <h4 className="font-bold text-white">{item.title}</h4>
                  <p className="text-[11px] text-slate-400 leading-relaxed">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ── Right panel — form ───────────────────────────────────────────── */}
      <div className="flex flex-1 flex-col items-center justify-center px-6 py-12">
        <div className="w-full max-w-md">{children}</div>
      </div>
    </div>
  );
}
