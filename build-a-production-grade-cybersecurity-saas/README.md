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
- Risk improvement simulator: models selected remediations, before/after score, percentage lift, and fix impact.
- Business impact estimator: translates technical findings into exploitation likelihood, operational impact, and financial impact ranges.
- Recommendation engine: remediation guidance for each failing or warning finding.
- Reports: downloadable PDF with summary, findings, risk score, and recommendations.
- Authentication: JWT login, role guard dependencies, admin-only route.

## Production Efficiency Updates

- Background scan jobs: `POST /api/v1/scans/domain/jobs` enqueues scans and `GET /api/v1/scans/jobs/{id}` returns job status.
- PostgreSQL persistence layer: ORM entities and repositories cover tenants, assets, scans, findings, alerts, reports, jobs, schedules, and audit logs.
- Alembic migrations: initial production schema lives under `apps/api/alembic`.
- Multi-tenant scoping: APIs accept `X-Organization-Id` and enforce organization-aware scan limits.
- Scheduled monitoring: schedule APIs support daily, weekly, and monthly scan cadence.
- Scan result caching: in-memory TTL cache shields repeated scanner calls; Redis is available for production adapters.
- Queue and rate limits: Docker includes Redis, worker, scheduler, and per-organization scan throttling.
- Alert lifecycle: alerts support open, acknowledged, resolved, suppressed, and false positive states.
- Auth hardening: access and refresh tokens are issued, MFA-ready user fields exist, and audit events track sensitive actions.
- Report persistence: report metadata is stored through a report store abstraction.
- Observability: request IDs, response timing, metrics, structured logging hooks, and audit logs are included.
- Security hardening: API/frontend security headers, CORS controls, secret validation, and non-root Docker users are configured.
- Scanner architecture: scanner registry normalizes scanners behind a common interface for future integrations.
- Frontend performance: loading skeletons, async scan job UX, typed API clients, and security middleware are included.

## Local Development

```bash
cp .env.example .env
docker compose up --build
```

Web app: http://localhost:3000  
API docs: http://localhost:8000/docs  
API health: http://localhost:8000/api/v1/health
Metrics: http://localhost:8000/api/v1/metrics

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
- Replace in-memory dev adapters with Redis/PostgreSQL-backed implementations where marked.
- Store generated report binaries in object storage while keeping metadata in PostgreSQL.
