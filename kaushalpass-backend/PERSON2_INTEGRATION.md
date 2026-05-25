# Person 2 — Integration (for Person 1)

This folder contains **only Person 2** code under `app/`. There is no `app/main.py` — you own the FastAPI app bootstrap.

## Mount routers in your `app/main.py`

```python
from app.api.v1.auth.router import router as auth_router
from app.api.v1.passport.router import router as passport_router
from app.api.v1.documents.router import router as documents_router
from app.api.v1.certificate.router import router as certificate_router
from app.api.v1.verifier.router import router as verifier_router
from app.api.v1.verify.router import router as verify_router

app.include_router(auth_router, prefix="/api/v1")
app.include_router(passport_router, prefix="/api/v1")
app.include_router(documents_router, prefix="/api/v1")
app.include_router(certificate_router, prefix="/api/v1")
app.include_router(verifier_router, prefix="/api/v1")
app.include_router(verify_router, prefix="/api/v1")
```

## Person 2 pip dependencies

Merge `requirements-person2.txt` into your project `requirements.txt` (do not duplicate versions blindly).

## Environment variables

| Variable | Who sets it |
|----------|-------------|
| `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_JWT_SECRET` | **Person 1 / team** (shared project `.env`) |
| `NVIDIA_API_KEY`, `APP_URL` | **Person 2** — see `.env.example` |

Person 2 services call Supabase for DB + storage, but **provisioning the Supabase project and migrations** is a team/Person 1 concern. Use the same values in one root `.env` when the app runs.

## Database

Apply `supabase/migrations/20250526000001_person2_core_schema.sql` or merge into your migration set.

## Auth helper

Protected routes use `CurrentUserId` from `app.api.v1.auth.router` (JWT via `SUPABASE_JWT_SECRET`).
