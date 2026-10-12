"use client";

import { Filter, RotateCcw, Building, MapPin, Tag, Shield } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import type { FilterOptions } from "@/types";

interface CompanyFiltersProps {
  facets: FilterOptions;
  selectedIndustry: string;
  selectedState: string;
  selectedName: string;
  selectedSector: string;
  selectedRiskLevel: string;
  onIndustryChange: (industry: string) => void;
  onStateChange: (state: string) => void;
  onNameChange: (name: string) => void;
  onSectorChange: (sector: string) => void;
  onRiskLevelChange: (risk: string) => void;
  onReset: () => void;
  className?: string;
}

export function CompanyFilters({
  facets,
  selectedIndustry,
  selectedState,
  selectedName,
  selectedSector,
  selectedRiskLevel,
  onIndustryChange,
  onStateChange,
  onNameChange,
  onSectorChange,
  onRiskLevelChange,
  onReset,
  className = "",
}: CompanyFiltersProps) {
  const hasActiveFilters =
    Boolean(selectedIndustry && selectedIndustry !== "all") ||
    Boolean(selectedState && selectedState !== "all") ||
    Boolean(selectedName) ||
    Boolean(selectedSector && selectedSector !== "all") ||
    Boolean(selectedRiskLevel && selectedRiskLevel !== "all");

  return (
    <div className={`space-y-6 rounded-2xl border border-border/60 bg-card/70 p-5 backdrop-blur-md shadow-sm ${className}`}>
      <div className="flex items-center justify-between pb-2 border-b border-border/50">
        <div className="flex items-center gap-2">
          <Filter className="h-4 w-4 text-primary" />
          <h3 className="font-semibold text-foreground text-sm tracking-tight">Filter Directory</h3>
        </div>

        {hasActiveFilters && (
          <Button
            variant="ghost"
            size="sm"
            onClick={onReset}
            className="h-7 px-2 text-xs text-muted-foreground hover:text-foreground gap-1"
          >
            <RotateCcw className="h-3 w-3" />
            Reset
          </Button>
        )}
      </div>

      {/* 1. Filter by Company Name */}
      <div className="space-y-2">
        <Label htmlFor="filter-name" className="text-xs font-semibold text-muted-foreground uppercase tracking-wider flex items-center gap-1.5">
          <Building className="h-3.5 w-3.5 text-primary" />
          Company Name
        </Label>
        <Input
          id="filter-name"
          type="text"
          placeholder="e.g. Apple, Microsoft..."
          value={selectedName}
          onChange={(e) => onNameChange(e.target.value)}
          className="h-9 rounded-lg text-xs"
        />
      </div>

      {/* 2. Filter by Industry */}
      <div className="space-y-2">
        <Label htmlFor="filter-industry" className="text-xs font-semibold text-muted-foreground uppercase tracking-wider flex items-center gap-1.5">
          <Tag className="h-3.5 w-3.5 text-primary" />
          Industry
        </Label>
        <select
          id="filter-industry"
          value={selectedIndustry}
          onChange={(e) => onIndustryChange(e.target.value)}
          className="w-full h-9 rounded-lg border border-input bg-background px-3 py-1 text-xs shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
        >
          <option value="all">All Industries</option>
          {facets.industries.map((ind) => (
            <option key={ind} value={ind}>
              {ind}
            </option>
          ))}
        </select>
      </div>

      {/* 3. Filter by State */}
      <div className="space-y-2">
        <Label htmlFor="filter-state" className="text-xs font-semibold text-muted-foreground uppercase tracking-wider flex items-center gap-1.5">
          <MapPin className="h-3.5 w-3.5 text-primary" />
          State (US)
        </Label>
        <select
          id="filter-state"
          value={selectedState}
          onChange={(e) => onStateChange(e.target.value)}
          className="w-full h-9 rounded-lg border border-input bg-background px-3 py-1 text-xs shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
        >
          <option value="all">All States</option>
          {facets.states.map((st) => (
            <option key={st} value={st}>
              {st}
            </option>
          ))}
        </select>
      </div>

      {/* 4. Filter by Sector */}
      <div className="space-y-2">
        <Label htmlFor="filter-sector" className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
          Sector
        </Label>
        <select
          id="filter-sector"
          value={selectedSector}
          onChange={(e) => onSectorChange(e.target.value)}
          className="w-full h-9 rounded-lg border border-input bg-background px-3 py-1 text-xs shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
        >
          <option value="all">All Sectors</option>
          {facets.sectors.map((sec) => (
            <option key={sec} value={sec}>
              {sec}
            </option>
          ))}
        </select>
      </div>

      {/* 5. Filter by Risk Level */}
      <div className="space-y-2">
        <Label htmlFor="filter-risk" className="text-xs font-semibold text-muted-foreground uppercase tracking-wider flex items-center gap-1.5">
          <Shield className="h-3.5 w-3.5 text-primary" />
          Risk Score Level
        </Label>
        <div className="grid grid-cols-2 gap-1.5 pt-1">
          {["all", "LOW", "MEDIUM", "HIGH", "CRITICAL"].map((lvl) => {
            const isSelected = selectedRiskLevel === lvl;
            const badgeLabel = lvl === "all" ? "Any Risk" : lvl;
            return (
              <button
                key={lvl}
                type="button"
                onClick={() => onRiskLevelChange(lvl)}
                className={`rounded-lg py-1.5 px-2 text-xs font-medium transition-colors text-center border ${
                  isSelected
                    ? "bg-primary text-primary-foreground border-primary"
                    : "bg-muted/30 text-muted-foreground hover:bg-muted border-border/50"
                }`}
              >
                {badgeLabel}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
