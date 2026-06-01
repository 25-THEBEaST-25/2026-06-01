import type {
  BusinessImpactResponse,
  DashboardResponse,
  Finding,
  RiskSimulationResponse,
  ScanResponse
} from "@/lib/types";

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

export async function simulateRiskImprovement(
  currentScore: number,
  findings: Finding[],
  selectedFindingKeys: string[]
): Promise<RiskSimulationResponse> {
  if (!authToken()) {
    return demoSimulation(currentScore, findings, selectedFindingKeys);
  }
  return request<RiskSimulationResponse>("/risk/simulate", {
    method: "POST",
    body: JSON.stringify({
      current_score: currentScore,
      findings,
      selected_finding_keys: selectedFindingKeys
    })
  });
}

export async function estimateBusinessImpact(
  domain: string,
  findings: Finding[]
): Promise<BusinessImpactResponse> {
  if (!authToken()) {
    return demoBusinessImpact(domain, findings);
  }
  return request<BusinessImpactResponse>("/business-impact/estimate", {
    method: "POST",
    body: JSON.stringify({ domain, findings })
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

function demoSimulation(
  currentScore: number,
  findings: Finding[],
  selectedFindingKeys: string[]
): RiskSimulationResponse {
  const impactByKey: Record<string, number> = {
    dmarc: 10,
    ssl_certificate: 7,
    open_ports: 5,
    content_security_policy: 4
  };
  const improvement = selectedFindingKeys.reduce((total, key) => total + (impactByKey[key] ?? 3), 0);
  const predictedScore = Math.min(100, currentScore + improvement);
  const topFixes = findings
    .filter((finding) => finding.status !== "pass")
    .map((finding) => ({
      finding_key: finding.key,
      title: demoFixLabel(finding.key),
      category: finding.category,
      severity: finding.severity,
      score_impact: impactByKey[finding.key] ?? 3,
      risk_reduction: impactByKey[finding.key] ?? 3
    }))
    .sort((a, b) => b.score_impact - a.score_impact);

  return {
    current_score: currentScore,
    predicted_score: predictedScore,
    improvement: predictedScore - currentScore,
    improvement_percentage: Number((((predictedScore - currentScore) / currentScore) * 100).toFixed(1)),
    estimated_risk_reduction: predictedScore - currentScore,
    selected_finding_keys: selectedFindingKeys,
    top_fixes: topFixes,
    comparison: [
      { label: "Current", score: currentScore },
      { label: "Predicted", score: predictedScore }
    ]
  };
}

function demoFixLabel(key: string) {
  const labels: Record<string, string> = {
    dmarc: "Enable DMARC enforcement",
    ssl_certificate: "Renew SSL certificate",
    open_ports: "Close unnecessary public ports",
    content_security_policy: "Add Content-Security-Policy"
  };
  return labels[key] ?? `Fix ${key.replaceAll("_", " ")}`;
}

function demoBusinessImpact(domain: string, findings: Finding[]): BusinessImpactResponse {
  const profiles: Record<
    string,
    Omit<BusinessImpactResponse["estimates"][number], "finding_key" | "technical_risk">
  > = {
    ssl_certificate: {
      finding_title: "Expired SSL Certificate",
      likelihood_of_exploitation: "Medium",
      business_impact: ["Customers may lose trust.", "Potential website downtime."],
      financial_impact_range: "₹10,000 - ₹50,000",
      operational_impact: "Emergency certificate replacement and customer support follow-up."
    },
    dmarc: {
      finding_title: "DMARC Not Enforced",
      likelihood_of_exploitation: "High",
      business_impact: ["Attackers can impersonate the brand.", "Payment or credential phishing risk increases."],
      financial_impact_range: "₹50,000 - ₹5,00,000",
      operational_impact: "Mail policy rollout, investigation, and customer communications."
    },
    open_ports: {
      finding_title: "Unnecessary Public Port Exposure",
      likelihood_of_exploitation: "High",
      business_impact: ["Exposed services can become intrusion paths.", "Attackers can fingerprint public systems."],
      financial_impact_range: "₹1,00,000 - ₹10,00,000",
      operational_impact: "Firewall changes, owner review, and monitoring updates."
    },
    content_security_policy: {
      finding_title: "Missing Content-Security-Policy",
      likelihood_of_exploitation: "Medium",
      business_impact: ["Script injection can expose sessions or form data.", "Forensic review may be required."],
      financial_impact_range: "₹75,000 - ₹7,50,000",
      operational_impact: "Report-only tuning and third-party script review."
    }
  };

  return {
    domain,
    estimates: findings.map((finding) => {
      const profile = profiles[finding.key] ?? {
        finding_title: "Security Finding",
        likelihood_of_exploitation: finding.severity === "high" ? "High" : "Medium",
        business_impact: ["The finding may increase exposure to security incidents."],
        financial_impact_range: "₹10,000 - ₹1,00,000",
        operational_impact: "Owner assignment, remediation, and follow-up scanning."
      };
      return {
        finding_key: finding.key,
        technical_risk: titleCase(finding.severity),
        ...profile
      };
    })
  };
}

function titleCase(value: string) {
  return `${value.slice(0, 1).toUpperCase()}${value.slice(1)}`;
}
