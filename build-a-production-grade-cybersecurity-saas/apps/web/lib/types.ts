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

export type RiskSimulationFixImpact = {
  finding_key: string;
  title: string;
  category: string;
  severity: Severity;
  score_impact: number;
  risk_reduction: number;
};

export type RiskSimulationResponse = {
  current_score: number;
  predicted_score: number;
  improvement: number;
  improvement_percentage: number;
  estimated_risk_reduction: number;
  selected_finding_keys: string[];
  top_fixes: RiskSimulationFixImpact[];
  comparison: Array<{ label: string; score: number }>;
};
