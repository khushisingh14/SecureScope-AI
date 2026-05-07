# SecureScope AI

SecureScope AI is a production-style full-stack cybersecurity assessment platform for importing scanner output, normalizing vulnerabilities, generating AI-assisted analysis, scoring security posture, and exporting professional penetration testing reports.

## Stack

- Frontend: React, Tailwind CSS, Framer Motion, Recharts, Axios
- Backend: FastAPI, SQLAlchemy, PostgreSQL-ready configuration with the modern psycopg driver
- AI: OpenRouter chat completions API with an offline fallback when no key is configured
- Reports: ReportLab PDF generation

## Local Development

Backend, from the repository root:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r backend\requirements.txt
copy backend\.env.example backend\.env
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

From the repository root, seed demo data:

```bash
python -m backend.scripts.seed_demo
```

Frontend:

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

Default demo credentials after seeding:

- Email: `analyst@securescope.ai`
- Password: `SecureScope123!`

## Scanner Imports

Supported development samples are in `sample-scans/`:

- `nmap-sample.xml`
- `burp-sample.xml`
- `nikto-sample.txt`
- `sslyze-sample.json`

All imported findings are normalized to:

```json
{
  "title": "string",
  "severity": "Critical | High | Medium | Low | Informational",
  "description": "string",
  "affected_host": "string",
  "remediation": "string",
  "references": "string",
  "source": "string"
}
```

## Security Scoring

Severity weights:

- Critical: 10
- High: 7
- Medium: 5
- Low: 2
- Informational: 1

The posture score starts from 100 and decreases based on weighted findings for the scan or workspace.

## Docker

```bash
docker compose up --build
```

Services:

- Frontend: `http://localhost:8080`
- Backend: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

## Environment Variables

Important variables:

- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `OPENROUTER_API_KEY`
- `OPENROUTER_MODEL`
- `CORS_ORIGINS`
- `VITE_API_URL`

Use `.env.example`, `backend/.env.example`, and `frontend/.env.example` as templates.

## Render Deployment

`render.yaml` defines:

- Dockerized FastAPI web service
- Static React frontend
- Managed PostgreSQL database

Set `OPENROUTER_API_KEY` in Render as a secret environment variable before enabling live AI analysis.
