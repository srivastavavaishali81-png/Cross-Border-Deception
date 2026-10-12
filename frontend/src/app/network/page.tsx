"use client";

import { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import {
  ArrowLeft,
  Building2,
  Filter,
  GitBranch,
  Info,
  Landmark,
  Layers,
  Loader2,
  MapPin,
  Network,
  RefreshCw,
  Search,
  Share2,
  Shield,
  Sparkles,
  User,
  X,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { SearchBar } from "@/components/SearchBar";
import { ErrorState } from "@/components/ui/ErrorState";
import { NetworkGraphCanvas } from "@/components/network/NetworkGraphCanvas";
import { fetchCompanyNetwork } from "@/lib/network";
import type { GraphNodeData, NetworkGraphResponse } from "@/types/network";

const PRESET_COMPANIES = [
  { ticker: "AAPL", name: "Apple Inc." },
  { ticker: "NVDA", name: "NVIDIA Corp." },
  { ticker: "MSFT", name: "Microsoft Corp." },
  { ticker: "TSLA", name: "Tesla Inc." },
];

function NetworkVisualizerContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const companyParam = searchParams.get("company") || "AAPL";

  const [graphData, setGraphData] = useState<NetworkGraphResponse | null>(null);
  const [selectedNode, setSelectedNode] = useState<GraphNodeData | null>(null);
  const [filterEntity, setFilterEntity] = useState<string>("all");
  const [filterRel, setFilterRel] = useState<string>("all");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadGraph = () => {
    setIsLoading(true);
    setError(null);
    fetchCompanyNetwork(companyParam)
      .then((data) => {
        setGraphData(data);
        setSelectedNode(null);
      })
      .catch((err) => {
        setError(err.message || "Failed to load relationship graph");
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  useEffect(() => {
    loadGraph();
  }, [companyParam]);

  const handleSelectCompany = (ticker: string) => {
    router.push(`/network?company=${ticker}`);
  };

  return (
    <div className="min-h-screen pb-20">
      {/* ── Main Content Container ────────────────────────────────────────── */}
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 space-y-6">
        {/* Header Hero & Company Presets */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-white/[0.08] pb-5">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-mono font-bold uppercase tracking-widest text-cyan-400">
                Neo4j Topology Engine
              </span>
              <span className="rounded-full bg-cyan-500/10 border border-cyan-500/30 px-2.5 py-0.5 text-xs font-mono font-bold text-cyan-400 shadow-[0_0_15px_rgba(6,182,212,0.2)]">
                Multi-Hop Graph
              </span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-black tracking-tight text-white flex items-center gap-2.5">
              <Network className="h-8 w-8 text-cyan-400" />
              Enterprise Relationship Network
            </h1>
            <p className="text-xs sm:text-sm text-slate-400">
              Surveilling 4 entity nodes (Company, Director, Bank, State) across 5 topological relationships.
            </p>
          </div>

          {/* Quick Preset Badges */}
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs text-slate-400 font-semibold mr-1">Focus Asset:</span>
            {PRESET_COMPANIES.map((item) => (
              <button
                key={item.ticker}
                type="button"
                onClick={() => handleSelectCompany(item.ticker)}
                className={`rounded-xl px-3.5 py-1.5 text-xs font-mono font-bold transition-all border ${
                  companyParam.toUpperCase() === item.ticker
                    ? "bg-blue-600 text-white border-blue-500 shadow-[0_0_15px_rgba(37,99,235,0.4)]"
                    : "bg-[#0F172A] text-slate-400 hover:text-white border-white/10 hover:border-white/20"
                }`}
              >
                {item.ticker}
              </button>
            ))}
          </div>
        </div>

        {/* Global Search Bar */}
        <div className="glass-card rounded-2xl p-2 border border-white/10">
          <SearchBar
            initialQuery={companyParam}
            placeholder="Search company network (e.g. AAPL, NVDA, MSFT, TSLA)..."
            onSearch={(q) => {
              if (q) handleSelectCompany(q);
            }}
          />
        </div>

        {/* ── Filter Bar & Graph Topology Metrics ────────────────────────────── */}
        <div className="glass-card flex flex-wrap items-center justify-between gap-4 rounded-3xl p-4 border border-white/[0.08] text-xs">
          {/* Entity & Relationship Filters */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center gap-1.5 text-slate-400 font-semibold">
              <Filter className="h-3.5 w-3.5 text-blue-400" />
              <span>Nodes:</span>
            </div>

            <div className="flex flex-wrap items-center gap-1.5">
              {[
                { id: "all", label: "All Nodes" },
                { id: "Company", label: "🏢 Company" },
                { id: "Director", label: "👤 Director" },
                { id: "Bank", label: "🏛️ Bank" },
                { id: "State", label: "📍 State" },
              ].map((tab) => (
                <button
                  key={tab.id}
                  type="button"
                  onClick={() => setFilterEntity(tab.id)}
                  className={`rounded-xl px-3 py-1 text-xs font-bold transition-all border ${
                    filterEntity === tab.id
                      ? "bg-blue-600 text-white border-blue-500 shadow-[0_0_15px_rgba(37,99,235,0.3)]"
                      : "bg-[#0B1120] text-slate-400 hover:text-white border-white/10"
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            <div className="h-4 w-px bg-white/10 hidden md:block mx-1" />

            <div className="flex items-center gap-1.5 text-slate-400 font-semibold">
              <span>Edges:</span>
              <select
                value={filterRel}
                onChange={(e) => setFilterRel(e.target.value)}
                aria-label="Filter relationships"
                className="h-8 rounded-xl border border-white/10 bg-[#0B1120] px-3 text-xs font-semibold text-white focus:outline-none cursor-pointer"
              >
                <option value="all">All Relationships</option>
                <option value="DIRECTS">DIRECTS (Governance)</option>
                <option value="OWNS">OWNS (Shareholding)</option>
                <option value="FUNDED_BY">FUNDED_BY (Credit/Debt)</option>
                <option value="OPERATES_IN">OPERATES_IN (Jurisdiction)</option>
                <option value="PARTNERS_WITH">PARTNERS_WITH (Alliance)</option>
              </select>
            </div>
          </div>

          {/* Graph Metrics Summary */}
          {graphData && (
            <div className="flex flex-wrap items-center gap-4 text-xs font-medium text-slate-400 border-t md:border-t-0 pt-2 md:pt-0 w-full md:w-auto">
              <span>
                Nodes: <strong className="text-white font-mono">{graphData.metrics.total_nodes}</strong>
              </span>
              <span>
                Edges: <strong className="text-white font-mono">{graphData.metrics.total_edges}</strong>
              </span>
              <span>
                Density: <strong className="text-cyan-400 font-mono font-bold">{graphData.metrics.density}</strong>
              </span>
              <span>
                Centrality: <strong className="text-emerald-400 font-mono font-bold">{graphData.metrics.centrality_score}</strong>
              </span>
            </div>
          )}
        </div>

        {/* ── Graph Canvas & Inspector Grid ─────────────────────────────────── */}
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-4">
          {/* Main React Flow Graph Canvas */}
          <div className="lg:col-span-3">
            {isLoading ? (
              <div className="glass-card flex h-[650px] flex-col items-center justify-center rounded-3xl border border-dashed border-white/10 p-12 text-center space-y-4">
                <Loader2 className="h-10 w-10 animate-spin text-cyan-400" />
                <p className="text-xs font-mono font-bold text-slate-300">
                  Traversing Neo4j relationship graph for {companyParam}...
                </p>
              </div>
            ) : error ? (
              <ErrorState
                title="Graph Pipeline Error"
                message={error}
                onRetry={loadGraph}
                className="h-[650px]"
              />
            ) : graphData ? (
              <NetworkGraphCanvas
                graphData={graphData}
                onSelectNode={setSelectedNode}
                filterEntityType={filterEntity}
                filterRelationshipType={filterRel}
              />
            ) : (
              <div className="glass-card flex h-[650px] flex-col items-center justify-center rounded-3xl border border-dashed border-white/10 p-12 text-center">
                <p className="text-xs text-slate-400">No graph data found for {companyParam}.</p>
              </div>
            )}
          </div>

          {/* Node Inspector Sidebar */}
          <div className="lg:col-span-1 space-y-4">
            <Card className="glass-card rounded-3xl border border-white/[0.08] shadow-xl h-full flex flex-col justify-between">
              <CardHeader className="pb-3 border-b border-white/[0.06]">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Info className="h-4 w-4 text-blue-400" />
                    <CardTitle className="text-sm font-bold text-white">Entity Inspector</CardTitle>
                  </div>
                  {selectedNode && (
                    <button
                      type="button"
                      onClick={() => setSelectedNode(null)}
                      className="rounded-full p-1 text-slate-400 hover:bg-white/10 hover:text-white"
                      title="Deselect"
                    >
                      <X className="h-3.5 w-3.5" />
                    </button>
                  )}
                </div>
                <CardDescription className="text-[11px] text-slate-400">
                  {selectedNode
                    ? `Inspecting ${selectedNode.type} metadata`
                    : "Select any node in the canvas to inspect"}
                </CardDescription>
              </CardHeader>

              <CardContent className="pt-4 flex-1 space-y-4 text-xs">
                {selectedNode ? (
                  <div className="space-y-4">
                    <div className="rounded-2xl bg-[#0B1120]/80 p-4 border border-white/[0.06] space-y-1">
                      <span
                        className={`rounded-lg px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-wider ${
                          selectedNode.type === "Company"
                            ? "bg-blue-500/20 text-blue-400 border border-blue-500/30"
                            : selectedNode.type === "Director"
                            ? "bg-purple-500/20 text-purple-400 border border-purple-500/30"
                            : selectedNode.type === "Bank"
                            ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                            : "bg-amber-500/20 text-amber-400 border border-amber-500/30"
                        }`}
                      >
                        {selectedNode.type}
                      </span>
                      <h4 className="font-black text-base text-white mt-2">{selectedNode.label}</h4>
                    </div>

                    <div className="space-y-2">
                      <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-400">
                        Node Attributes
                      </span>
                      <dl className="space-y-2 rounded-2xl bg-[#0B1120]/60 p-3.5 border border-white/[0.05] text-xs">
                        {Object.entries(selectedNode.properties).map(([key, val]) => (
                          <div key={key} className="flex justify-between gap-2 border-b border-white/[0.04] pb-1.5 last:border-b-0">
                            <dt className="text-slate-400 capitalize font-medium">{key.replace(/_/g, " ")}</dt>
                            <dd className="font-mono text-slate-200 font-bold truncate max-w-[130px]" title={String(val)}>
                              {String(val)}
                            </dd>
                          </div>
                        ))}
                      </dl>
                    </div>

                    {selectedNode.type === "Company" && Boolean(selectedNode.properties.ticker) && (
                      <Link href={`/companies/${String(selectedNode.properties.ticker)}`}>
                        <Button size="sm" className="w-full text-xs font-bold rounded-xl mt-2 bg-blue-600 hover:bg-blue-500 text-white shadow-[0_0_20px_rgba(37,99,235,0.4)]">
                          View Full Company Analysis
                        </Button>
                      </Link>
                    )}
                  </div>
                ) : (
                  <div className="flex flex-col items-center justify-center py-16 text-center text-slate-400 space-y-3">
                    <Sparkles className="h-8 w-8 text-cyan-400/50" />
                    <p className="text-xs font-bold text-white">Interactive Graph Explorer</p>
                    <p className="text-[11px] text-slate-400 max-w-[190px] leading-relaxed">
                      Select any Director, Bank, State, or Company node to reveal governance connections.
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}

export default function NetworkPage() {
  return (
    <Suspense
      fallback={
        <div className="flex min-h-screen items-center justify-center">
          <Loader2 className="h-8 w-8 animate-spin text-cyan-400" />
        </div>
      }
    >
      <NetworkVisualizerContent />
    </Suspense>
  );
}
