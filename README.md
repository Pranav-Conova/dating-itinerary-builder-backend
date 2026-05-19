# Dating Itinerary Builder — Backend

FastAPI backend for building dating itineraries. Companion to [dating-itinerary-builder-frontend](https://github.com/Pranav-Conova/dating-itinerary-builder-frontend).

## Stack
- Python 3.12
- FastAPI
- SQLAlchemy 2.x
- Pydantic v2
- **SQLite** locally / **Postgres** on Render (selected automatically via `DATABASE_URL`)

## Local dev

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

With no `DATABASE_URL` set, the app uses SQLite at `data/app.db` (the directory is auto-created). Interactive API docs: http://localhost:8000/docs

## Docker

```bash
docker build -t dib-backend .
docker run -p 8000:8000 -v $(pwd)/data:/app/data dib-backend
```

## Deploy on Render (free tier)

The included `render.yaml` provisions both a free **Postgres** instance and a free **Web Service** in one click:

1. Push to GitHub (done if you're reading this).
2. Render dashboard → **New** → **Blueprint** → pick this repo.
3. Render reads `render.yaml`, shows the proposed Postgres + Web Service, click **Apply**.
4. After ~3 min, your API is live at `https://<service>.onrender.com`. Confirm with `<url>/health` and `<url>/docs`.

The Web Service receives the Postgres URL via the `DATABASE_URL` env var (auto-wired by `fromDatabase` in `render.yaml`), and `app/database.py` picks it up at startup.

### Free tier caveats
- **Postgres**: Render's free Postgres expires after **90 days**. After that you must upgrade (~$7/mo) or migrate your data, or your DB is suspended.
- **Web service**: spins down after 15 min of inactivity. First request after a sleep cold-starts in ~30s.
- **CORS**: the default `render.yaml` sets `CORS_ORIGINS=*`. Once your frontend is up, tighten this to your exact frontend URL in the Render dashboard.

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
