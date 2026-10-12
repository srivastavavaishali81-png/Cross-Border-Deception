"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { Search, X, Building2, TrendingUp, ShieldAlert, Loader2, ArrowRight } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { searchCompanies } from "@/lib/companies";
import type { CompanySummary } from "@/types";

interface SearchBarProps {
  initialQuery?: string;
  placeholder?: string;
  onSearch?: (query: string) => void;
  className?: string;
  autoFocus?: boolean;
}

export function SearchBar({
  initialQuery = "",
  placeholder = "Search by company name, ticker (e.g. AAPL, NVDA), industry, state...",
  onSearch,
  className = "",
  autoFocus = false,
}: SearchBarProps) {
  const router = useRouter();
  const [query, setQuery] = useState(initialQuery);
  const [suggestions, setSuggestions] = useState<CompanySummary[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const debounceTimerRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    setQuery(initialQuery);
  }, [initialQuery]);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleQueryChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setQuery(val);

    if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);

    if (val.trim().length >= 2) {
      setIsLoading(true);
      debounceTimerRef.current = setTimeout(async () => {
        try {
          const res = await searchCompanies(val.trim(), { page_size: 5 });
          setSuggestions(res.items || []);
          setIsOpen(true);
        } catch {
          setSuggestions([]);
        } finally {
          setIsLoading(false);
        }
      }, 250);
    } else {
      setSuggestions([]);
      setIsOpen(false);
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setQuery("");
    setSuggestions([]);
    setIsOpen(false);
    if (onSearch) onSearch("");
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsOpen(false);
    if (onSearch) {
      onSearch(query.trim());
    } else {
      router.push(`/companies?q=${encodeURIComponent(query.trim())}`);
    }
  };

  const handleSelectCompany = (tickerOrId: string) => {
    setIsOpen(false);
    router.push(`/companies/${tickerOrId}`);
  };

  return (
    <div ref={dropdownRef} className={`relative w-full ${className}`}>
      <form onSubmit={handleSubmit} className="relative flex items-center">
        <div className="pointer-events-none absolute left-3.5 flex items-center text-muted-foreground">
          {isLoading ? (
            <Loader2 className="h-4 w-4 animate-spin text-primary" />
          ) : (
            <Search className="h-4 w-4 text-muted-foreground" />
          )}
        </div>

        <Input
          type="text"
          value={query}
          onChange={handleQueryChange}
          onFocus={() => {
            if (suggestions.length > 0) setIsOpen(true);
          }}
          placeholder={placeholder}
          autoFocus={autoFocus}
          className="h-11 rounded-xl border-border/80 bg-background/80 pl-10 pr-24 text-sm backdrop-blur-sm shadow-sm transition-all focus-visible:ring-2 focus-visible:ring-primary/40 focus-visible:border-primary"
        />

        <div className="absolute right-2 flex items-center gap-1.5">
          {query && (
            <button
              type="button"
              onClick={handleClear}
              className="rounded-full p-1 text-muted-foreground hover:bg-muted hover:text-foreground transition-colors"
              title="Clear search"
            >
              <X className="h-3.5 w-3.5" />
            </button>
          )}

          <Button type="submit" size="sm" className="h-8 rounded-lg px-3 text-xs font-medium">
            Search
          </Button>
        </div>
      </form>

      {/* Autocomplete Dropdown */}
      {isOpen && suggestions.length > 0 && (
        <div className="absolute left-0 right-0 top-full z-50 mt-2 overflow-hidden rounded-xl border border-border/70 bg-card/95 p-1.5 shadow-2xl backdrop-blur-md animate-in fade-in-0 zoom-in-95">
          <div className="px-3 py-1.5 text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
            Matching Companies
          </div>
          <div className="space-y-0.5">
            {suggestions.map((company) => {
              const riskColor =
                company.latest_risk_score?.risk_level === "LOW"
                  ? "text-emerald-500 bg-emerald-500/10 border-emerald-500/20"
                  : company.latest_risk_score?.risk_level === "MEDIUM"
                  ? "text-amber-500 bg-amber-500/10 border-amber-500/20"
                  : "text-rose-500 bg-rose-500/10 border-rose-500/20";

              return (
                <button
                  key={company.id}
                  type="button"
                  onClick={() => handleSelectCompany(company.ticker || company.id)}
                  className="flex w-full items-center justify-between rounded-lg px-3 py-2 text-left text-sm transition-colors hover:bg-muted/80"
                >
                  <div className="flex items-center gap-2.5">
                    <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10 text-primary font-bold text-xs">
                      {company.ticker}
                    </div>
                    <div>
                      <p className="font-medium text-foreground leading-tight">{company.name}</p>
                      <p className="text-xs text-muted-foreground">
                        {company.industry} • {company.state ? `${company.state}, ` : ""}{company.country}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    {company.latest_risk_score && (
                      <span className={`inline-flex items-center rounded-full border px-2 py-0.5 text-[10px] font-semibold ${riskColor}`}>
                        Risk: {company.latest_risk_score.overall_score}
                      </span>
                    )}
                    <ArrowRight className="h-3.5 w-3.5 text-muted-foreground" />
                  </div>
                </button>
              );
            })}
          </div>

          <div className="border-t border-border/50 mt-1 pt-1">
            <button
              type="button"
              onClick={handleSubmit}
              className="flex w-full items-center justify-center gap-1.5 rounded-lg py-1.5 text-xs text-primary font-medium hover:bg-primary/5 transition-colors"
            >
              View all results for &ldquo;{query}&rdquo;
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
