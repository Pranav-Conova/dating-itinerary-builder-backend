from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(tags=["dates"])


@router.post("/dates", response_model=schemas.DateOut)
def create_date(payload: schemas.DateCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_date = models.Date(**payload.model_dump())
    db.add(new_date)
    db.commit()
    db.refresh(new_date)
    return new_date


@router.get("/dates", response_model=List[schemas.DateOut])
def list_dates(user_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Date)
        .filter(models.Date.user_id == user_id)
        .order_by(models.Date.scheduled_at.desc().nullslast())
        .all()
    )


@router.get("/dates/{date_id}", response_model=schemas.DateOut)
def get_date(date_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Date).filter(models.Date.id == date_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Date not found")
    return obj


@router.put("/dates/{date_id}", response_model=schemas.DateOut)
def update_date(date_id: int, payload: schemas.DateUpdate, db: Session = Depends(get_db)):
    obj = db.query(models.Date).filter(models.Date.id == date_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Date not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/dates/{date_id}", status_code=204)
def delete_date(date_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Date).filter(models.Date.id == date_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Date not found")
    db.delete(obj)
    db.commit()


@router.post("/dates/{date_id}/items", response_model=schemas.ItineraryItemOut)
def add_item(date_id: int, payload: schemas.ItineraryItemCreate, db: Session = Depends(get_db)):
    date_obj = db.query(models.Date).filter(models.Date.id == date_id).first()
    if not date_obj:
        raise HTTPException(status_code=404, detail="Date not found")
    if not payload.activity_id and not payload.custom_name:
        raise HTTPException(status_code=400, detail="Provide either activity_id or custom_name")
    item = models.ItineraryItem(date_id=date_id, **payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/items/{item_id}", response_model=schemas.ItineraryItemOut)
def update_item(item_id: int, payload: schemas.ItineraryItemUpdate, db: Session = Depends(get_db)):
    item = db.query(models.ItineraryItem).filter(models.ItineraryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.ItineraryItem).filter(models.ItineraryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
