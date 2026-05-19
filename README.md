# Dating Itinerary Builder — Backend

FastAPI + SQLite backend for building dating itineraries. Companion to [dating-itinerary-builder-frontend](https://github.com/Pranav-Conova/dating-itinerary-builder-frontend).

## Stack
- Python 3.12
- FastAPI
- SQLAlchemy 2.x + SQLite
- Pydantic v2

## Local dev

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Interactive API docs: http://localhost:8000/docs

## Docker

```bash
docker build -t dib-backend .
docker run -p 8000:8000 -v $(pwd)/data:/app/data dib-backend
```

The SQLite file lives at `data/app.db` (volume-mounted, so it survives container restarts).

## Deploy on Render

1. Connect this repo as a **Web Service**.
2. Render auto-detects `render.yaml`.
3. **SQLite + Render caveat**: Render's free filesystem is ephemeral — data is wiped on each deploy. The included `render.yaml` mounts a 1 GB persistent disk (Starter plan) at `/app/data` to keep your SQLite file safe. If you'd rather use the free tier, swap SQLite for Render's free managed Postgres:
   - Provision a Postgres instance on Render.
   - Set the env var `DATABASE_URL` to the Render-provided connection string.
   - Add `psycopg2-binary` to `requirements.txt`.
   - `app/database.py` already reads `DATABASE_URL` and adapts.

## Data model

```
users           id, name, email, created_at
dates           id, user_id (FK), title, scheduled_at, mood, budget, notes, created_at
activities      id, name, category, default_duration_min, est_cost     (seeded catalog)
itinerary_items id, date_id (FK), activity_id (FK, nullable),
                custom_name, start_time, duration_min, order_index, notes
```

- One **user** → many **dates**
- One **date** → many ordered **itinerary_items**
- Each item either links to a catalog **activity** or has a custom name

## API endpoints

| Method | Path                           | Description                              |
|--------|--------------------------------|------------------------------------------|
| GET    | `/health`                      | Health check                             |
| POST   | `/users`                       | Create user (idempotent on email)        |
| GET    | `/users/{user_id}`             | Get user                                 |
| GET    | `/activities`                  | List activity catalog                    |
| POST   | `/dates`                       | Create a date                            |
| GET    | `/dates?user_id=…`             | List a user's dates                      |
| GET    | `/dates/{date_id}`             | Get a date + ordered items               |
| PUT    | `/dates/{date_id}`             | Update a date                            |
| DELETE | `/dates/{date_id}`             | Delete a date                            |
| POST   | `/dates/{date_id}/items`       | Add an itinerary item                    |
| PUT    | `/items/{item_id}`             | Update an item                           |
| DELETE | `/items/{item_id}`             | Delete an item                           |
