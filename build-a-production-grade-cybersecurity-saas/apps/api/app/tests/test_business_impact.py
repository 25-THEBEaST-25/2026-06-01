from app.schemas.security import BusinessImpactRequest, Finding
from app.services.business_impact import BusinessImpactEstimator


def test_business_impact_estimator_maps_ssl_to_financial_impact() -> None:
    response = BusinessImpactEstimator().estimate(
        BusinessImpactRequest(
            domain="example.com",
            findings=[
                Finding(
                    category="ssl",
                    key="ssl_certificate",
                    status="fail",
                    severity="medium",
                    message="Expired SSL certificate",
                )
            ],
        )
    )

    estimate = response.estimates[0]
    assert estimate.finding_title == "Expired SSL Certificate"
    assert estimate.likelihood_of_exploitation == "Medium"
    assert estimate.financial_impact_range == "₹10,000 - ₹50,000"
