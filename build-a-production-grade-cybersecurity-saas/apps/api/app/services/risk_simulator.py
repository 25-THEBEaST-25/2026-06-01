from copy import deepcopy

from app.schemas.security import Finding, RiskSimulationFixImpact, RiskSimulationResponse
from app.services.risk_engine import RiskEngine


class RiskImprovementSimulator:
    def __init__(self) -> None:
        self.risk_engine = RiskEngine()

    def simulate(
        self,
        findings: list[Finding],
        selected_finding_keys: list[str],
        current_score: float | None = None,
    ) -> RiskSimulationResponse:
        modeled_baseline_score = self.risk_engine.calculate(findings)
        baseline_score = current_score if current_score is not None else modeled_baseline_score
        selected_keys = set(selected_finding_keys)
        simulated_findings = [self._fixed_finding(finding) for finding in findings if finding.key in selected_keys]
        unchanged_findings = [finding for finding in findings if finding.key not in selected_keys]
        modeled_predicted_score = self.risk_engine.calculate([*simulated_findings, *unchanged_findings])
        modeled_improvement = modeled_predicted_score - modeled_baseline_score
        predicted_score = min(100.0, round(baseline_score + modeled_improvement, 1))
        improvement = round(predicted_score - baseline_score, 1)
        improvement_percentage = round((improvement / baseline_score) * 100, 1) if baseline_score else 0

        return RiskSimulationResponse(
            current_score=baseline_score,
            predicted_score=predicted_score,
            improvement=improvement,
            improvement_percentage=improvement_percentage,
            estimated_risk_reduction=improvement,
            selected_finding_keys=selected_finding_keys,
            top_fixes=self._rank_fix_impacts(findings, modeled_baseline_score),
            comparison=[
                {"label": "Current", "score": baseline_score},
                {"label": "Predicted", "score": predicted_score},
            ],
        )

    def _rank_fix_impacts(
        self, findings: list[Finding], baseline_score: float
    ) -> list[RiskSimulationFixImpact]:
        impacts: list[RiskSimulationFixImpact] = []
        actionable_findings = [finding for finding in findings if finding.status != "pass"]

        for finding in actionable_findings:
            simulated = [
                self._fixed_finding(candidate) if candidate.key == finding.key else candidate
                for candidate in findings
            ]
            score_after_fix = self.risk_engine.calculate(simulated)
            impacts.append(
                RiskSimulationFixImpact(
                    finding_key=finding.key,
                    title=self._label_for(finding),
                    category=finding.category,
                    severity=finding.severity,
                    score_impact=round(score_after_fix - baseline_score, 1),
                    risk_reduction=round(score_after_fix - baseline_score, 1),
                )
            )

        return sorted(impacts, key=lambda impact: impact.score_impact, reverse=True)

    def _fixed_finding(self, finding: Finding) -> Finding:
        fixed = deepcopy(finding)
        fixed.status = "pass"
        fixed.severity = "info"
        fixed.message = f"Simulated fix applied for {finding.key.replace('_', ' ')}."
        return fixed

    def _label_for(self, finding: Finding) -> str:
        labels = {
            "dmarc": "Enable DMARC enforcement",
            "spf": "Fix SPF record",
            "dkim": "Validate DKIM signing",
            "ssl_certificate": "Renew SSL certificate",
            "open_ports": "Close unnecessary public ports",
            "content_security_policy": "Add Content-Security-Policy",
            "strict_transport_security": "Enable HSTS",
        }
        return labels.get(finding.key, f"Fix {finding.key.replace('_', ' ')}")
