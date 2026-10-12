/**
OZARK — Company API Client
*/

import { api } from "@/lib/api-client";
import type {
  CompanyDetail,
  CompanyListResponse,
  CompanySearchResponse,
  FilterOptions,
} from "@/types";

export interface CompanyFilterParams {
  q?: string;
  industry?: string;
  state?: string;
  name?: string;
  sector?: string;
  risk_level?: string;
  sort_by?: string;
  sort_order?: "asc" | "desc";
  page?: number;
  page_size?: number;
}

export async function fetchCompanies(
  params: CompanyFilterParams = {}
): Promise<CompanyListResponse> {
  const queryParams: Record<string, string | number | boolean> = {};

  if (params.industry && params.industry !== "all") queryParams.industry = params.industry;
  if (params.state && params.state !== "all") queryParams.state = params.state;
  if (params.name) queryParams.name = params.name;
  if (params.sector && params.sector !== "all") queryParams.sector = params.sector;
  if (params.risk_level && params.risk_level !== "all") queryParams.risk_level = params.risk_level;
  if (params.sort_by) queryParams.sort_by = params.sort_by;
  if (params.sort_order) queryParams.sort_order = params.sort_order;
  if (params.page) queryParams.page = params.page;
  if (params.page_size) queryParams.page_size = params.page_size;

  return api.get<CompanyListResponse>("/api/v1/companies", {
    params: queryParams,
  });
}

export async function searchCompanies(
  query: string,
  params: Omit<CompanyFilterParams, "q"> = {}
): Promise<CompanySearchResponse> {
  const queryParams: Record<string, string | number | boolean> = {
    q: query,
  };

  if (params.industry && params.industry !== "all") queryParams.industry = params.industry;
  if (params.state && params.state !== "all") queryParams.state = params.state;
  if (params.name) queryParams.name = params.name;
  if (params.sector && params.sector !== "all") queryParams.sector = params.sector;
  if (params.page) queryParams.page = params.page;
  if (params.page_size) queryParams.page_size = params.page_size;

  return api.get<CompanySearchResponse>("/api/v1/companies/search", {
    params: queryParams,
  });
}

export async function fetchFilterOptions(): Promise<FilterOptions> {
  return api.get<FilterOptions>("/api/v1/companies/filters");
}

export async function fetchCompanyDetail(idOrTicker: string): Promise<CompanyDetail> {
  return api.get<CompanyDetail>(`/api/v1/companies/${encodeURIComponent(idOrTicker)}`);
}
