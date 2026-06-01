from app.schemas.security import Finding
from app.services.risk_simulator import RiskImprovementSimulator


def test_simulator_predicts_score_after_selected_fixes() -> None:
    findings = [
        Finding(
            category="email_security",
            key="dmarc",
            status="fail",
            severity="high",
            message="missing dmarc",
        ),
        Finding(
            category="ssl",
            key="ssl_certificate",
            status="fail",
            severity="high",
            message="bad ssl",
        ),
        Finding(
            category="asset_discovery",
            key="open_ports",
            status="warn",
            severity="medium",
            message="ports exposed",
        ),
    ]

    result = RiskImprovementSimulator().simulate(
        findings=findings,
        selected_finding_keys=["dmarc", "ssl_certificate"],
    )

    assert result.predicted_score > result.current_score
    assert result.improvement > 0
    assert result.top_fixes[0].score_impact >= result.top_fixes[-1].score_impact
