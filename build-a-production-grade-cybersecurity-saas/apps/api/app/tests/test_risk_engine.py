from app.schemas.security import Finding
from app.services.risk_engine import RiskEngine


def test_risk_engine_penalizes_failed_high_severity_findings() -> None:
    score = RiskEngine().calculate(
        [
            Finding(
                category="ssl",
                key="ssl_certificate",
                status="fail",
                severity="high",
                message="bad ssl",
            ),
            Finding(
                category="security_headers",
                key="hsts",
                status="pass",
                severity="info",
                message="ok",
            ),
        ]
    )

    assert score == 86.5


def test_risk_engine_never_goes_below_zero() -> None:
    findings = [
        Finding(
            category="email_security",
            key=f"finding_{index}",
            status="fail",
            severity="critical",
            message="critical",
        )
        for index in range(10)
    ]

    assert RiskEngine().calculate(findings) == 0
