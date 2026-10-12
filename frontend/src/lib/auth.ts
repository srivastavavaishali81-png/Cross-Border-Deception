/**
 * OZARK — Auth API Client
 *
 * Wraps all auth-related backend calls.
 */

import { api } from "@/lib/api-client";

export interface User {
  id: string;
  name: string;
  email: string;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface RegisterPayload {
  name: string;
  email: string;
  password: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

// ── Token storage (memory + localStorage) ────────────────────────────────────
// Access tokens live in memory only (not localStorage) to reduce XSS surface.
// Refresh tokens go to localStorage to survive page refreshes.

let _accessToken: string | null = null;

export const tokenStore = {
  getAccess: () => _accessToken,
  setAccess: (t: string | null) => { _accessToken = t; },

  getRefresh: () => {
    if (typeof window === "undefined") return null;
    return localStorage.getItem("ozark_refresh_token");
  },
  setRefresh: (t: string | null) => {
    if (typeof window === "undefined") return;
    if (t) localStorage.setItem("ozark_refresh_token", t);
    else localStorage.removeItem("ozark_refresh_token");
  },

  clear: () => {
    _accessToken = null;
    if (typeof window !== "undefined") {
      localStorage.removeItem("ozark_refresh_token");
    }
  },
};

// ── Auth API calls ─────────────────────────────────────────────────────────────

export async function register(payload: RegisterPayload): Promise<User> {
  return api.post<User>("/api/v1/auth/register", payload);
}

export async function login(payload: LoginPayload): Promise<TokenResponse> {
  const tokens = await api.post<TokenResponse>("/api/v1/auth/login", payload);
  tokenStore.setAccess(tokens.access_token);
  tokenStore.setRefresh(tokens.refresh_token);
  return tokens;
}

export async function refreshTokens(): Promise<TokenResponse | null> {
  const refresh_token = tokenStore.getRefresh();
  if (!refresh_token) return null;
  try {
    const tokens = await api.post<TokenResponse>("/api/v1/auth/refresh", {
      refresh_token,
    });
    tokenStore.setAccess(tokens.access_token);
    tokenStore.setRefresh(tokens.refresh_token);
    return tokens;
  } catch {
    tokenStore.clear();
    return null;
  }
}

export async function getMe(accessToken: string): Promise<User> {
  return api.get<User>("/api/v1/auth/me", {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}

export function logout(): void {
  tokenStore.clear();
}
