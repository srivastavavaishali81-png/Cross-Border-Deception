"use client";

import { LucideIcon, TrendingDown, TrendingUp } from "lucide-react";
import { Card, CardContent, CardHeader } from "@/components/ui/card";

interface MetricCardProps {
  title: string;
  value: string | number;
  change: string;
  isPositive?: boolean;
  description: string;
  badge?: string;
  icon: LucideIcon;
  iconColor: string;
  iconBg: string;
}

export function MetricCard({
  title,
  value,
  change,
  isPositive = true,
  description,
  badge,
  icon: Icon,
  iconColor,
  iconBg,
}: MetricCardProps) {
  return (
    <Card className="group relative overflow-hidden border-border/60 bg-card/70 backdrop-blur-sm shadow-sm transition-all duration-300 hover:border-border hover:shadow-md">
      <div className="absolute -right-6 -top-6 h-24 w-24 rounded-full bg-primary/5 blur-2xl transition-all group-hover:bg-primary/10" />

      <CardHeader className="flex flex-row items-center justify-between pb-2 pt-5">
        <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          {title}
        </span>
        <div className={`rounded-xl p-2.5 transition-transform duration-300 group-hover:scale-105 ${iconBg}`}>
          <Icon className={`h-4 w-4 ${iconColor}`} />
        </div>
      </CardHeader>

      <CardContent className="space-y-3 pb-5">
        <div className="flex items-baseline justify-between">
          <span className="text-3xl font-extrabold tracking-tight text-foreground">
            {value}
          </span>
          {badge && (
            <span className="rounded-full border border-border/60 bg-muted/40 px-2 py-0.5 text-[10px] font-semibold text-muted-foreground">
              {badge}
            </span>
          )}
        </div>

        <div className="flex items-center justify-between border-t border-border/40 pt-3 text-xs">
          <span className="text-muted-foreground truncate">{description}</span>
          <span
            className={`inline-flex items-center gap-1 font-semibold shrink-0 ${
              isPositive ? "text-emerald-500" : "text-amber-500"
            }`}
          >
            {isPositive ? (
              <TrendingUp className="h-3.5 w-3.5" />
            ) : (
              <TrendingDown className="h-3.5 w-3.5" />
            )}
            {change}
          </span>
        </div>
      </CardContent>
    </Card>
  );
}
