from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/activities", tags=["activities"])


@router.get("", response_model=List[schemas.ActivityOut])
def list_activities(db: Session = Depends(get_db)):
    return (
        db.query(models.Activity)
        .order_by(models.Activity.category, models.Activity.name)
        .all()
    )
