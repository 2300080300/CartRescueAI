from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas import CartPredictionRequest, CartPredictionResponse
from ..services.ml_model import train_sample_model, predict_abandonment, recommendation_for_probability
from ..crud import create_cart_event
from ..database import get_db

router = APIRouter()
model = train_sample_model()


@router.post("/predict", response_model=CartPredictionResponse)
def predict(request: CartPredictionRequest, db: Session = Depends(get_db)):
    payload = request.dict()
    try:
        score = predict_abandonment(model, payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    create_cart_event(db, {
        "user_id": "anonymous",
        "session_duration": payload["session_duration"],
        "items_in_cart": payload["items_in_cart"],
        "total_value": payload["total_value"],
        "device_type": payload["device_type"],
        "source": payload["source"],
    })

    return {
        "abandonment_probability": score,
        "recommendation": recommendation_for_probability(score),
    }
