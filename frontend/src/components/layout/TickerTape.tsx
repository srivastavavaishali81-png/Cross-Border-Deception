"use client";

import React from "react";
import Link from "next/link";
import { TrendingUp, ShieldAlert, Activity } from "lucide-react";

interface TickerItem {
  symbol: string;
  name: string;
  riskScore: number;
  riskLevel: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  change: string;
  isPositive: boolean;
}

const SAMPLE_TICKERS: TickerItem[] = [
  { symbol: "NVDA", name: "NVIDIA Corp", riskScore: 18.4, riskLevel: "LOW", change: "+3.2%", isPositive: true },
  { symbol: "AAPL", name: "Apple Inc", riskScore: 12.5, riskLevel: "LOW", change: "+1.1%", isPositive: true },
  { symbol: "MSFT", name: "Microsoft", riskScore: 14.8, riskLevel: "LOW", change: "+0.8%", isPositive: true },
  { symbol: "TSLA", name: "Tesla Inc", riskScore: 42.0, riskLevel: "MEDIUM", change: "-2.4%", isPositive: false },
  { symbol: "APEX", name: "Apex Cybernetics", riskScore: 16.5, riskLevel: "LOW", change: "+4.6%", isPositive: true },
  { symbol: "QNTM", name: "QuantumEdge", riskScore: 38.6, riskLevel: "MEDIUM", change: "+1.9%", isPositive: true },
  { symbol: "NOVA", name: "Nova BioHealth", riskScore: 78.4, riskLevel: "CRITICAL", change: "-8.2%", isPositive: false },
  { symbol: "VRTX", name: "Vortex Aero", riskScore: 22.1, riskLevel: "LOW", change: "+0.5%", isPositive: true },
];

export function TickerTape() {
  const items = [...SAMPLE_TICKERS, ...SAMPLE_TICKERS]; // Duplicate for seamless infinite loop

  return (
    <div className="relative w-full overflow-hidden border-b border-white/[0.06] bg-[#0B1120]/90 backdrop-blur-md py-1.5 z-30">
      <div className="flex items-center">
        {/* Left Live Badge */}
        <div className="flex shrink-0 items-center gap-1.5 px-4 text-[10px] font-bold tracking-widest text-emerald-400 uppercase border-r border-white/10 bg-[#0F172A]/90 z-10">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span>LIVE INTEL</span>
        </div>

        {/* Scrolling Ticker Stream */}
        <div className="flex whitespace-nowrap animate-ticker hover:[animation-play-state:paused]">
          {items.map((item, idx) => (
            <Link
              key={`${item.symbol}-${idx}`}
              href={`/companies/${item.symbol}`}
              className="inline-flex items-center gap-2.5 px-4 text-xs font-medium text-slate-300 hover:text-white transition-colors cursor-pointer"
            >
              <span className="font-bold text-white tracking-wider">{item.symbol}</span>
              <span className="text-[11px] text-slate-400 hidden sm:inline">{item.name}</span>
              
              <span
                className={`text-[10px] font-mono font-bold px-1.5 py-0.5 rounded border ${
                  item.riskLevel === "LOW"
                    ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                    : item.riskLevel === "MEDIUM"
                    ? "bg-amber-500/10 text-amber-400 border-amber-500/20"
                    : "bg-rose-500/10 text-rose-400 border-rose-500/20"
                }`}
              >
                RS {item.riskScore.toFixed(1)}
              </span>

              <span className={`text-[11px] font-mono ${item.isPositive ? "text-emerald-400" : "text-rose-400"}`}>
                {item.change}
              </span>

              <span className="text-slate-600 font-normal">|</span>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
