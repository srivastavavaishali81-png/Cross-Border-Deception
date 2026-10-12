"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  CheckCircle2,
  Info,
  Loader2,
  Lock,
  Mail,
  Shield,
  Sparkles,
  User,
  UserPlus,
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

type FormState = {
  name: string;
  email: string;
  password: string;
  confirm: string;
};

type FieldErrors = Partial<Record<keyof FormState, string>>;

function validateForm(form: FormState): FieldErrors {
  const errors: FieldErrors = {};

  if (form.name.trim().length < 2)
    errors.name = "Name must be at least 2 characters.";

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email))
    errors.email = "Enter a valid corporate email address.";

  const p = form.password;
  if (p.length < 8) errors.password = "Minimum 8 characters required.";
  else if (!/[A-Z]/.test(p)) errors.password = "Must contain at least one uppercase letter.";
  else if (!/\d/.test(p)) errors.password = "Must contain at least one number.";
  else if (!/[!@#$%^&*()_+\-=[\]{}|;':\",./<>?]/.test(p))
    errors.password = "Must contain at least one special symbol.";

  if (form.confirm !== form.password)
    errors.confirm = "Passwords do not match.";

  return errors;
}

export default function RegisterPage() {
  const { register, login } = useAuth();
  const router = useRouter();

  const [form, setForm] = useState<FormState>({
    name: "",
    email: "",
    password: "",
    confirm: "",
  });
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFillSample = () => {
    const randomId = Math.floor(Math.random() * 900 + 100);
    setForm({
      name: "Risk Analyst",
      email: `analyst${randomId}@ozark.ai`,
      password: "Password@123",
      confirm: "Password@123",
    });
    setFieldErrors({});
    setError(null);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    setFieldErrors((prev) => ({ ...prev, [name]: undefined }));
    setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const errors = validateForm(form);
    if (Object.keys(errors).length > 0) {
      setFieldErrors(errors);
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      await register({
        name: form.name.trim(),
        email: form.email,
        password: form.password,
      });
      document.cookie = "ozark_authed=1; path=/; max-age=604800; SameSite=Strict";
      router.push("/dashboard");
    } catch (err: unknown) {
      const msg =
        err instanceof Error
          ? err.message
          : "Registration failed. Please try again.";
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      {/* ── Sample Form Autofill / Demo Helper ──────────────────────────────── */}
      <div className="rounded-2xl border border-blue-500/30 bg-blue-500/10 p-3.5 text-xs flex items-center justify-between shadow-lg shadow-blue-950/20">
        <div className="flex items-center gap-2 text-blue-300">
          <Sparkles className="h-4 w-4" />
          <span>Quick Testing: Pre-populate analyst details</span>
        </div>
        <Button
          type="button"
          size="sm"
          variant="outline"
          onClick={handleFillSample}
          className="h-7 px-2.5 text-[11px] font-bold border-blue-400/40 bg-blue-500/20 hover:bg-blue-500/30 text-blue-200 rounded-lg"
        >
          Auto-Fill
        </Button>
      </div>

      {/* ── Main Register Card ─────────────────────────────────────────────── */}
      <Card className="glass-card rounded-3xl border border-white/[0.12] shadow-2xl p-2 bg-[#0F172A]/80 backdrop-blur-xl">
        <CardHeader className="space-y-1 pb-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Shield className="h-5 w-5 text-blue-400" />
              <span className="text-[11px] font-mono font-bold uppercase tracking-widest text-blue-400">
                Institutional Onboarding
              </span>
            </div>
            <Link href="/login" className="text-xs font-semibold text-blue-400 hover:text-blue-300">
              Have account?
            </Link>
          </div>
          <CardTitle className="text-2xl font-black text-white tracking-tight">Create Risk Account</CardTitle>
          <CardDescription className="text-xs text-slate-400">
            Provision credential access to the OZARK intelligence suite.
          </CardDescription>
        </CardHeader>

        <CardContent>
          <form id="register-form" onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div
                role="alert"
                className="rounded-2xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-xs text-rose-300 leading-relaxed font-medium"
              >
                {error}
              </div>
            )}

            {/* Name */}
            <div className="space-y-1.5">
              <Label htmlFor="name" className="text-xs font-semibold text-slate-200">
                Full Legal Name
              </Label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                <Input
                  id="name"
                  name="name"
                  type="text"
                  placeholder="Warren Buffett"
                  autoComplete="name"
                  required
                  value={form.name}
                  onChange={handleChange}
                  disabled={isLoading}
                  aria-invalid={!!fieldErrors.name}
                  className="pl-9 h-11 rounded-xl bg-[#0B1120] border-white/15 text-white placeholder:text-slate-500 text-xs focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                />
              </div>
              {fieldErrors.name && (
                <p className="text-[11px] text-rose-400 font-medium">{fieldErrors.name}</p>
              )}
            </div>

            {/* Email */}
            <div className="space-y-1.5">
              <Label htmlFor="reg-email" className="text-xs font-semibold text-slate-200">
                Corporate Email Address
              </Label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                <Input
                  id="reg-email"
                  name="email"
                  type="email"
                  placeholder="analyst@hedgefund.com"
                  autoComplete="email"
                  required
                  value={form.email}
                  onChange={handleChange}
                  disabled={isLoading}
                  aria-invalid={!!fieldErrors.email}
                  className="pl-9 h-11 rounded-xl bg-[#0B1120] border-white/15 text-white placeholder:text-slate-500 text-xs focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                />
              </div>
              {fieldErrors.email && (
                <p className="text-[11px] text-rose-400 font-medium">{fieldErrors.email}</p>
              )}
            </div>

            {/* Password */}
            <div className="space-y-1.5">
              <Label htmlFor="reg-password" className="text-xs font-semibold text-slate-200">
                Password
              </Label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                <Input
                  id="reg-password"
                  name="password"
                  type="password"
                  placeholder="Min 8 chars (1 uppercase, 1 digit, 1 symbol)"
                  autoComplete="new-password"
                  required
                  value={form.password}
                  onChange={handleChange}
                  disabled={isLoading}
                  aria-invalid={!!fieldErrors.password}
                  className="pl-9 h-11 rounded-xl bg-[#0B1120] border-white/15 text-white placeholder:text-slate-500 text-xs focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                />
              </div>
              {fieldErrors.password && (
                <p className="text-[11px] text-rose-400 font-medium">{fieldErrors.password}</p>
              )}
            </div>

            {/* Confirm */}
            <div className="space-y-1.5">
              <Label htmlFor="confirm" className="text-xs font-semibold text-slate-200">
                Confirm Password
              </Label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                <Input
                  id="confirm"
                  name="confirm"
                  type="password"
                  placeholder="Re-enter password"
                  autoComplete="new-password"
                  required
                  value={form.confirm}
                  onChange={handleChange}
                  disabled={isLoading}
                  aria-invalid={!!fieldErrors.confirm}
                  className="pl-9 h-11 rounded-xl bg-[#0B1120] border-white/15 text-white placeholder:text-slate-500 text-xs focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                />
              </div>
              {fieldErrors.confirm && (
                <p className="text-[11px] text-rose-400 font-medium">{fieldErrors.confirm}</p>
              )}
            </div>

            <Button
              type="submit"
              className="w-full h-11 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs shadow-[0_0_25px_rgba(37,99,235,0.45)] transition-all gap-2"
              disabled={isLoading}
              id="register-submit"
            >
              {isLoading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Provisioning account...
                </>
              ) : (
                <>
                  <UserPlus className="h-4 w-4" />
                  Create Institutional Account
                </>
              )}
            </Button>
          </form>
        </CardContent>

        <CardFooter className="flex-col items-center gap-3 border-t border-white/[0.08] pt-4">
          <div className="flex items-center justify-between w-full text-xs text-slate-400">
            <span>Already registered?</span>
            <Link
              href="/login"
              className="font-bold text-blue-400 hover:text-blue-300 transition-colors"
            >
              Sign in to Account →
            </Link>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}
