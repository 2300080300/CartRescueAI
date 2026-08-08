from sqlalchemy.orm import Session
from . import models


def create_cart_event(db: Session, event_data: dict) -> models.CartEvent:
    event = models.CartEvent(**event_data)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def create_customer_session(db: Session, session_data: dict) -> models.CustomerSession:
    customer_session = models.CustomerSession(**session_data)
    db.add(customer_session)
    db.flush()
    return customer_session


def create_prediction(db: Session, prediction_data: dict) -> models.Prediction:
    prediction = models.Prediction(**prediction_data)
    db.add(prediction)
    db.flush()
    return prediction


def commit_session_and_prediction(db: Session, session_data: dict, prediction_data: dict):
    try:
        customer_session = create_customer_session(db, session_data)
        prediction = create_prediction(db, {**prediction_data, "session_id": customer_session.id})
        db.commit()
        db.refresh(customer_session)
        db.refresh(prediction)
        return customer_session, prediction
    except Exception:
        db.rollback()
        raise


def list_products(db: Session):
    return db.query(models.Product).order_by(models.Product.id).all()


def seed_products(db: Session) -> None:
    if db.query(models.Product).count():
        return

    sample_products = [
        {"name": "Apple iPhone 16 Pro", "price": 129999, "rating": 4.9, "reviews": "2.4k", "category": "Smartphones", "image": "https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?auto=format&fit=crop&w=900&q=85"},
        {"name": "Sony WH-1000XM5", "price": 29999, "rating": 4.8, "reviews": "1.8k", "category": "Audio", "image": "https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?auto=format&fit=crop&w=900&q=85"},
        {"name": "Nike Air Max", "price": 7999, "rating": 4.7, "reviews": "3.1k", "category": "Footwear", "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=85"},
        {"name": "Samsung Galaxy Watch", "price": 24999, "rating": 4.6, "reviews": "980", "category": "Wearables", "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=85"},
        {"name": "Logitech Gaming Mouse", "price": 3999, "rating": 4.8, "reviews": "1.2k", "category": "Gaming", "image": "https://images.unsplash.com/photo-1527814050087-3793815479db?auto=format&fit=crop&w=900&q=85"},
    ]
    db.add_all(models.Product(**product) for product in sample_products)
    db.commit()


def list_predictions(db: Session):
    return db.query(models.Prediction).order_by(models.Prediction.timestamp.desc()).all()
