"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { DollarSign } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { PROFIT_TREND_DATA } from "@/lib/dashboard-mock-data";

interface ProfitTooltipProps {
  active?: boolean;
  payload?: Array<{ value: number; name: string; color: string; payload: { profitMargin: number } }>;
  label?: string;
}

function ProfitTooltip({ active, payload, label }: ProfitTooltipProps) {
  if (active && payload && payload.length) {
    const margin = payload[0]?.payload?.profitMargin;
    return (
      <div className="rounded-xl border border-border/80 bg-card/95 p-3.5 shadow-xl backdrop-blur-md text-xs space-y-1.5 min-w-[190px]">
        <div className="flex items-center justify-between border-b border-border/50 pb-1">
          <p className="font-semibold text-foreground">Fiscal Year {label}</p>
          {margin && (
            <span className="font-bold text-emerald-500 bg-emerald-500/10 px-1.5 py-0.5 rounded text-[10px]">
              {margin}% Margin
            </span>
          )}
        </div>

        {payload.map((item, index) => (
          <div key={index} className="flex items-center justify-between gap-4">
            <span className="text-muted-foreground flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full" style={{ backgroundColor: item.color }} />
              {item.name}:
            </span>
            <span className="font-bold text-foreground font-mono">
              ${item.value.toLocaleString()}B
            </span>
          </div>
        ))}
      </div>
    );
  }
  return null;
}

export function ProfitTrendChart() {
  return (
    <Card className="border-border/60 bg-card/70 backdrop-blur-sm shadow-sm flex flex-col justify-between">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <DollarSign className="h-4 w-4 text-emerald-400" />
            <CardTitle className="text-base font-semibold">Profitability & Net Margin Trend</CardTitle>
          </div>
          <CardDescription className="text-xs">
            Gross Profit, EBITDA, and Net Income ($ Billions USD)
          </CardDescription>
        </div>

        <span className="rounded-full bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-0.5 text-xs font-bold text-emerald-500">
          25.8% Margin (2024)
        </span>
      </CardHeader>

      <CardContent className="pt-4 pb-4">
        <div className="h-[280px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={PROFIT_TREND_DATA}
              margin={{ top: 10, right: 10, left: -15, bottom: 0 }}
              barGap={4}
            >
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
              <Tooltip content={<ProfitTooltip />} />
              <Bar
                dataKey="grossProfit"
                name="Gross Profit"
                fill="#3b82f6"
                radius={[4, 4, 0, 0]}
              />
              <Bar
                dataKey="ebitda"
                name="EBITDA"
                fill="#8b5cf6"
                radius={[4, 4, 0, 0]}
              />
              <Bar
                dataKey="netIncome"
                name="Net Income"
                fill="#10b981"
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="mt-4 flex flex-wrap items-center justify-between border-t border-border/40 pt-3 text-xs text-muted-foreground gap-2">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-blue-500" />
              Gross Profit
            </span>
            <span className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-violet-500" />
              EBITDA
            </span>
            <span className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-emerald-500" />
              Net Income
            </span>
          </div>

          <span className="font-semibold text-foreground">
            5-Year Net Income CAGR: <strong className="text-emerald-500">+19.8%</strong>
          </span>
        </div>
      </CardContent>
    </Card>
  );
}
