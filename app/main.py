import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from . import models  # noqa: F401
from .seed import seed_activities
from .routers import users, dates, activities

Base.metadata.create_all(bind=engine)
seed_activities()

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
