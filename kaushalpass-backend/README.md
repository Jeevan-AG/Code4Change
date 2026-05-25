# KaushalPass Backend — Person 1

Foundation + Sarvam voice pipeline + GLM 5.1 NSQF assessment.

## Prerequisites

- Python 3.12
- Supabase project (run migrations in `migrations/`)
- Redis (Upstash recommended)
- [Sarvam API key](https://dashboard.sarvam.ai)
- [NVIDIA API key](https://build.nvidia.com) for GLM 5.1 NIM

## Setup

```bash
cd kaushalpass-backend
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your keys
```

### Supabase migrations

Run in order in Supabase SQL Editor:

1. `migrations/001_initial_schema.sql`
2. `migrations/002_rls_policies.sql`
3. `migrations/003_indexes.sql`

Create Storage bucket: `tts-audio` (private; signed URLs used).

### Run locally

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Person 1 endpoints

| Method | Path | Auth |
|--------|------|------|
| GET | `/health` | No |
| POST | `/api/v1/voice/assess` | Bearer JWT |

### Voice assess (multipart)

- `audio`: WebM/WAV file (max ~60s)
- `language_code`: `hi-IN` \| `ta-IN` \| `te-IN` \| `kn-IN` \| `bn-IN` \| `en-IN`

SSE events: text chunks → `data: [DONE]:{json}` → `data: [TTS]:{signed_url}`

## Quality checks

```bash
ruff check app/
mypy app/
```

## Handoff to Person 2

After migrations are applied, Person 2 adds:

- `auth/`, `passport/`, `documents/`, `certificate/`, `verifier/`, `verify/` routers
- Nemotron + certificate services

Register new routers in `app/api/v1/router.py`.
