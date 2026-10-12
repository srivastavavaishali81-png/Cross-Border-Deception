"use client";

import { useState } from "react";
import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { TrendingUp, ArrowUpRight } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { REVENUE_TREND_DATA } from "@/lib/dashboard-mock-data";

interface CustomTooltipProps {
  active?: boolean;
  payload?: Array<{ value: number; name: string; color: string }>;
  label?: string;
}

function CustomTooltip({ active, payload, label }: CustomTooltipProps) {
  if (active && payload && payload.length) {
    const rev = payload.find((p) => p.name === "Revenue")?.value;
    const target = payload.find((p) => p.name === "Target")?.value;

    return (
      <div className="rounded-xl border border-border/80 bg-card/95 p-3.5 shadow-xl backdrop-blur-md text-xs space-y-1.5 min-w-[170px]">
        <p className="font-semibold text-foreground border-b border-border/50 pb-1">{label}</p>
        <div className="flex items-center justify-between gap-4">
          <span className="text-muted-foreground flex items-center gap-1.5">
            <span className="h-2 w-2 rounded-full bg-indigo-500" />
            Actual Revenue:
          </span>
          <span className="font-bold text-foreground font-mono">
            ${rev?.toLocaleString()}B
          </span>
        </div>
        {target && (
          <div className="flex items-center justify-between gap-4">
            <span className="text-muted-foreground flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-cyan-400" />
              Target / Baseline:
            </span>
            <span className="font-medium text-muted-foreground font-mono">
              ${target.toLocaleString()}B
            </span>
          </div>
        )}
      </div>
    );
  }
  return null;
}

export function RevenueTrendChart() {
  const [timeRange, setTimeRange] = useState<"Quarterly" | "Annual">("Quarterly");

  return (
    <Card className="border-border/60 bg-card/70 backdrop-blur-sm shadow-sm flex flex-col justify-between">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <TrendingUp className="h-4 w-4 text-indigo-400" />
            <CardTitle className="text-base font-semibold">Aggregate Revenue Trend</CardTitle>
          </div>
          <CardDescription className="text-xs">
            Combined portfolio revenue trajectory ($ Billions USD)
          </CardDescription>
        </div>

        <div className="flex items-center rounded-lg border border-border/60 bg-muted/40 p-0.5 text-xs">
          <button
            type="button"
            onClick={() => setTimeRange("Quarterly")}
            className={`rounded-md px-2.5 py-1 font-medium transition-colors ${
              timeRange === "Quarterly" ? "bg-primary text-primary-foreground shadow-sm" : "text-muted-foreground hover:text-foreground"
            }`}
          >
            Quarterly
          </button>
          <button
            type="button"
            onClick={() => setTimeRange("Annual")}
            className={`rounded-md px-2.5 py-1 font-medium transition-colors ${
              timeRange === "Annual" ? "bg-primary text-primary-foreground shadow-sm" : "text-muted-foreground hover:text-foreground"
            }`}
          >
            Annual
          </button>
        </div>
      </CardHeader>

      <CardContent className="pt-4 pb-4">
        <div className="h-[280px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart
              data={REVENUE_TREND_DATA}
              margin={{ top: 10, right: 10, left: -15, bottom: 0 }}
            >
              <defs>
                <linearGradient id="revenueGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0.0} />
                </linearGradient>
                <linearGradient id="targetGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.15} />
                  <stop offset="95%" stopColor="#06b6d4" stopOpacity={0.0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="hsl(var(--border) / 0.4)" />
              <XAxis
                dataKey="period"
                stroke="hsl(var(--muted-foreground))"
                fontSize={11}
                tickLine={false}
                axisLine={false}
              />
              <YAxis
                stroke="hsl(var(--muted-foreground))"
                fontSize={11}
                tickLine={false}
                axisLine={false}
                tickFormatter={(val) => `$${val}B`}
              />
              <Tooltip content={<CustomTooltip />} />
              <Area
                type="monotone"
                dataKey="revenue"
                name="Revenue"
                stroke="#6366f1"
                strokeWidth={2.5}
                fillOpacity={1}
                fill="url(#revenueGradient)"
              />
              <Area
                type="monotone"
                dataKey="targetRevenue"
                name="Target"
                stroke="#06b6d4"
                strokeWidth={1.5}
                strokeDasharray="4 4"
                fillOpacity={1}
                fill="url(#targetGradient)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="mt-4 flex items-center justify-between border-t border-border/40 pt-3 text-xs text-muted-foreground">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-indigo-500" />
              Actual Revenue
            </span>
            <span className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-cyan-400" />
              Baseline Target
            </span>
          </div>

          <span className="font-semibold text-emerald-500 flex items-center gap-0.5">
            +18.2% YoY Growth
            <ArrowUpRight className="h-3 w-3" />
          </span>
        </div>
      </CardContent>
    </Card>
  );
}
