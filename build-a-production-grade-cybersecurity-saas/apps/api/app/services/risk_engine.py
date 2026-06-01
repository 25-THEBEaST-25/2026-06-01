from app.schemas.security import Finding

WEIGHTS = {
    "ssl": 18,
    "domain": 8,
    "email_security": 22,
    "security_headers": 20,
    "asset_discovery": 17,
    "breach_monitoring": 15,
}

SEVERITY_MULTIPLIERS = {
    "critical": 1.0,
    "high": 0.75,
    "medium": 0.45,
    "low": 0.2,
    "info": 0.0,
}


class RiskEngine:
    def calculate(self, findings: list[Finding]) -> float:
        penalty = 0.0
        for finding in findings:
            if finding.status == "pass":
                continue
            category_weight = WEIGHTS.get(finding.category, 5)
            penalty += category_weight * SEVERITY_MULTIPLIERS[finding.severity]
        return max(0.0, round(100 - min(penalty, 100), 1))
