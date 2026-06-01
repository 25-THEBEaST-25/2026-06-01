export type FindingStatus = "pass" | "warn" | "fail";
export type Severity = "critical" | "high" | "medium" | "low" | "info";

export type Finding = {
  category: string;
  key: string;
  status: FindingStatus;
  severity: Severity;
  message: string;
  evidence: Record<string, unknown>;
};

export type Recommendation = {
  title: string;
  priority: Exclude<Severity, "info">;
  remediation: string;
  finding_key: string;
};

export type ScanResponse = {
  domain: string;
  risk_score: number;
  findings: Finding[];
  recommendations: Recommendation[];
  scanned_at: string;
};

export type DashboardResponse = {
  risk_score: number;
  trend: Array<{ date: string; score: number }>;
  active_alerts: Array<{ severity: Severity; title: string; asset: string; created_at: string }>;
  recommendations: Recommendation[];
};
