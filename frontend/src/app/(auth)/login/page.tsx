"use client";

import { Suspense, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import {
  CheckCircle2,
  KeyRound,
  Loader2,
  LogIn,
  Lock,
  Mail,
  Shield,
  Sparkles,
  Zap,
} from "lucide-react";

import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

function LoginForm() {
  const { login } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get("callbackUrl") ?? "/dashboard";

  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isDemoLoading, setIsDemoLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    setError(null);
  };

  const handleDemoFill = async () => {
    setIsDemoLoading(true);
    setError(null);
    setForm({ email: "demo@ozark.ai", password: "Demo@123" });
    try {
      await login({ email: "demo@ozark.ai", password: "Demo@123" });
      document.cookie = "ozark_authed=1; path=/; max-age=604800; SameSite=Strict";
      router.push(callbackUrl);
    } catch (err: unknown) {
      const msg =
        err instanceof Error ? err.message : "Demo authentication failed.";
      setError(msg);
    } finally {
      setIsDemoLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      await login(form);
      document.cookie = "ozark_authed=1; path=/; max-age=604800; SameSite=Strict";
      router.push(callbackUrl);
    } catch (err: unknown) {
      const msg =
        err instanceof Error ? err.message : "Authentication failed. Please verify credentials.";
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      {/* ── Quick Demo Banner ──────────────────────────────────────────────── */}
      <div className="rounded-2xl border border-amber-500/30 bg-gradient-to-r from-amber-500/15 via-amber-500/10 to-transparent p-4 text-xs space-y-2 shadow-lg shadow-amber-950/20">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 font-bold text-amber-300">
            <Zap className="h-4 w-4 fill-amber-400 text-amber-400" />
            <span>Fast Instant Demo Access</span>
          </div>
          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/20 text-amber-200 border border-amber-500/30">
            Pre-configured
          </span>
        </div>
        <p className="text-[11px] text-slate-300 leading-relaxed">
          Want to explore the <strong>Investor Dashboard</strong> immediately? Click below for 1-click authorization.
        </p>
        <Button
          type="button"
          onClick={handleDemoFill}
          disabled={isLoading || isDemoLoading}
          className="w-full h-10 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs shadow-[0_0_20px_rgba(245,158,11,0.35)] transition-all flex items-center justify-center gap-2"
        >
          {isDemoLoading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              Signing in demo session...
            </>
          ) : (
            <>
              <Zap className="h-4 w-4 fill-slate-950" />
              1-Click Demo Login (demo@ozark.ai)
            </>
          )}
        </Button>
      </div>

      {/* ── Main Login Card ────────────────────────────────────────────────── */}
      <Card className="glass-card rounded-3xl border border-white/[0.12] shadow-2xl p-2 bg-[#0F172A]/80 backdrop-blur-xl">
        <CardHeader className="space-y-1 pb-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Shield className="h-5 w-5 text-blue-400" />
              <span className="text-[11px] font-mono font-bold uppercase tracking-widest text-blue-400">
                Secure Portal Access
              </span>
            </div>
            <Link href="/register" className="text-xs font-semibold text-blue-400 hover:text-blue-300">
              Need account?
            </Link>
          </div>
          <CardTitle className="text-2xl font-black text-white tracking-tight">Institutional Sign In</CardTitle>
          <CardDescription className="text-xs text-slate-400">
            Enter authorized credentials or use demo credentials below.
          </CardDescription>
        </CardHeader>

        <CardContent>
          <form id="login-form" onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div
                role="alert"
                className="rounded-2xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-xs text-rose-300 leading-relaxed font-medium"
              >
                {error}
              </div>
            )}

            <div className="space-y-1.5">
              <Label htmlFor="email" className="text-xs font-semibold text-slate-200">
                Corporate Email Address
              </Label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                <Input
                  id="email"
                  name="email"
                  type="email"
                  placeholder="analyst@fund.com"
                  autoComplete="email"
                  required
                  value={form.email}
                  onChange={handleChange}
                  disabled={isLoading || isDemoLoading}
                  className="pl-9 h-11 rounded-xl bg-[#0B1120] border-white/15 text-white placeholder:text-slate-500 text-xs focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <div className="flex items-center justify-between">
                <Label htmlFor="password" className="text-xs font-semibold text-slate-200">
                  Password
                </Label>
                <button
                  type="button"
                  onClick={() => setForm({ email: "demo@ozark.ai", password: "Demo@123" })}
                  className="text-[11px] font-mono text-blue-400 hover:underline"
                >
                  Fill: Demo@123
                </button>
              </div>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                <Input
                  id="password"
                  name="password"
                  type="password"
                  placeholder="••••••••••••"
                  autoComplete="current-password"
                  required
                  value={form.password}
                  onChange={handleChange}
                  disabled={isLoading || isDemoLoading}
                  className="pl-9 h-11 rounded-xl bg-[#0B1120] border-white/15 text-white placeholder:text-slate-500 text-xs focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                />
              </div>
            </div>

            <Button
              type="submit"
              className="w-full h-11 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs shadow-[0_0_25px_rgba(37,99,235,0.45)] transition-all gap-2"
              disabled={isLoading || isDemoLoading}
              id="login-submit"
            >
              {isLoading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Authenticating session...
                </>
              ) : (
                <>
                  <LogIn className="h-4 w-4" />
                  Sign In to Platform
                </>
              )}
            </Button>
          </form>
        </CardContent>

        <CardFooter className="flex-col items-center gap-3 border-t border-white/[0.08] pt-4">
          <div className="flex items-center justify-between w-full text-xs text-slate-400">
            <span>New institutional user?</span>
            <Link
              href="/register"
              className="font-bold text-blue-400 hover:text-blue-300 transition-colors"
            >
              Create an Account →
            </Link>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense
      fallback={
        <div className="glass-card rounded-3xl border border-white/10 p-12 flex items-center justify-center">
          <Loader2 className="h-6 w-6 animate-spin text-blue-400" />
        </div>
      }
    >
      <LoginForm />
    </Suspense>
  );
}
