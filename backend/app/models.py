from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base


class CartEvent(Base):
    __tablename__ = "cart_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(128), nullable=False)
    session_duration = Column(Float, nullable=False)
    items_in_cart = Column(Integer, nullable=False)
    total_value = Column(Float, nullable=False)
    device_type = Column(String(64), nullable=False)
    source = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
