"use client";

import { Suspense, useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import {
  Building2,
  ChevronLeft,
  ChevronRight,
  Filter,
  Layers,
  LayoutGrid,
  Loader2,
  Network,
  RefreshCw,
  Search,
  SlidersHorizontal,
  Sparkles,
  TrendingUp,
  X,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { SearchBar } from "@/components/SearchBar";
import { CompanyCard } from "@/components/CompanyCard";
import { CompanyFilters } from "@/components/CompanyFilters";
import { CompanyCardSkeleton } from "@/components/ui/Skeleton";
import { ErrorState } from "@/components/ui/ErrorState";
import { fetchCompanies, fetchFilterOptions, searchCompanies } from "@/lib/companies";
import type { CompanyListResponse, CompanySummary, FilterOptions } from "@/types";

const DEFAULT_FACETS: FilterOptions = {
  industries: [
    "Consumer Electronics",
    "Software—Infrastructure",
    "Semiconductors",
    "Internet Content & Information",
    "Internet Retail",
    "Insurance—Diversified",
    "Drug Manufacturers—General",
    "Auto Manufacturers",
    "Banks—Diversified",
    "Credit Services",
    "Healthcare Plans",
    "Oil & Gas Integrated",
    "Discount Stores",
    "Household & Personal Products",
    "Home Improvement Retail",
  ],
  states: ["CA", "WA", "NE", "IN", "TX", "NY", "MN", "AR", "NJ", "OH", "GA", "IL", "NC", "CT", "MA", "FL", "VA", "CO"],
  sectors: [
    "Technology",
    "Communication Services",
    "Consumer Cyclical",
    "Financial Services",
    "Healthcare",
    "Energy",
    "Consumer Defensive",
    "Basic Materials",
    "Industrials",
    "Utilities",
  ],
  exchanges: ["NASDAQ", "NYSE"],
  risk_levels: ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
};

function CompanyDirectoryContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const currentQ = searchParams.get("q") ?? "";
  const currentIndustry = searchParams.get("industry") ?? "all";
  const currentState = searchParams.get("state") ?? "all";
  const currentName = searchParams.get("name") ?? "";
  const currentSector = searchParams.get("sector") ?? "all";
  const currentRisk = searchParams.get("risk_level") ?? "all";
  const currentSort = searchParams.get("sort_by") ?? "market_cap";
  const currentOrder = (searchParams.get("sort_order") as "asc" | "desc") ?? "desc";
  const currentPage = parseInt(searchParams.get("page") ?? "1", 10);

  const [data, setData] = useState<CompanyListResponse | null>(null);
  const [facets, setFacets] = useState<FilterOptions>(DEFAULT_FACETS);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [mobileFilterOpen, setMobileFilterOpen] = useState(false);

  // Update URL helper
  const updateParams = useCallback(
    (newParams: Record<string, string | null>) => {
      const params = new URLSearchParams(searchParams.toString());
      Object.entries(newParams).forEach(([k, v]) => {
        if (v === null || v === "" || v === "all") {
          params.delete(k);
        } else {
          params.set(k, v);
        }
      });
      if (!newParams.page) {
        params.delete("page");
      }
      router.push(`/companies?${params.toString()}`);
    },
    [router, searchParams]
  );

  // Load facets once
  useEffect(() => {
    fetchFilterOptions()
      .then((res) => {
        if (res && res.industries && res.industries.length > 0) {
          setFacets(res);
        }
      })
      .catch(() => {});
  }, []);

  const loadData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      let res: CompanyListResponse;
      if (currentQ.trim()) {
        res = await searchCompanies(currentQ.trim(), {
          industry: currentIndustry !== "all" ? currentIndustry : undefined,
          state: currentState !== "all" ? currentState : undefined,
          name: currentName || undefined,
          sector: currentSector !== "all" ? currentSector : undefined,
          page: currentPage,
          page_size: 12,
        });
      } else {
        res = await fetchCompanies({
          industry: currentIndustry !== "all" ? currentIndustry : undefined,
          state: currentState !== "all" ? currentState : undefined,
          name: currentName || undefined,
          sector: currentSector !== "all" ? currentSector : undefined,
          risk_level: currentRisk !== "all" ? currentRisk : undefined,
          sort_by: currentSort,
          sort_order: currentOrder,
          page: currentPage,
          page_size: 12,
        });
      }
      setData(res);
    } catch (err: any) {
      setError(err?.message || "Failed to load corporate registry");
    } finally {
      setIsLoading(false);
    }
  }, [
    currentQ,
    currentIndustry,
    currentState,
    currentName,
    currentSector,
    currentRisk,
    currentSort,
    currentOrder,
    currentPage,
  ]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleSearch = (q: string) => {
    updateParams({ q, page: null });
  };

  const handleResetFilters = () => {
    router.push("/companies");
  };

  const activeFilterChips = [
    currentQ && { label: `Search: "${currentQ}"`, onRemove: () => updateParams({ q: null }) },
    currentName && { label: `Name: "${currentName}"`, onRemove: () => updateParams({ name: null }) },
    currentIndustry !== "all" && { label: `Industry: ${currentIndustry}`, onRemove: () => updateParams({ industry: null }) },
    currentState !== "all" && { label: `State: ${currentState}`, onRemove: () => updateParams({ state: null }) },
    currentSector !== "all" && { label: `Sector: ${currentSector}`, onRemove: () => updateParams({ sector: null }) },
    currentRisk !== "all" && { label: `Risk: ${currentRisk}`, onRemove: () => updateParams({ risk_level: null }) },
  ].filter(Boolean) as { label: string; onRemove: () => void }[];

  return (
    <div className="min-h-screen pb-20">
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 space-y-8">
        {/* Page Header */}
        <div className="flex flex-col justify-between gap-4 md:flex-row md:items-end">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-mono font-bold uppercase tracking-widest text-blue-400">
                Corporate Registry
              </span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-black tracking-tight text-white">
              Company Intelligence Directory
            </h1>
            <p className="text-xs sm:text-sm text-slate-400">
              Multi-factor risk scoring, forensic anomaly indicators, and relationship maps across 50 enterprises.
            </p>
          </div>

          {/* Sort Selector & Mobile Filter Button */}
          <div className="flex items-center gap-3">
            <Button
              variant="outline"
              size="sm"
              className="lg:hidden gap-1.5 h-10 rounded-xl border-white/10 bg-[#0F172A]"
              onClick={() => setMobileFilterOpen(!mobileFilterOpen)}
            >
              <Filter className="h-4 w-4 text-blue-400" />
              <span>Filters</span>
              {activeFilterChips.length > 0 && (
                <span className="ml-1 rounded-full bg-blue-600 px-1.5 py-0.2 text-[10px] text-white font-bold">
                  {activeFilterChips.length}
                </span>
              )}
            </Button>

            <div className="flex items-center gap-2 glass-panel px-3 py-1.5 rounded-xl border border-white/10">
              <span className="text-xs text-slate-400 whitespace-nowrap">Sort:</span>
              <select
                value={currentSort}
                onChange={(e) => updateParams({ sort_by: e.target.value })}
                aria-label="Sort by"
                className="h-8 rounded-lg bg-transparent text-xs text-white font-semibold focus:outline-none cursor-pointer"
              >
                <option value="market_cap" className="bg-[#0B1120]">Market Cap (High to Low)</option>
                <option value="name" className="bg-[#0B1120]">Company Name (A-Z)</option>
                <option value="founded_year" className="bg-[#0B1120]">Founded Year</option>
                <option value="risk_score" className="bg-[#0B1120]">Risk Score</option>
              </select>
            </div>
          </div>
        </div>

        {/* Global Search Bar */}
        <div className="glass-card rounded-2xl p-2 border border-white/10">
          <SearchBar initialQuery={currentQ} onSearch={handleSearch} placeholder="Filter by company name, ticker (e.g. NVDA, AAPL), or sector..." />
        </div>

        {/* Active Filter Chips */}
        {activeFilterChips.length > 0 && (
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs font-semibold text-slate-400 mr-1">Active filters:</span>
            {activeFilterChips.map((chip, idx) => (
              <span
                key={idx}
                className="inline-flex items-center gap-1.5 rounded-xl border border-blue-500/30 bg-blue-500/10 px-3 py-1 text-xs font-semibold text-blue-400"
              >
                {chip.label}
                <button
                  type="button"
                  onClick={chip.onRemove}
                  className="rounded-full p-0.5 hover:bg-blue-500/20 text-blue-400 transition-colors"
                >
                  <X className="h-3 w-3" />
                </button>
              </span>
            ))}
            <Button
              variant="ghost"
              size="sm"
              onClick={handleResetFilters}
              className="h-7 px-2 text-xs text-slate-400 hover:text-white"
            >
              Clear all
            </Button>
          </div>
        )}

        <div className="grid grid-cols-1 gap-8 lg:grid-cols-4">
          {/* ── Left Filter Sidebar (Desktop) ─────────────────────────────── */}
          <aside className="hidden lg:block lg:col-span-1 space-y-6">
            <div className="glass-card rounded-3xl p-5 border border-white/[0.08]">
              <CompanyFilters
                facets={facets}
                selectedIndustry={currentIndustry}
                selectedState={currentState}
                selectedName={currentName}
                selectedSector={currentSector}
                selectedRiskLevel={currentRisk}
                onIndustryChange={(ind) => updateParams({ industry: ind })}
                onStateChange={(st) => updateParams({ state: st })}
                onNameChange={(nm) => updateParams({ name: nm })}
                onSectorChange={(sec) => updateParams({ sector: sec })}
                onRiskLevelChange={(rsk) => updateParams({ risk_level: rsk })}
                onReset={handleResetFilters}
              />
            </div>
          </aside>

          {/* ── Mobile Filter Drawer ──────────────────────────────────────── */}
          {mobileFilterOpen && (
            <div className="lg:hidden col-span-1 mb-6 glass-card rounded-2xl p-4 border border-white/10">
              <CompanyFilters
                facets={facets}
                selectedIndustry={currentIndustry}
                selectedState={currentState}
                selectedName={currentName}
                selectedSector={currentSector}
                selectedRiskLevel={currentRisk}
                onIndustryChange={(ind) => updateParams({ industry: ind })}
                onStateChange={(st) => updateParams({ state: st })}
                onNameChange={(nm) => updateParams({ name: nm })}
                onSectorChange={(sec) => updateParams({ sector: sec })}
                onRiskLevelChange={(rsk) => updateParams({ risk_level: rsk })}
                onReset={handleResetFilters}
              />
            </div>
          )}

          {/* ── Right Results Section ─────────────────────────────────────── */}
          <section className="col-span-1 lg:col-span-3 space-y-6">
            {isLoading ? (
              <div className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
                {Array.from({ length: 6 }).map((_, i) => (
                  <CompanyCardSkeleton key={i} />
                ))}
              </div>
            ) : error ? (
              <ErrorState
                title="Failed to Load Company Directory"
                message={error}
                onRetry={loadData}
              />
            ) : data && data.items.length > 0 ? (
              <>
                <div className="flex items-center justify-between text-xs text-slate-400 px-1">
                  <span>
                    Displaying <strong className="text-white">{data.items.length}</strong> of <strong className="text-white">{data.total}</strong> corporate entities
                  </span>
                  <span className="font-mono">
                    Page {data.page} of {data.total_pages || 1}
                  </span>
                </div>

                {/* Company Cards Grid */}
                <div className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
                  {data.items.map((company) => (
                    <CompanyCard key={company.id} company={company} />
                  ))}
                </div>

                {/* Pagination Controls */}
                {data.total_pages > 1 && (
                  <div className="flex items-center justify-center gap-2 pt-8">
                    <Button
                      variant="outline"
                      size="sm"
                      disabled={data.page <= 1}
                      onClick={() => updateParams({ page: String(data.page - 1) })}
                      className="gap-1 rounded-xl border-white/10 bg-[#0F172A] text-xs font-semibold text-white"
                    >
                      <ChevronLeft className="h-4 w-4" />
                      Previous
                    </Button>

                    <div className="flex items-center gap-1">
                      {Array.from({ length: data.total_pages }, (_, i) => i + 1).map((p) => (
                        <Button
                          key={p}
                          variant={p === data.page ? "default" : "outline"}
                          size="sm"
                          onClick={() => updateParams({ page: String(p) })}
                          className={`h-8 w-8 rounded-xl p-0 text-xs font-bold ${
                            p === data.page
                              ? "bg-blue-600 text-white shadow-[0_0_15px_rgba(37,99,235,0.4)]"
                              : "border-white/10 bg-[#0F172A] text-slate-300 hover:text-white"
                          }`}
                        >
                          {p}
                        </Button>
                      ))}
                    </div>

                    <Button
                      variant="outline"
                      size="sm"
                      disabled={data.page >= data.total_pages}
                      onClick={() => updateParams({ page: String(data.page + 1) })}
                      className="gap-1 rounded-xl border-white/10 bg-[#0F172A] text-xs font-semibold text-white"
                    >
                      Next
                      <ChevronRight className="h-4 w-4" />
                    </Button>
                  </div>
                )}
              </>
            ) : (
              <div className="glass-card flex flex-col items-center justify-center rounded-3xl border border-dashed border-white/10 p-16 text-center space-y-3">
                <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-white/[0.04] text-slate-400">
                  <Search className="h-8 w-8" />
                </div>
                <h3 className="text-lg font-bold text-white">No Matching Companies Found</h3>
                <p className="max-w-sm text-xs text-slate-400 leading-relaxed">
                  No company records match your current filter selection. Reset filters or search with another term.
                </p>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleResetFilters}
                  className="mt-4 rounded-xl border-white/10 bg-[#0F172A] text-xs font-semibold text-white"
                >
                  Reset All Filters
                </Button>
              </div>
            )}
          </section>
        </div>
      </main>
    </div>
  );
}

export default function CompaniesPage() {
  return (
    <Suspense
      fallback={
        <div className="flex min-h-screen items-center justify-center">
          <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
        </div>
      }
    >
      <CompanyDirectoryContent />
    </Suspense>
  );
}
