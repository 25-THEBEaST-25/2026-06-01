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

export type BusinessImpactEstimate = {
  finding_key: string;
  finding_title: string;
  technical_risk: string;
  likelihood_of_exploitation: string;
  business_impact: string[];
  financial_impact_range: string;
  operational_impact: string;
};

export type BusinessImpactResponse = {
  domain: string | null;
  estimates: BusinessImpactEstimate[];
};

export type ScanJob = {
  id: string;
  organization_id: string;
  domain: string;
  status: "queued" | "running" | "completed" | "failed";
  progress: number;
  result: ScanResponse | null;
  error: string | null;
  created_at: string;
  updated_at: string;
};

export type AlertStatus = "open" | "acknowledged" | "resolved" | "suppressed" | "false_positive";

export type AlertRead = {
  id: string;
  asset: string;
  severity: Severity;
  title: string;
  description: string;
  status: AlertStatus;
  resolution_note: string | null;
  created_at: string;
  updated_at: string | null;
};

export type ScanSchedule = {
  id: string;
  organization_id: string;
  domain: string;
  cadence: "daily" | "weekly" | "monthly";
  enabled: boolean;
  next_run_at: string;
};

export type ReportMetadata = {
  id: string;
  domain: string;
  report_type: string;
  storage_uri: string;
  created_at: string;
};
