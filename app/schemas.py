from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    name: str
    email: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    created_at: datetime


class ActivityOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    category: str
    default_duration_min: int
    est_cost: float


class ItineraryItemCreate(BaseModel):
    activity_id: Optional[int] = None
    custom_name: Optional[str] = None
    start_time: Optional[datetime] = None
    duration_min: int = 60
    order_index: int = 0
    notes: Optional[str] = None


class ItineraryItemUpdate(BaseModel):
    activity_id: Optional[int] = None
    custom_name: Optional[str] = None
    start_time: Optional[datetime] = None
    duration_min: Optional[int] = None
    order_index: Optional[int] = None
    notes: Optional[str] = None


class ItineraryItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    activity_id: Optional[int]
    custom_name: Optional[str]
    start_time: Optional[datetime]
    duration_min: int
    order_index: int
    notes: Optional[str]


class DateCreate(BaseModel):
    user_id: int
    title: str
    scheduled_at: Optional[datetime] = None
    mood: Optional[str] = None
    budget: Optional[float] = None
    notes: Optional[str] = None


class DateUpdate(BaseModel):
    title: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    mood: Optional[str] = None
    budget: Optional[float] = None
    notes: Optional[str] = None


class DateOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    title: str
    scheduled_at: Optional[datetime]
    mood: Optional[str]
    budget: Optional[float]
    notes: Optional[str]
    created_at: datetime
    items: List[ItineraryItemOut] = []
