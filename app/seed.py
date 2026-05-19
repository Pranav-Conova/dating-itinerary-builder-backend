from .database import SessionLocal
from .models import Activity

SEED_ACTIVITIES = [
    ("Dinner at a restaurant", "Food", 90, 1500),
    ("Coffee date", "Food", 60, 400),
    ("Movie", "Entertainment", 150, 600),
    ("Beach walk", "Outdoor", 60, 0),
    ("Bowling", "Activity", 90, 800),
    ("Karaoke", "Activity", 120, 1000),
    ("Art gallery / museum", "Culture", 90, 300),
    ("Picnic in park", "Outdoor", 120, 500),
    ("Live music / concert", "Entertainment", 180, 2000),
    ("Mini golf", "Activity", 60, 600),
    ("Cooking class together", "Activity", 120, 2500),
    ("Ice cream parlor", "Food", 30, 300),
]


def seed_activities():
    db = SessionLocal()
    try:
        if db.query(Activity).count() > 0:
            return
        for name, category, dur, cost in SEED_ACTIVITIES:
            db.add(Activity(name=name, category=category, default_duration_min=dur, est_cost=cost))
        db.commit()
    finally:
        db.close()
