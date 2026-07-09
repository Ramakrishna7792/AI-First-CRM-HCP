# AI-First CRM for Healthcare Professionals

A full-stack CRM where medical representatives record doctor interactions with either a conventional form or an AI conversation. The assistant produces a structured, editable draft; only the representative can confirm and save it.

## Stack

- React, Redux Toolkit, React Router, Material UI, Axios
- FastAPI, Pydantic, SQLAlchemy, PostgreSQL
- LangGraph, Groq API, `gemma2-9b-it`

## Architecture

```text
React UI
  -> Redux Toolkit
    -> Axios
      -> FastAPI routes
        -> application services
          -> LangGraph -> Groq
          -> repositories -> SQLAlchemy -> PostgreSQL
```

React never receives the Groq key and never calls Groq. LangGraph cannot execute SQL. Persistence is available only through repositories and application services.

The backend follows clean architecture:

- `domain`: database entities and enterprise concepts
- `schemas`: validated transport and AI draft contracts
- `repositories`: persistence adapters
- `services`: application use cases and transaction boundaries
- `ai`: LangGraph state, prompts, extraction, and validation
- `api`: authenticated HTTP delivery
- `core` and `db`: cross-cutting infrastructure

## Project layout

```text
.
|-- backend/
|   |-- app/
|   |   |-- ai/
|   |   |-- api/v1/routes/
|   |   |-- core/
|   |   |-- db/
|   |   |-- domain/
|   |   |-- repositories/
|   |   |-- schemas/
|   |   `-- services/
|   |-- tests/
|   |-- .env.example
|   |-- Dockerfile
|   `-- requirements.txt
|-- frontend/
|   |-- src/
|   |   |-- components/
|   |   |-- hooks/
|   |   |-- pages/
|   |   |-- services/
|   |   `-- store/
|   |-- .env.example
|   |-- Dockerfile
|   `-- package.json
|-- docker-compose.yml
|-- package.json
`-- requirements.txt
```

## Run with Docker

1. Copy `backend/.env.example` to `backend/.env`.
2. Set `SECRET_KEY` and optionally `GROQ_API_KEY`.
3. Run:

```bash
docker compose up --build
```

Open `http://localhost:5173`. API documentation is at `http://localhost:8000/docs`.

## Run locally

Backend:

```bash
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
cd backend
uvicorn app.main:app --reload
```

The default local database is SQLite so the app starts without infrastructure. To use PostgreSQL, set `DATABASE_URL` from `backend/.env.example`.

Frontend:

```bash
npm install
npm run dev
```

## AI chat flow

1. FastAPI authenticates the representative and checks chat-session ownership.
2. LangGraph extracts only the allowed interaction fields.
3. Pydantic rejects invalid structured output.
4. The backend stores the conversation and returns a form draft.
5. Redux merges the draft into the shared form.
6. The representative reviews and explicitly submits it.
7. The normal interaction service resolves the doctor and saves the record.

Without `GROQ_API_KEY`, a small deterministic extractor is used for local development. It is deliberately limited and returns a visible warning.

## Security notes

- Replace the development secret before deployment.
- Use TLS and a managed secret store in production.
- Access tokens are short-lived; production deployments should add refresh-token rotation.
- Chat content may contain sensitive data. Apply an approved retention policy and redact application logs.
- Database creation on startup is convenient for development. Production should disable it and use versioned migrations.

## Verification

```bash
cd backend
pytest

cd ../frontend
npm run build
```
