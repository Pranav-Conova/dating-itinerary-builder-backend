from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(200), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    dates = relationship("Date", back_populates="user", cascade="all, delete-orphan")


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    category = Column(String(60), nullable=False)
    default_duration_min = Column(Integer, default=60)
    est_cost = Column(Float, default=0.0)


class Date(Base):
    __tablename__ = "dates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(160), nullable=False)
    scheduled_at = Column(DateTime, nullable=True)
    mood = Column(String(60), nullable=True)
    budget = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="dates")
    items = relationship(
        "ItineraryItem",
        back_populates="date",
        cascade="all, delete-orphan",
        order_by="ItineraryItem.order_index",
    )


class ItineraryItem(Base):
    __tablename__ = "itinerary_items"

    id = Column(Integer, primary_key=True, index=True)
    date_id = Column(Integer, ForeignKey("dates.id", ondelete="CASCADE"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=True)
    custom_name = Column(String(160), nullable=True)
    start_time = Column(DateTime, nullable=True)
    duration_min = Column(Integer, default=60)
    order_index = Column(Integer, default=0)
    notes = Column(Text, nullable=True)

    date = relationship("Date", back_populates="items")
    activity = relationship("Activity")
