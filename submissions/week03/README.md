# Week 3 Submission — Individual Readiness Lab

## Student information

- Name: ZHUANG QI
- Student ID: 21312937
- Repository: https://github.com/Vinegar-repression/maie6000c-lab
- Checkpoint tag: `w03-readiness`
- Commit SHA: run `git rev-parse w03-readiness^{commit}` (tag `w03-readiness`)

## 1. What I changed

Added an optional `source` field to the `Case` model end-to-end. The field records where a case originated (for example: `"email"`, `"web-form"`, `"chat"`).

The change is intentionally small and bounded:
- Schema accepts an optional `source` string on case creation and returns it on read.
- Database model stores `source` as a nullable `String(100)` column.
- API persists the value when a case is created and returns it in responses.
- Alembic migration adds the column safely to existing tables.
- Integration tests verify both omitted and provided `source` values.
- Dockerfile was updated to include dev dependencies and the `tests/` directory so tests can run inside the container.

## 2. Files touched

- `Dockerfile` — install package with `[dev]` extras and copy `tests/` into the image
- `services/common/models.py` — add `source` column to `Case`
- `services/common/schemas.py` — add `source` to `CaseCreate` and `CaseRead`
- `services/api/app/main.py` — persist `source` when creating a case
- `alembic/versions/20260922_0002_add_source_to_cases.py` — new migration
- `tests/integration/test_api_case_flow.py` — new test for `source` field
- `docs/operations.md` — document local and container-based test commands
- `submissions/week03/README.md` — this file

## 3. How I verified it

- Built the API image and ran the unit and integration tests inside the container:
  ```bash
  docker compose build api
  docker compose run --rm --no-deps api pytest -q tests/unit tests/integration
  ```
  Expected: all tests pass.
- Started the full stack and confirmed migration applied:
  ```bash
  docker compose up -d --build
  docker compose exec db psql -U postgres -d maie6000c -c "\d cases"
  ```
  Expected: `source` column visible.
- Used Swagger / curl to create a case with `"source": "email"` and checked that `GET /cases` and `GET /cases/{id}` return the source value.
- Checked worker logs to confirm the case was still triaged normally after the schema change.

## 4. Known limitations or notes

- `source` is optional and nullable, so existing cases and clients that do not send it continue to work.
- No validation is applied beyond a 100-character maximum length and optional presence.
- The `Case` worker process passes only `title` and `description` to the AI service; `source` is not used for triage in this minimal change.

## 5. AI Use Statement

I used a generative AI assistant (Coze Agent with Kimi / DeepSeek models) to help implement this Week 3 readiness lab. I first decided to add an optional `source` field to the `Case` model as my bounded change, because it is small, end-to-end verifiable, and does not break existing functionality. The AI then helped me:

- Draft the schema, model, API, Alembic migration, and integration tests
- Debug environment issues (Docker Hub connectivity and local PostgreSQL port conflict)
- Write the initial version of this README

I reviewed every file, adjusted the implementation details where needed, and verified everything before committing. Specifically, I:
- Confirmed the migration applies cleanly to PostgreSQL
- Ran the test suite and confirmed all tests pass
- Tested the full `POST /cases` → worker triage → `GET /cases/{id}` flow via Swagger/curl
- Manually updated my student name and ID in this README on GitHub
