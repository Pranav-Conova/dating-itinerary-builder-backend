import os
import time
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError
from .database import Base, engine
from . import models  # noqa: F401
from .seed import seed_activities
from .routers import users, dates, activities

logger = logging.getLogger("uvicorn.error")


def wait_for_db_and_init(max_attempts: int = 12, base_delay: float = 1.5) -> None:
    """Retry create_all so a freshly-provisioned DB has time to come up."""
    last_err: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            Base.metadata.create_all(bind=engine)
            seed_activities()
            logger.info("DB ready (attempt %d)", attempt)
            return
        except OperationalError as e:
            last_err = e
            delay = base_delay * attempt
            logger.warning(
                "DB not ready yet (attempt %d/%d): %s. retrying in %.1fs",
                attempt, max_attempts, e.__class__.__name__, delay,
            )
            time.sleep(delay)
    raise RuntimeError(f"DB still unreachable after {max_attempts} attempts") from last_err


wait_for_db_and_init()

app = FastAPI(title="Dating Itinerary Builder API", version="0.1.0")

cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(users.router)
app.include_router(activities.router)
app.include_router(dates.router)
