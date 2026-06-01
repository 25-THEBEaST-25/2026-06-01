import type { DashboardResponse, ScanResponse } from "@/lib/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";
const DEMO_TOKEN = process.env.NEXT_PUBLIC_DEMO_TOKEN ?? "";

function authToken() {
  if (DEMO_TOKEN) {
    return DEMO_TOKEN;
  }
  if (typeof window !== "undefined") {
    return window.localStorage.getItem("cyber-risk-radar-token") ?? "";
  }
  return "";
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const token = authToken();
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...init?.headers
    },
    next: { revalidate: 30 }
  });
  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function getDashboard(): Promise<DashboardResponse> {
  if (!authToken()) {
    return demoDashboard;
  }
  return request<DashboardResponse>("/dashboard");
}

export async function scanDomain(domain: string): Promise<ScanResponse> {
  if (!authToken()) {
    return demoScan(domain);
  }
  return request<ScanResponse>("/scans/domain", {
    method: "POST",
    body: JSON.stringify({ domain })
  });
}

export async function login(email: string, password: string): Promise<string> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });
  if (!response.ok) {
    throw new Error("Invalid credentials");
  }
  const payload = (await response.json()) as { access_token: string };
  window.localStorage.setItem("cyber-risk-radar-token", payload.access_token);
  return payload.access_token;
}

const demoDashboard: DashboardResponse = {
  risk_score: 78,
  trend: [
    { date: "May 26", score: 88 },
    { date: "May 27", score: 84 },
    { date: "May 28", score: 80 },
    { date: "May 29", score: 79 },
    { date: "May 30", score: 78 }
  ],
  active_alerts: [
    { severity: "high", title: "DMARC policy missing enforcement", asset: "acme.example", created_at: "2026-05-30" },
    { severity: "medium", title: "CSP header not configured", asset: "app.acme.example", created_at: "2026-05-29" },
    { severity: "low", title: "Certificate expires in 41 days", asset: "portal.acme.example", created_at: "2026-05-28" }
  ],
  recommendations: [
    {
      title: "Publish DMARC enforcement",
      priority: "high",
      remediation: "Move from monitoring to quarantine after validating legitimate senders.",
      finding_key: "dmarc"
    },
    {
      title: "Restrict exposed admin services",
      priority: "medium",
      remediation: "Limit management ports to VPN or identity-aware proxy access.",
      finding_key: "open_ports"
    }
  ]
};

function demoScan(domain: string): ScanResponse {
  return {
    domain,
    risk_score: 78,
    scanned_at: new Date().toISOString(),
    findings: [
      { category: "ssl", key: "ssl_certificate", status: "pass", severity: "info", message: "SSL certificate is valid.", evidence: {} },
      { category: "email_security", key: "dmarc", status: "fail", severity: "high", message: "DMARC record is missing enforcement.", evidence: {} },
      { category: "security_headers", key: "content_security_policy", status: "fail", severity: "medium", message: "Content-Security-Policy is missing.", evidence: {} },
      { category: "asset_discovery", key: "open_ports", status: "warn", severity: "medium", message: "Public HTTP and HTTPS services detected.", evidence: { ports: [80, 443] } }
    ],
    recommendations: demoDashboard.recommendations
  };
}
