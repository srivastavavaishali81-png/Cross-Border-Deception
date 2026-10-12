"use client";

import { useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { Layers } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { SECTOR_ANALYSIS_DATA } from "@/lib/dashboard-mock-data";

interface SectorTooltipProps {
  active?: boolean;
  payload?: Array<{ payload: { sector: string; companyCount: number; marketCap: number; avgRiskScore: number } }>;
}

function SectorTooltip({ active, payload }: SectorTooltipProps) {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="rounded-xl border border-border/80 bg-card/95 p-3.5 shadow-xl backdrop-blur-md text-xs space-y-1.5 min-w-[200px]">
        <p className="font-bold text-foreground border-b border-border/50 pb-1">{data.sector}</p>
        <div className="flex items-center justify-between gap-4">
          <span className="text-muted-foreground">Market Cap:</span>
          <span className="font-bold text-foreground font-mono">
            ${data.marketCap >= 1000 ? `${(data.marketCap / 1000).toFixed(2)}T` : `${data.marketCap}B`}
          </span>
        </div>
        <div className="flex items-center justify-between gap-4">
          <span className="text-muted-foreground">Tracked Companies:</span>
          <span className="font-semibold text-foreground font-mono">{data.companyCount}</span>
        </div>
        <div className="flex items-center justify-between gap-4">
          <span className="text-muted-foreground">Avg Risk Score:</span>
          <span className="font-bold text-amber-500 font-mono">{data.avgRiskScore} / 100</span>
        </div>
      </div>
    );
  }
  return null;
}

export function SectorAnalysisChart() {
  const [metric, setMetric] = useState<"marketCap" | "avgRiskScore">("marketCap");

  return (
    <Card className="border-border/60 bg-card/70 backdrop-blur-sm shadow-sm flex flex-col justify-between">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <Layers className="h-4 w-4 text-cyan-400" />
            <CardTitle className="text-base font-semibold">Sector Concentration Analysis</CardTitle>
          </div>
          <CardDescription className="text-xs">
            {metric === "marketCap"
              ? "Aggregate Market Capitalization by sector ($ Billions USD)"
              : "Average Risk Vulnerability Score by industry sector"}
          </CardDescription>
        </div>

        <div className="flex items-center rounded-lg border border-border/60 bg-muted/40 p-0.5 text-xs">
          <button
            type="button"
            onClick={() => setMetric("marketCap")}
            className={`rounded-md px-2.5 py-1 font-medium transition-colors ${
              metric === "marketCap" ? "bg-primary text-primary-foreground shadow-sm" : "text-muted-foreground hover:text-foreground"
            }`}
          >
            Market Cap
          </button>
          <button
            type="button"
            onClick={() => setMetric("avgRiskScore")}
            className={`rounded-md px-2.5 py-1 font-medium transition-colors ${
              metric === "avgRiskScore" ? "bg-primary text-primary-foreground shadow-sm" : "text-muted-foreground hover:text-foreground"
            }`}
          >
            Risk Score
          </button>
        </div>
      </CardHeader>

      <CardContent className="pt-4 pb-4">
        <div className="h-[280px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={SECTOR_ANALYSIS_DATA}
              layout="vertical"
              margin={{ top: 5, right: 20, left: 35, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="hsl(var(--border) / 0.4)" />
              <XAxis
                type="number"
                stroke="hsl(var(--muted-foreground))"
                fontSize={11}
                tickLine={false}
                axisLine={false}
                tickFormatter={(val) => (metric === "marketCap" ? `$${val}B` : `${val}`)}
              />
              <YAxis
                type="category"
                dataKey="sector"
                stroke="hsl(var(--muted-foreground))"
                fontSize={11}
                tickLine={false}
                axisLine={false}
                width={85}
              />
              <Tooltip content={<SectorTooltip />} />
              <Bar
                dataKey={metric}
                radius={[0, 6, 6, 0]}
                name={metric === "marketCap" ? "Market Cap" : "Avg Risk Score"}
              >
                {SECTOR_ANALYSIS_DATA.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={metric === "marketCap" ? entry.color : entry.avgRiskScore > 35 ? "#f59e0b" : "#10b981"}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="mt-4 flex items-center justify-between border-t border-border/40 pt-3 text-xs text-muted-foreground">
          <span>
            Top Concentration: <strong className="text-foreground font-semibold">Technology (48.5% of AUM)</strong>
          </span>
          <span className="font-medium text-primary">
            8 Major Industry Sectors
          </span>
        </div>
      </CardContent>
    </Card>
  );
}
