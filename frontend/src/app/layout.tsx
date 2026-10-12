import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/contexts/AuthContext";
import { Navbar } from "@/components/layout/Navbar";
import { TickerTape } from "@/components/layout/TickerTape";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });
const mono = JetBrains_Mono({ subsets: ["latin"], variable: "--font-mono" });

export const metadata: Metadata = {
  title: {
    default: "OZARK — Enterprise Risk & Intelligence Platform",
    template: "%s | OZARK",
  },
  description: "High-frequency corporate risk surveillance, Neo4j relationship graphs, and ML forensic analytics.",
  keywords: ["OZARK", "Fintech", "Risk Intelligence", "Neo4j", "Forensics", "Knowledge Graph"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark" suppressHydrationWarning>
      <body className={`${inter.variable} ${mono.variable} font-sans bg-[#0B1120] text-slate-100 min-h-screen antialiased fintech-grid`}>
        <AuthProvider>
          <div className="relative min-h-screen flex flex-col">
            {/* Ambient Background Radial Glows */}
            <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
              <div className="absolute -top-[20%] left-1/2 -translate-x-1/2 w-[1000px] h-[500px] rounded-full bg-blue-600/10 blur-[130px]" />
              <div className="absolute top-[40%] right-[-10%] w-[600px] h-[600px] rounded-full bg-emerald-500/5 blur-[150px]" />
              <div className="absolute bottom-[-10%] left-[-10%] w-[700px] h-[500px] rounded-full bg-indigo-600/10 blur-[160px]" />
            </div>

            <Navbar />
            <TickerTape />

            <div className="relative z-10 flex-1">
              {children}
            </div>

            {/* Fintech Footer */}
            <footer className="relative z-10 border-t border-white/[0.06] bg-[#0B1120]/90 backdrop-blur-xl py-8 mt-20">
              <div className="mx-auto max-w-7xl px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-400">
                <div className="flex items-center gap-3">
                  <span className="font-mono font-bold text-white tracking-wider">OZARK INTEL</span>
                  <span>•</span>
                  <span>Institutional Risk Surveillance Engine v2.4</span>
                </div>
                <div className="flex items-center gap-6">
                  <span className="flex items-center gap-1.5 text-emerald-400 font-mono">
                    <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
                    SEBI / MCA / Kite Live Pipeline
                  </span>
                  <span>© 2026 OZARK Corp.</span>
                </div>
              </div>
            </footer>
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}
