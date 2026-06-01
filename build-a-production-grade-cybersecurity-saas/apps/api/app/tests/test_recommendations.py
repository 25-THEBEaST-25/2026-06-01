from app.schemas.security import Finding
from app.services.recommendations import RecommendationEngine


def test_recommendations_ignore_passing_findings() -> None:
    recommendations = RecommendationEngine().generate(
        [
            Finding(
                category="security_headers",
                key="content_security_policy",
                status="pass",
                severity="info",
                message="present",
            ),
            Finding(
                category="email_security",
                key="dmarc",
                status="fail",
                severity="high",
                message="missing",
            ),
        ]
    )

    assert len(recommendations) == 1
    assert recommendations[0].finding_key == "dmarc"
