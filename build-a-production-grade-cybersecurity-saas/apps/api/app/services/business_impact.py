from app.schemas.security import BusinessImpactEstimate, BusinessImpactRequest, BusinessImpactResponse, Finding


class BusinessImpactEstimator:
    def estimate(self, payload: BusinessImpactRequest) -> BusinessImpactResponse:
        estimates = [self._estimate_finding(finding) for finding in payload.findings]
        return BusinessImpactResponse(domain=payload.domain, estimates=estimates)

    def _estimate_finding(self, finding: Finding) -> BusinessImpactEstimate:
        profile = IMPACT_PROFILES.get(finding.key, DEFAULT_IMPACT_PROFILE)
        severity_likelihood = {
            "critical": "Very high",
            "high": "High",
            "medium": "Medium",
            "low": "Low",
            "info": "Low",
        }
        likelihood = profile.get("likelihood") or severity_likelihood[finding.severity]

        return BusinessImpactEstimate(
            finding_key=finding.key,
            finding_title=profile["title"],
            technical_risk=finding.severity.title(),
            likelihood_of_exploitation=likelihood,
            business_impact=profile["business_impact"],
            financial_impact_range=profile["financial_impact_range"],
            operational_impact=profile["operational_impact"],
        )


IMPACT_PROFILES = {
    "ssl_certificate": {
        "title": "Expired SSL Certificate",
        "likelihood": "Medium",
        "business_impact": [
            "Customers may lose trust when browser warnings appear.",
            "Conversion and support volume may be affected during the outage window.",
        ],
        "financial_impact_range": "₹10,000 - ₹50,000",
        "operational_impact": "Potential website downtime, failed integrations, and emergency certificate replacement.",
    },
    "dmarc": {
        "title": "DMARC Not Enforced",
        "likelihood": "High",
        "business_impact": [
            "Attackers can impersonate the brand in phishing campaigns.",
            "Customers and suppliers may receive fraudulent payment or credential requests.",
        ],
        "financial_impact_range": "₹50,000 - ₹5,00,000",
        "operational_impact": "Security team investigation, customer communications, and mail deliverability remediation.",
    },
    "spf": {
        "title": "Invalid SPF Record",
        "likelihood": "Medium",
        "business_impact": [
            "Legitimate email may be rejected or marked as suspicious.",
            "Domain spoofing risk increases when sender policy is incomplete.",
        ],
        "financial_impact_range": "₹20,000 - ₹1,50,000",
        "operational_impact": "Email delivery troubleshooting and DNS policy changes across vendors.",
    },
    "dkim": {
        "title": "DKIM Validation Gap",
        "likelihood": "Medium",
        "business_impact": [
            "Email authenticity is harder for recipients to verify.",
            "Marketing and transactional email reputation can degrade.",
        ],
        "financial_impact_range": "₹20,000 - ₹1,00,000",
        "operational_impact": "Mail platform selector discovery, DNS updates, and staged validation.",
    },
    "content_security_policy": {
        "title": "Missing Content-Security-Policy",
        "likelihood": "Medium",
        "business_impact": [
            "Successful script injection could expose customer sessions or sensitive form data.",
            "Incident response may require customer notification and forensic review.",
        ],
        "financial_impact_range": "₹75,000 - ₹7,50,000",
        "operational_impact": "Frontend policy rollout, report-only tuning, and third-party script review.",
    },
    "open_ports": {
        "title": "Unnecessary Public Port Exposure",
        "likelihood": "High",
        "business_impact": [
            "Public services can become entry points for ransomware or data theft.",
            "Attackers may fingerprint exposed systems and target known vulnerabilities.",
        ],
        "financial_impact_range": "₹1,00,000 - ₹10,00,000",
        "operational_impact": "Firewall changes, service owner review, maintenance windows, and monitoring updates.",
    },
}

DEFAULT_IMPACT_PROFILE = {
    "title": "Security Finding",
    "business_impact": [
        "The finding may increase exposure to security incidents.",
        "Delayed remediation can raise investigation and recovery costs.",
    ],
    "financial_impact_range": "₹10,000 - ₹1,00,000",
    "operational_impact": "Owner assignment, validation, remediation, and follow-up scanning.",
}
