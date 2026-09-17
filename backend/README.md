# Mediscan Note FastAPI backend

## Local setup

1. Create `backend/.env` from `.env.example` and enter only your local PostgreSQL password.
2. Apply `app/db/migrations/001_auth.sql` to the local `mediscan_note` database.
3. Run `py -m uvicorn app.main:app --reload --port 3000` from `backend/`.
4. Run `py -m pytest -q` from `backend/`.

`ENABLE_DEV_AUTH_SHORTCUTS=true` is permitted only together with `ENVIRONMENT=development`. It exposes a development-only verification token in API responses and must never be enabled in production.

The test suite creates uniquely named `pytest-auth-...@example.local` accounts and removes only those accounts during cleanup.
## Rate-limit deployment note

The login rate limiter is stored in process memory. Running multiple workers makes each IP- and account-based limit effectively looser by the number of workers. Before a multi-worker deployment, move this state to shared storage such as Redis.
