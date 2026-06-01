# Cyber Risk Radar

Production-grade cybersecurity SaaS scaffold for SMEs that need continuous cyber risk monitoring, posture assessment, remediation guidance, and PDF reporting.

## Project Structure

```text
cyber-risk-radar/
  apps/
    api/
      app/
        api/v1/            FastAPI routes and auth guards
        core/              settings and JWT/password helpers
        db/                SQLAlchemy session and base model
        models/            PostgreSQL ORM entities
        schemas/           Pydantic contracts
        services/          scanners, risk engine, AI-style recommendations, reports
        tests/             unit tests
      Dockerfile
      pyproject.toml
    web/
      app/                 Next.js App Router screens
      components/          shadcn-style UI and dashboard components
      lib/                 typed API client and shared types
      tests/               Vitest tests
      Dockerfile
      package.json
  docker-compose.yml
  .env.example
```

## Core Modules

- Dashboard: risk gauge, trend chart, active alerts, security recommendations.
- Domain monitoring: WHOIS placeholder, expiry posture, SSL certificate validation and expiry alerts.
- Security header scanner: HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy.
- Email security analyzer: SPF, DKIM guidance, DMARC validation.
- Asset discovery: subdomain discovery hooks, public service and open port analysis.
- Breach monitoring: breach feed integration point with exposed-email findings.
- Risk engine: weighted score across SSL, DNS/domain, email, headers, ports, and breaches.
- Recommendation engine: remediation guidance for each failing or warning finding.
- Reports: downloadable PDF with summary, findings, risk score, and recommendations.
- Authentication: JWT login, role guard dependencies, admin-only route.

## Local Development

```bash
cp .env.example .env
docker compose up --build
```

Web app: http://localhost:3000  
API docs: http://localhost:8000/docs  
API health: http://localhost:8000/api/v1/health

Demo login:

```text
admin@cyberriskradar.dev
ChangeMe123!
```

The frontend includes demo data when `NEXT_PUBLIC_DEMO_TOKEN` is unset, so the UI is browsable before auth wiring is completed.

## Backend

```bash
cd apps/api
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
pytest
uvicorn app.main:app --reload
```

## Frontend

```bash
cd apps/web
npm install
npm run dev
npm run test
```

## Production Notes

- Replace `JWT_SECRET` with a long random secret.
- Move demo users into PostgreSQL-backed user management.
- Add scheduled workers for periodic scans and alert creation.
- Connect breach monitoring to approved commercial or internal feeds.
- Add migrations with Alembic before the first production release.
- Store generated reports in object storage when report history is required.
