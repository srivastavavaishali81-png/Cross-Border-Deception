/**
 * OZARK — Next.js Edge Middleware
 *
 * Protects /dashboard/* routes by checking for a refresh token in localStorage.
 * Note: localStorage is not available at the edge, so we use a cookie-based
 * indicator token written by the client after login.
 *
 * Strategy:
 *   - Client writes a non-httpOnly cookie `ozark_authed=1` after successful login.
 *   - Middleware reads this cookie to gate protected routes.
 *   - Actual token validation happens server-side or via the AuthContext.
 */

import { NextRequest, NextResponse } from "next/server";

const PROTECTED_ROUTES = ["/dashboard"];
const AUTH_ROUTES = ["/login", "/register"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const isAuthed = request.cookies.has("ozark_authed");

  // Redirect unauthenticated users away from protected routes
  if (PROTECTED_ROUTES.some((p) => pathname.startsWith(p)) && !isAuthed) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("callbackUrl", pathname);
    return NextResponse.redirect(loginUrl);
  }

  // Redirect authenticated users away from auth pages
  if (AUTH_ROUTES.some((p) => pathname.startsWith(p)) && isAuthed) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/login", "/register"],
};
