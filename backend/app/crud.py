from sqlalchemy.orm import Session
from . import models


def create_cart_event(db: Session, event_data: dict) -> models.CartEvent:
    event = models.CartEvent(**event_data)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
