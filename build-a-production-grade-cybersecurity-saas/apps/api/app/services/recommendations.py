from app.schemas.security import Finding, Recommendation


class RecommendationEngine:
    def generate(self, findings: list[Finding]) -> list[Recommendation]:
        recommendations: list[Recommendation] = []
        for finding in findings:
            if finding.status == "pass":
                continue
            recommendations.append(
                Recommendation(
                    title=self._title_for(finding),
                    priority=finding.severity if finding.severity != "info" else "low",
                    remediation=self._remediation_for(finding),
                    finding_key=finding.key,
                )
            )
        return recommendations

    def _title_for(self, finding: Finding) -> str:
        labels = {
            "ssl_certificate": "Renew or repair SSL certificate",
            "spf": "Fix SPF configuration",
            "dkim": "Validate DKIM selectors",
            "dmarc": "Publish DMARC policy",
            "open_ports": "Review exposed services",
        }
        return labels.get(finding.key, f"Remediate {finding.key.replace('_', ' ')}")

    def _remediation_for(self, finding: Finding) -> str:
        if finding.category == "security_headers":
            return "Apply the missing header at the edge or application layer and test in report-only mode first where applicable."
        if finding.category == "email_security":
            return "Publish standards-compliant DNS records, start with monitoring policies, then move to enforcement."
        if finding.category == "ssl":
            return "Install a trusted certificate, automate renewal, and monitor expiry with at least 30 days of lead time."
        if finding.key == "open_ports":
            return "Confirm business need for each public service, restrict source IPs, and close unused ports."
        return "Assign an owner, verify the finding, remediate the root cause, and rescan."
