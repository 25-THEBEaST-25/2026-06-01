import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Link from "next/link";
import { Activity, FileText, Gauge, LogIn, Network, Radar, ShieldCheck, SlidersHorizontal, Users } from "lucide-react";

import "./globals.css";
import { ThemeProvider } from "@/components/theme-provider";
import { ThemeToggle } from "@/components/theme-toggle";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Cyber Risk Radar",
  description: "Continuous cyber risk monitoring and posture assessment for SMEs"
};

const nav = [
  { href: "/dashboard", label: "Dashboard", icon: Gauge },
  { href: "/domains", label: "Domains", icon: ShieldCheck },
  { href: "/simulator", label: "Simulator", icon: SlidersHorizontal },
  { href: "/assets", label: "Assets", icon: Network },
  { href: "/reports", label: "Reports", icon: FileText },
  { href: "/admin", label: "Admin", icon: Users },
  { href: "/login", label: "Sign in", icon: LogIn }
];

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <div className="min-h-screen">
            <aside className="fixed inset-y-0 left-0 hidden w-64 border-r bg-card lg:block">
              <div className="flex h-16 items-center gap-2 border-b px-6">
                <Radar className="h-6 w-6 text-primary" />
                <span className="text-lg font-semibold">Cyber Risk Radar</span>
              </div>
              <nav className="grid gap-1 p-3">
                {nav.map((item) => (
                  <Link
                    className="flex items-center gap-3 rounded-md px-3 py-2 text-sm text-muted-foreground transition hover:bg-muted hover:text-foreground"
                    href={item.href}
                    key={item.href}
                  >
                    <item.icon className="h-4 w-4" />
                    {item.label}
                  </Link>
                ))}
              </nav>
            </aside>
            <main className="lg:pl-64">
              <header className="sticky top-0 z-10 flex h-16 items-center justify-between border-b bg-background/95 px-4 backdrop-blur md:px-8">
                <div>
                  <p className="text-sm text-muted-foreground">Continuous security posture assessment</p>
                  <h1 className="text-lg font-semibold">Cyber Risk Radar</h1>
                </div>
                <div className="flex items-center gap-2">
                  <Activity className="h-4 w-4 text-primary" />
                  <span className="hidden text-sm text-muted-foreground sm:inline">Live monitoring</span>
                  <ThemeToggle />
                </div>
              </header>
              <div className="p-4 md:p-8">{children}</div>
            </main>
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
