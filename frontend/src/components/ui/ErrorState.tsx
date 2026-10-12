"use client";

import React from "react";
import { AlertTriangle, RefreshCw } from "lucide-react";
import { Button } from "./button";

interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
  className?: string;
}

export function ErrorState({
  title = "Data Stream Interrupted",
  message = "An unexpected error occurred while loading intelligence records. Please verify your connection or try again.",
  onRetry,
  className = "",
}: ErrorStateProps) {
  return (
    <div
      className={`glass-card flex flex-col items-center justify-center p-8 text-center rounded-3xl border border-rose-500/20 bg-rose-500/5 ${className}`}
    >
      <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-rose-500/10 text-rose-400 mb-4 border border-rose-500/20 shadow-[0_0_25px_rgba(239,68,68,0.2)]">
        <AlertTriangle className="h-8 w-8 animate-pulse" />
      </div>

      <h3 className="text-xl font-bold text-white tracking-tight">{title}</h3>
      <p className="mt-2 max-w-md text-xs leading-relaxed text-slate-400">{message}</p>

      {onRetry && (
        <Button
          onClick={onRetry}
          variant="outline"
          className="mt-6 gap-2 rounded-xl border-white/10 bg-[#0F172A] hover:bg-white/10 text-white text-xs font-semibold"
        >
          <RefreshCw className="h-3.5 w-3.5" />
          Retry Request
        </Button>
      )}
    </div>
  );
}
