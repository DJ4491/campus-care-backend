Nice — let’s remove the fog. Below is a **compact, file-by-file ledger** for every recommendation-related file in your tree. Read it once and you’ll stop guessing where things go.

# At-a-glance flow

Route → Service (rec_engine) → CRUD → Supabase client → DB
(HTTP auth + schemas live at the top; tests sit to validate each layer)

---

## `app/routes/recommendations.py`

**Purpose:** HTTP endpoints for recommendation features.
**Allowed:**

* Endpoint definitions (`GET /people-you-may-know`, etc.)
* Dependency injection (auth, pagination)
* Call into `services.rec_engine` and `schemas` to validate input/output
* Return JSON responses / proper status codes
  **Not allowed:** business logic, DB queries, ranking.
  **Who calls it / imports it:** Mounted in `main.py` via `app.include_router`.
  **Return shape:** Pydantic models from `schemas/recommendations.py`.

---

## `app/services/rec_engine.py`

**Purpose:** The brain — all recommendation algorithms live here.
**Allowed:**

* Pure algorithmic logic: mutual-friends, scoring, filtering, ranking, combining signals, weighting rules, caching decisions.
* Calling CRUD helper functions to *fetch raw data*.
* Returning final candidate lists and scores (plain Python lists/dicts or dataclass/pydantic-ready structures).
  **Not allowed:** direct DB client creation, route handling, reading env or HTTP details.
  **Who calls it / imports it:** Called by `routes/recommendations.py`. Imports `crud/recommendations.py` functions.
  **Testing tip:** Unit-test this layer in isolation by mocking CRUD return values.

---

## `app/crud/recommendations.py`

**Purpose:** Raw data access for recommendation use-cases.
**Allowed:**

* SQL queries or supabase-js/python client calls that *only fetch raw rows* needed by rec_engine (e.g., followers list, follow-edges, interactions).
* SQL-heavy helpers (views, CTE wrappers) as long as they return raw structured data.
* Lightweight transformations that normalize DB rows to plain dicts.
  **Not allowed:** scoring, sorting by business rules, “if mutual_count > X then …” decisions.
  **Who calls it / imports it:** Called by `services/rec_engine.py`.
  **Important:** never run heavy queries at import time — wrap client calls inside functions. Keep functions small and well-documented (e.g., `get_follow_edges(user_id)`).

---

## `app/schemas/recommendations.py`

**Purpose:** Pydantic models for request/response shapes used by routes/services.
**Allowed:**

* Request body models, query param models, response models (result list item schema: `user_id`, `score`, `reason`, etc.)
* Serialization/validation only.
  **Not allowed:** algorithmic logic or DB calls.
  **Who uses it:** `routes/recommendations.py` for response typing, `services/rec_engine.py` for output conformity if desired.

---

## `app/services/supabase_service.py`

**Purpose:** Single place for Supabase client (service role) creation.
**Allowed:**

* Create and export `service_supabase` client.
* Small utility wrappers for common low-level client behavior.
  **Not allowed:** importing `crud` or `services.rec_engine` (to avoid circular imports).
  **How to use:** `crud/recommendations.py` imports this client and uses it inside functions.

---

## `app/tests/test_recommendations.py`

**Purpose:** Tests that validate both the raw queries and the algorithm.
**What to test:**

* `crud` functions return expected shapes for known DB fixtures (integration).
* `rec_engine` logic given mocked `crud` results (unit).
* End-to-end route behavior (optional integration tests with test DB or supabase emulator).

---

## Practical import & circular-import rules (short)

* CRUD imports `service_supabase` from `app.services.supabase_service`.
* Services import CRUD (NOT vice-versa).
* Routes import services and schemas (NOT services import routes).
* If you ever hit circular import, move the import inside the function (lazy import) as a last resort.

---

## Quick reference: what to edit for each task

* Add a DB query or index → `crud/recommendations.py`
* Change how candidates are scored or filtered → `services/rec_engine.py`
* Add response fields or validation → `schemas/recommendations.py`
* Expose a new endpoint → `routes/recommendations.py`
* Change client config or keys → `services/supabase_service.py` (but do not export keys to frontend)

---

If you want I can now:

* Produce a **one-page contract list** (function name, input, output) for the CRUD ↔ rec_engine boundary — no code, just exact signatures and return shapes to implement.
  Pick that and I’ll make it tiny and precise.
