"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
} from "react";
import {
  type User,
  type LoginPayload,
  type RegisterPayload,
  getMe,
  login as apiLogin,
  logout as apiLogout,
  refreshTokens,
  register as apiRegister,
  tokenStore,
} from "@/lib/auth";

// ── Types ──────────────────────────────────────────────────────────────────────

interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
}

interface AuthContextValue extends AuthState {
  login: (payload: LoginPayload) => Promise<void>;
  register: (payload: RegisterPayload) => Promise<void>;
  logout: () => void;
}

// ── Context ────────────────────────────────────────────────────────────────────

const AuthContext = createContext<AuthContextValue | null>(null);

// ── Provider ───────────────────────────────────────────────────────────────────

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const refreshTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Schedule silent token refresh 1 minute before expiry
  const scheduleRefresh = useCallback((expiresInSeconds: number) => {
    if (refreshTimerRef.current) clearTimeout(refreshTimerRef.current);
    const delay = Math.max((expiresInSeconds - 60) * 1000, 0);
    refreshTimerRef.current = setTimeout(async () => {
      const tokens = await refreshTokens();
      if (tokens) scheduleRefresh(tokens.expires_in);
      else setUser(null);
    }, delay);
  }, []);

  // On mount: attempt silent restore from refresh token
  useEffect(() => {
    (async () => {
      try {
        const tokens = await refreshTokens();
        if (tokens) {
          const me = await getMe(tokens.access_token);
          setUser(me);
          scheduleRefresh(tokens.expires_in);
        }
      } catch {
        // No valid session — that's fine
      } finally {
        setIsLoading(false);
      }
    })();

    return () => {
      if (refreshTimerRef.current) clearTimeout(refreshTimerRef.current);
    };
  }, [scheduleRefresh]);

  const login = useCallback(
    async (payload: LoginPayload) => {
      const tokens = await apiLogin(payload);
      const me = await getMe(tokens.access_token);
      setUser(me);
      scheduleRefresh(tokens.expires_in);
    },
    [scheduleRefresh]
  );

  const register = useCallback(async (payload: RegisterPayload) => {
    await apiRegister(payload);
    // After register, immediately log in
    const tokens = await apiLogin({
      email: payload.email,
      password: payload.password,
    });
    const me = await getMe(tokens.access_token);
    setUser(me);
    scheduleRefresh(tokens.expires_in);
  }, [scheduleRefresh]);

  const logout = useCallback(() => {
    apiLogout();
    setUser(null);
    if (refreshTimerRef.current) clearTimeout(refreshTimerRef.current);
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

// ── Hook ───────────────────────────────────────────────────────────────────────

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within <AuthProvider>");
  return ctx;
}
