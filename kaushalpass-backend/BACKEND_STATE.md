# Backend State — Person 2 only

## Scope

Only files under `app/` listed in the Person 2 task spec (+ migration + integration doc).

**Removed to avoid merge conflicts:** `app/main.py`, `app/config.py`, `app/dependencies.py`, `app/exceptions.py`, `app/db/client.py`, `Dockerfile`, `tests/`, `GET /health`.

## Person 1 action

See [PERSON2_INTEGRATION.md](PERSON2_INTEGRATION.md) to mount routers and merge requirements.

## Blockers

- Shared Supabase migration with Person 1
- Storage buckets: `documents`, `certificates`
