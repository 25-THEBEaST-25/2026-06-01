from datetime import UTC, datetime, timedelta
import ssl
import socket

from app.schemas.security import Finding


class DomainMonitor:
    async def scan(self, domain: str) -> list[Finding]:
        findings: list[Finding] = []
        findings.extend(await self._ssl_findings(domain))
        findings.append(self._whois_findings(domain))
        return findings

    async def _ssl_findings(self, domain: str) -> list[Finding]:
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=4) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as tls:
                    cert = tls.getpeercert()
            expires_at = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=UTC)
            days_remaining = (expires_at - datetime.now(UTC)).days
            status = "pass" if days_remaining > 30 else "warn"
            severity = "info" if status == "pass" else "medium"
            return [
                Finding(
                    category="ssl",
                    key="ssl_certificate",
                    status=status,
                    severity=severity,
                    message=f"SSL certificate expires in {days_remaining} days.",
                    evidence={"expires_at": expires_at.isoformat(), "days_remaining": days_remaining},
                )
            ]
        except Exception as exc:
            return [
                Finding(
                    category="ssl",
                    key="ssl_certificate",
                    status="fail",
                    severity="high",
                    message="SSL certificate validation failed.",
                    evidence={"error": str(exc)},
                )
            ]

    def _whois_findings(self, domain: str) -> Finding:
        try:
            import whois

            result = whois.whois(domain)
            expiry = result.expiration_date
            if isinstance(expiry, list):
                expiry = min(date for date in expiry if date)
            if not expiry:
                raise ValueError("WHOIS response did not include an expiration date")
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=UTC)
            days_remaining = (expiry - datetime.now(UTC)).days
            status = "pass" if days_remaining > 45 else "warn"
            return Finding(
                category="domain",
                key="domain_expiry",
                status=status,
                severity="info" if status == "pass" else "medium",
                message=f"Domain registration expires in {days_remaining} days.",
                evidence={"domain": domain, "expires_at": expiry.date().isoformat()},
            )
        except Exception as exc:
            fallback_expiry = datetime.now(UTC) + timedelta(days=180)
            return Finding(
                category="domain",
                key="domain_expiry",
                status="warn",
                severity="low",
                message="WHOIS lookup could not confirm domain expiry.",
                evidence={
                    "domain": domain,
                    "fallback_review_by": fallback_expiry.date().isoformat(),
                    "error": str(exc),
                },
            )
