/**
OZARK — Network Graph API Client
*/

import { api } from "@/lib/api-client";
import type { NetworkGraphResponse } from "@/types/network";

export async function fetchCompanyNetwork(
  companyId: string,
  depth: number = 1
): Promise<NetworkGraphResponse> {
  return api.get<NetworkGraphResponse>(`/api/v1/network/${encodeURIComponent(companyId)}`, {
    params: { depth },
  });
}
