import httpx

from app.schemas.security import Finding

REQUIRED_HEADERS = {
    "strict-transport-security": ("HSTS is enabled.", "Enable HSTS with a long max-age."),
    "content-security-policy": ("CSP is present.", "Add a restrictive Content-Security-Policy."),
    "x-frame-options": ("Clickjacking protection is enabled.", "Set X-Frame-Options or frame-ancestors."),
    "x-content-type-options": ("MIME sniffing protection is enabled.", "Set X-Content-Type-Options: nosniff."),
    "referrer-policy": ("Referrer policy is set.", "Set a privacy-preserving Referrer-Policy."),
}


class SecurityHeaderScanner:
    async def scan(self, domain: str) -> list[Finding]:
        url = f"https://{domain}"
        try:
            async with httpx.AsyncClient(timeout=6, follow_redirects=True) as client:
                response = await client.get(url)
            headers = {key.lower(): value for key, value in response.headers.items()}
        except Exception as exc:
            return [
                Finding(
                    category="security_headers",
                    key="headers_unreachable",
                    status="fail",
                    severity="medium",
                    message="Could not retrieve HTTP response headers.",
                    evidence={"error": str(exc), "url": url},
                )
            ]

        findings: list[Finding] = []
        for header, (pass_message, fail_message) in REQUIRED_HEADERS.items():
            present = header in headers
            findings.append(
                Finding(
                    category="security_headers",
                    key=header.replace("-", "_"),
                    status="pass" if present else "fail",
                    severity="info" if present else "medium",
                    message=pass_message if present else fail_message,
                    evidence={"value": headers.get(header)},
                )
            )
        return findings
