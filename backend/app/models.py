from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
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


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Float, nullable=False)
    reviews = Column(String(32), nullable=False)
    category = Column(String(100), nullable=False)
    image = Column(String(500), nullable=False)


class CustomerSession(Base):
    __tablename__ = "customer_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_duration = Column(Float, nullable=False)
    items = Column(Integer, nullable=False)
    cart_value = Column(Float, nullable=False)
    device = Column(String(64), nullable=False)
    traffic_source = Column(String(500), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    prediction = relationship("Prediction", back_populates="session", uselist=False)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("customer_sessions.id"), nullable=False, index=True)
    prediction_score = Column(Float, nullable=False)
    risk_level = Column(String(16), nullable=False)
    recommendation = Column(String(500), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    session = relationship("CustomerSession", back_populates="prediction")
