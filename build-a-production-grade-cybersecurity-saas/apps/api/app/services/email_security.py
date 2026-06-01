import dns.resolver

from app.schemas.security import Finding


class EmailSecurityAnalyzer:
    async def scan(self, domain: str) -> list[Finding]:
        return [
            self._txt_check(domain, "spf", lambda txt: txt.startswith("v=spf1")),
            self._txt_check(f"_dmarc.{domain}", "dmarc", lambda txt: txt.startswith("v=DMARC1")),
            self._dkim_hint(domain),
        ]

    def _txt_check(self, name: str, key: str, predicate) -> Finding:
        try:
            answers = dns.resolver.resolve(name, "TXT")
            values = ["".join(part.decode() for part in answer.strings) for answer in answers]
            matched = any(predicate(value) for value in values)
            return Finding(
                category="email_security",
                key=key,
                status="pass" if matched else "fail",
                severity="info" if matched else "high",
                message=f"{key.upper()} record {'is valid' if matched else 'was not found or invalid'}.",
                evidence={"records": values},
            )
        except Exception as exc:
            return Finding(
                category="email_security",
                key=key,
                status="fail",
                severity="high",
                message=f"{key.upper()} lookup failed.",
                evidence={"error": str(exc), "name": name},
            )

    def _dkim_hint(self, domain: str) -> Finding:
        return Finding(
            category="email_security",
            key="dkim",
            status="warn",
            severity="medium",
            message="DKIM requires selector discovery; configure known selectors for deep validation.",
            evidence={"domain": domain, "common_selectors": ["default", "google", "selector1"]},
        )
