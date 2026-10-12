"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  Activity,
  BarChart3,
  Building2,
  ChevronRight,
  Globe2,
  LogIn,
  LogOut,
  Menu,
  Network,
  Search,
  Shield,
  User,
  UserPlus,
  X,
  Sparkles,
  Zap,
} from "lucide-react";

import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";

export function Navbar() {
  const pathname = usePathname();
  const router = useRouter();
  const { user, isAuthenticated, logout, login } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [isDemoLoading, setIsDemoLoading] = useState(false);

  const handleQuickDemo = async () => {
    try {
      setIsDemoLoading(true);
      await login({ email: "demo@ozark.ai", password: "Demo@123" });
      document.cookie = "ozark_authed=1; path=/; max-age=604800; SameSite=Strict";
      router.push("/dashboard");
    } catch (e) {
      console.error(e);
      router.push("/login");
    } finally {
      setIsDemoLoading(false);
    }
  };

  const navLinks = [
    {
      name: "Dashboard",
      href: "/dashboard",
      icon: BarChart3,
      badge: "Live",
      badgeColor: "bg-blue-500/20 text-blue-300 border-blue-500/30",
    },
    {
      name: "Companies",
      href: "/companies",
      icon: Building2,
      badge: "50",
      badgeColor: "bg-slate-700/50 text-slate-300 border-white/10",
    },
    {
      name: "Network Graph",
      href: "/network",
      icon: Network,
      badge: "Neo4j",
      badgeColor: "bg-cyan-500/20 text-cyan-300 border-cyan-500/30",
    },
  ];

  return (
    <header className="sticky top-0 z-50 w-full border-b border-white/[0.12] bg-[#0B1120]/90 backdrop-blur-2xl shadow-lg shadow-black/20">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* ── Brand Logo & Version Badge ───────────────────────────────────── */}
        <div className="flex items-center gap-4 lg:gap-8">
          <Link href="/" className="flex items-center gap-3 group">
            <div className="relative flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-blue-600 via-indigo-600 to-blue-700 shadow-[0_0_20px_rgba(37,99,235,0.5)] group-hover:shadow-[0_0_25px_rgba(37,99,235,0.7)] group-hover:scale-105 transition-all">
              <Shield className="h-5 w-5 text-white" />
              <div className="absolute -bottom-0.5 -right-0.5 h-2.5 w-2.5 rounded-full bg-emerald-400 border-2 border-[#0B1120] animate-pulse" />
            </div>
            <div className="flex flex-col">
              <span className="text-lg font-black tracking-wider text-white font-mono flex items-center gap-1.5">
                OZARK
                <span className="text-[10px] font-bold text-blue-400 bg-blue-500/15 border border-blue-500/30 px-1.5 py-0.2 rounded font-sans">
                  PRO
                </span>
              </span>
              <span className="text-[10px] text-slate-400 font-medium tracking-tight">
                Enterprise Risk Intelligence
              </span>
            </div>
          </Link>

          {/* ── Desktop Navigation Links ───────────────────────────────────── */}
          <nav className="hidden md:flex items-center gap-1.5 ml-2 border-l border-white/10 pl-4 lg:pl-6">
            {navLinks.map((link) => {
              const Icon = link.icon;
              const isActive = pathname === link.href || (link.href !== "/" && pathname.startsWith(link.href));
              return (
                <Link
                  key={link.name}
                  href={link.href}
                  className={`inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
                    isActive
                      ? "bg-blue-600/25 text-white border border-blue-400/50 shadow-[0_0_15px_rgba(37,99,235,0.25)]"
                      : "text-slate-300 hover:text-white hover:bg-white/[0.08] border border-transparent"
                  }`}
                >
                  <Icon className={`h-4 w-4 ${isActive ? "text-blue-400" : "text-slate-400"}`} />
                  <span>{link.name}</span>
                  {link.badge && (
                    <span className={`text-[9px] font-mono px-1.5 py-0.5 rounded-full border ${link.badgeColor}`}>
                      {link.badge}
                    </span>
                  )}
                </Link>
              );
            })}
          </nav>
        </div>

        {/* ── Right Actions: Status, Dashboard Quick Link, Sign In & Register ─── */}
        <div className="hidden sm:flex items-center gap-2.5">
          {/* Engine Status pill (desktop) */}
          <div className="hidden lg:flex items-center gap-1.5 rounded-xl border border-emerald-500/30 bg-emerald-500/10 px-2.5 py-1 text-[11px] font-mono font-semibold text-emerald-400">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
            <span>Risk Engine Online</span>
          </div>

          {isAuthenticated ? (
            <div className="flex items-center gap-2.5 pl-2 border-l border-white/10">
              <Link href="/dashboard">
                <Button
                  size="sm"
                  className="h-9 px-3.5 rounded-xl text-xs font-bold bg-blue-600 hover:bg-blue-500 text-white shadow-[0_0_15px_rgba(37,99,235,0.4)] flex items-center gap-1.5"
                >
                  <BarChart3 className="h-3.5 w-3.5" />
                  Dashboard
                </Button>
              </Link>

              <div className="flex items-center gap-2 text-xs font-medium text-slate-200 bg-[#0F172A] border border-white/15 px-3 py-1.5 rounded-xl">
                <User className="h-3.5 w-3.5 text-blue-400" />
                <span className="max-w-[110px] truncate">{user?.name || user?.email || "Analyst"}</span>
              </div>

              <Button
                variant="ghost"
                size="sm"
                onClick={logout}
                className="h-9 px-2.5 text-slate-400 hover:text-rose-300 hover:bg-rose-500/15 rounded-xl border border-transparent hover:border-rose-500/30"
                title="Sign Out"
              >
                <LogOut className="h-4 w-4 mr-1" />
                <span className="text-xs">Exit</span>
              </Button>
            </div>
          ) : (
            <div className="flex items-center gap-2 pl-2 border-l border-white/10">
              {/* Quick Demo Access Button */}
              <Button
                size="sm"
                variant="outline"
                onClick={handleQuickDemo}
                disabled={isDemoLoading}
                className="h-9 px-3 rounded-xl text-xs font-bold border-amber-500/30 bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 hover:text-amber-200 transition-all gap-1.5 shadow-[0_0_12px_rgba(245,158,11,0.15)]"
                title="Log in immediately using the demo account"
              >
                <Zap className="h-3.5 w-3.5 fill-amber-400 text-amber-400" />
                {isDemoLoading ? "Loading..." : "Quick Demo"}
              </Button>

              {/* Sign In Button */}
              <Link href="/login">
                <Button
                  variant="outline"
                  size="sm"
                  className="h-9 px-3.5 text-xs font-semibold text-slate-200 hover:text-white border-white/20 bg-white/[0.05] hover:bg-white/[0.12] rounded-xl transition-all flex items-center gap-1.5"
                >
                  <LogIn className="h-3.5 w-3.5 text-blue-400" />
                  Sign In
                </Button>
              </Link>

              {/* Register Button */}
              <Link href="/register">
                <Button
                  size="sm"
                  className="h-9 px-4 text-xs font-bold bg-blue-600 hover:bg-blue-500 text-white rounded-xl shadow-[0_0_20px_rgba(37,99,235,0.45)] hover:shadow-[0_0_25px_rgba(37,99,235,0.6)] transition-all flex items-center gap-1.5"
                >
                  <UserPlus className="h-3.5 w-3.5" />
                  Register
                </Button>
              </Link>
            </div>
          )}
        </div>

        {/* ── Mobile Hamburger Button ──────────────────────────────────────── */}
        <div className="flex md:hidden items-center gap-2">
          {!isAuthenticated && (
            <Button
              size="sm"
              onClick={handleQuickDemo}
              disabled={isDemoLoading}
              className="h-8 px-2.5 rounded-lg text-[11px] font-bold bg-amber-500/15 border border-amber-500/30 text-amber-300 flex items-center gap-1"
            >
              <Zap className="h-3 w-3 fill-amber-400" />
              Demo
            </Button>
          )}
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="text-slate-200 hover:text-white bg-white/[0.05] border border-white/10 rounded-xl"
            aria-label="Toggle navigation menu"
          >
            {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </Button>
        </div>
      </div>

      {/* ── Mobile Menu Slide-down Drawer ─────────────────────────────────── */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-white/15 bg-[#0B1120]/98 backdrop-blur-2xl px-4 py-5 space-y-4 shadow-2xl">
          {/* Navigation Links */}
          <div className="space-y-1.5">
            <div className="px-2 pb-1 text-[10px] font-mono uppercase tracking-wider text-slate-400 font-bold">
              Navigation
            </div>
            {navLinks.map((link) => {
              const Icon = link.icon;
              const isActive = pathname === link.href || (link.href !== "/" && pathname.startsWith(link.href));
              return (
                <Link
                  key={link.name}
                  href={link.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-colors ${
                    isActive
                      ? "bg-blue-600/25 text-white border border-blue-500/40"
                      : "text-slate-300 hover:bg-white/[0.06] hover:text-white"
                  }`}
                >
                  <div className="flex items-center gap-2.5">
                    <Icon className={`h-4 w-4 ${isActive ? "text-blue-400" : "text-slate-400"}`} />
                    <span>{link.name}</span>
                  </div>
                  {link.badge && (
                    <span className={`text-[9px] font-mono px-1.5 py-0.5 rounded-full border ${link.badgeColor}`}>
                      {link.badge}
                    </span>
                  )}
                </Link>
              );
            })}
          </div>

          {/* Mobile Auth & Account Actions */}
          <div className="pt-3 border-t border-white/10 space-y-2">
            <div className="px-2 text-[10px] font-mono uppercase tracking-wider text-slate-400 font-bold">
              Account & Access
            </div>

            {isAuthenticated ? (
              <div className="flex flex-col gap-2 p-2 rounded-xl bg-white/[0.03] border border-white/10">
                <div className="flex items-center gap-2 text-xs text-slate-200">
                  <User className="h-4 w-4 text-blue-400" />
                  <span className="truncate font-medium">{user?.email}</span>
                </div>
                <div className="grid grid-cols-2 gap-2 pt-1">
                  <Link href="/dashboard" onClick={() => setMobileMenuOpen(false)}>
                    <Button size="sm" className="w-full text-xs font-bold bg-blue-600 hover:bg-blue-500 text-white rounded-xl">
                      <BarChart3 className="h-3.5 w-3.5 mr-1" />
                      Dashboard
                    </Button>
                  </Link>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => {
                      logout();
                      setMobileMenuOpen(false);
                    }}
                    className="text-xs text-rose-300 border-rose-500/30 bg-rose-500/10 hover:bg-rose-500/20 rounded-xl"
                  >
                    <LogOut className="h-3.5 w-3.5 mr-1" />
                    Sign Out
                  </Button>
                </div>
              </div>
            ) : (
              <div className="space-y-2">
                <Button
                  size="sm"
                  onClick={() => {
                    handleQuickDemo();
                    setMobileMenuOpen(false);
                  }}
                  className="w-full h-10 text-xs font-bold bg-amber-500/15 hover:bg-amber-500/25 border border-amber-500/40 text-amber-300 rounded-xl flex items-center justify-center gap-1.5 shadow-[0_0_15px_rgba(245,158,11,0.2)]"
                >
                  <Zap className="h-4 w-4 fill-amber-400 text-amber-400" />
                  Instant Demo Login (No Password)
                </Button>

                <div className="grid grid-cols-2 gap-2">
                  <Link href="/login" onClick={() => setMobileMenuOpen(false)}>
                    <Button variant="outline" className="w-full h-10 text-xs font-bold rounded-xl border-white/20 bg-white/[0.05] text-white">
                      <LogIn className="h-3.5 w-3.5 mr-1 text-blue-400" />
                      Sign In
                    </Button>
                  </Link>
                  <Link href="/register" onClick={() => setMobileMenuOpen(false)}>
                    <Button className="w-full h-10 text-xs font-bold bg-blue-600 hover:bg-blue-500 text-white rounded-xl shadow-[0_0_15px_rgba(37,99,235,0.4)]">
                      <UserPlus className="h-3.5 w-3.5 mr-1" />
                      Register
                    </Button>
                  </Link>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  );
}
