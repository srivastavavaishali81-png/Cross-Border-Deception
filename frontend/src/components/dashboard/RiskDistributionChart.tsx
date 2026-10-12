"use client";

import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import { Shield, ShieldAlert } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { RISK_DISTRIBUTION_DATA } from "@/lib/dashboard-mock-data";

interface RiskTooltipProps {
  active?: boolean;
  payload?: Array<{ payload: { name: string; value: number; percentage: number; color: string; description: string } }>;
}

function RiskTooltip({ active, payload }: RiskTooltipProps) {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="rounded-xl border border-border/80 bg-card/95 p-3.5 shadow-xl backdrop-blur-md text-xs space-y-1.5 min-w-[190px]">
        <div className="flex items-center justify-between border-b border-border/50 pb-1">
          <p className="font-bold text-foreground flex items-center gap-1.5">
            <span className="h-2 w-2 rounded-full" style={{ backgroundColor: data.color }} />
            {data.name}
          </p>
          <span className="font-semibold text-foreground font-mono">
            {data.percentage}%
          </span>
        </div>
        <p className="text-muted-foreground text-[11px] leading-tight pt-1">
          {data.value} of 50 companies ({data.description})
        </p>
      </div>
    );
  }
  return null;
}

export function RiskDistributionChart() {
  const totalCompanies = RISK_DISTRIBUTION_DATA.reduce((acc, curr) => acc + curr.value, 0);

  return (
    <Card className="border-border/60 bg-card/70 backdrop-blur-sm shadow-sm flex flex-col justify-between">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <Shield className="h-4 w-4 text-emerald-400" />
            <CardTitle className="text-base font-semibold">Risk Distribution</CardTitle>
          </div>
          <CardDescription className="text-xs">
            Classification of 50 tracked enterprises by risk severity tier
          </CardDescription>
        </div>

        <span className="rounded-full bg-primary/10 border border-primary/20 px-2.5 py-0.5 text-xs font-bold text-primary">
          68% Low Risk
        </span>
      </CardHeader>

      <CardContent className="pt-2 pb-4">
        <div className="relative h-[240px] w-full flex items-center justify-center">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Tooltip content={<RiskTooltip />} />
              <Pie
                data={RISK_DISTRIBUTION_DATA}
                cx="50%"
                cy="50%"
                innerRadius={65}
                outerRadius={95}
                paddingAngle={4}
                dataKey="value"
              >
                {RISK_DISTRIBUTION_DATA.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={entry.color}
                    stroke="hsl(var(--card))"
                    strokeWidth={2}
                  />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>

          {/* Center Callout */}
          <div className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center text-center">
            <span className="text-2xl font-black text-foreground leading-none">{totalCompanies}</span>
            <span className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mt-0.5">
              Enterprises
            </span>
          </div>
        </div>

        {/* Legend Grid */}
        <div className="mt-3 grid grid-cols-2 gap-2 border-t border-border/40 pt-3 text-xs">
          {RISK_DISTRIBUTION_DATA.map((item) => (
            <div
              key={item.name}
              className="flex items-center justify-between rounded-lg bg-muted/30 px-2.5 py-1.5 border border-border/30"
            >
              <div className="flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full" style={{ backgroundColor: item.color }} />
                <span className="font-medium text-muted-foreground text-[11px]">{item.name}</span>
              </div>
              <span className="font-bold text-foreground font-mono text-[11px]">
                {item.value} ({item.percentage}%)
              </span>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
