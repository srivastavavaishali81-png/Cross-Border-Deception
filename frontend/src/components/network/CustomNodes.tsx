"use client";

import { memo } from "react";
import { Handle, Position } from "@xyflow/react";
import { Building2, User, Landmark, MapPin, ShieldAlert, ShieldCheck } from "lucide-react";
import type { GraphNodeData } from "@/types/network";

interface CustomNodeProps {
  data: GraphNodeData;
  selected?: boolean;
}

export const CompanyNode = memo(({ data, selected }: CustomNodeProps) => {
  const ticker = (data.properties.ticker as string) || data.label;
  const isRoot = Boolean(data.properties.is_root);
  const risk = data.properties.risk_score as number | undefined;

  return (
    <div
      className={`relative min-w-[190px] rounded-2xl border bg-card/95 p-3.5 shadow-xl backdrop-blur-md transition-all duration-200 ${
        isRoot
          ? "border-primary ring-2 ring-primary/40 bg-gradient-to-br from-card via-card/90 to-primary/10"
          : "border-indigo-500/30 hover:border-indigo-500/60"
      } ${selected ? "ring-2 ring-cyan-400 scale-105" : ""}`}
    >
      <Handle type="target" position={Position.Top} className="!bg-indigo-400 !w-2.5 !h-2.5" />

      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-bold text-xs">
            <Building2 className="h-4 w-4" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="font-bold text-xs text-foreground leading-none">{ticker}</span>
              {isRoot && (
                <span className="rounded bg-primary/20 text-primary px-1 py-0.2 text-[9px] font-bold">
                  FOCUS
                </span>
              )}
            </div>
            <p className="text-[11px] text-muted-foreground truncate max-w-[110px] mt-0.5" title={data.label}>
              {data.label}
            </p>
          </div>
        </div>

        {risk !== undefined && (
          <span
            className={`rounded-full border px-1.5 py-0.5 text-[9px] font-bold ${
              risk < 25
                ? "bg-emerald-500/10 text-emerald-500 border-emerald-500/20"
                : risk < 50
                ? "bg-amber-500/10 text-amber-500 border-amber-500/20"
                : "bg-rose-500/10 text-rose-500 border-rose-500/20"
            }`}
          >
            {risk}
          </span>
        )}
      </div>

      <Handle type="source" position={Position.Bottom} className="!bg-indigo-400 !w-2.5 !h-2.5" />
    </div>
  );
});
CompanyNode.displayName = "CompanyNode";

export const DirectorNode = memo(({ data, selected }: CustomNodeProps) => {
  const role = (data.properties.role as string) || "Director";
  const tenure = data.properties.tenure_years as number | undefined;

  return (
    <div
      className={`relative min-w-[170px] rounded-2xl border border-violet-500/30 bg-card/95 p-3 shadow-lg backdrop-blur-md transition-all duration-200 hover:border-violet-500/60 ${
        selected ? "ring-2 ring-cyan-400 scale-105" : ""
      }`}
    >
      <Handle type="target" position={Position.Top} className="!bg-violet-400 !w-2.5 !h-2.5" />

      <div className="flex items-center gap-2.5">
        <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-violet-500/10 text-violet-400 border border-violet-500/20">
          <User className="h-4 w-4" />
        </div>
        <div className="overflow-hidden">
          <p className="font-semibold text-xs text-foreground truncate" title={data.label}>
            {data.label}
          </p>
          <p className="text-[10px] text-muted-foreground truncate mt-0.5">
            {role} {tenure ? `(${tenure}y)` : ""}
          </p>
        </div>
      </div>

      <Handle type="source" position={Position.Bottom} className="!bg-violet-400 !w-2.5 !h-2.5" />
    </div>
  );
});
DirectorNode.displayName = "DirectorNode";

export const BankNode = memo(({ data, selected }: CustomNodeProps) => {
  const tier = (data.properties.tier as string) || "Bank";
  const facility = data.properties.facility_m as number | undefined;

  return (
    <div
      className={`relative min-w-[170px] rounded-2xl border border-emerald-500/30 bg-card/95 p-3 shadow-lg backdrop-blur-md transition-all duration-200 hover:border-emerald-500/60 ${
        selected ? "ring-2 ring-cyan-400 scale-105" : ""
      }`}
    >
      <Handle type="target" position={Position.Top} className="!bg-emerald-400 !w-2.5 !h-2.5" />

      <div className="flex items-center gap-2.5">
        <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          <Landmark className="h-4 w-4" />
        </div>
        <div className="overflow-hidden">
          <p className="font-semibold text-xs text-foreground truncate" title={data.label}>
            {data.label}
          </p>
          <p className="text-[10px] text-muted-foreground truncate mt-0.5">
            {tier} {facility ? `• $${(facility / 1000).toFixed(1)}B` : ""}
          </p>
        </div>
      </div>

      <Handle type="source" position={Position.Bottom} className="!bg-emerald-400 !w-2.5 !h-2.5" />
    </div>
  );
});
BankNode.displayName = "BankNode";

export const StateNode = memo(({ data, selected }: CustomNodeProps) => {
  const code = (data.properties.code as string) || data.label;

  return (
    <div
      className={`relative min-w-[150px] rounded-2xl border border-cyan-500/30 bg-card/95 p-3 shadow-lg backdrop-blur-md transition-all duration-200 hover:border-cyan-500/60 ${
        selected ? "ring-2 ring-cyan-400 scale-105" : ""
      }`}
    >
      <Handle type="target" position={Position.Top} className="!bg-cyan-400 !w-2.5 !h-2.5" />

      <div className="flex items-center gap-2.5">
        <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-bold text-xs">
          <MapPin className="h-4 w-4" />
        </div>
        <div className="overflow-hidden">
          <p className="font-bold text-xs text-foreground truncate">
            {code}
          </p>
          <p className="text-[10px] text-muted-foreground truncate mt-0.5" title={data.label}>
            {data.label}
          </p>
        </div>
      </div>

      <Handle type="source" position={Position.Bottom} className="!bg-cyan-400 !w-2.5 !h-2.5" />
    </div>
  );
});
StateNode.displayName = "StateNode";
