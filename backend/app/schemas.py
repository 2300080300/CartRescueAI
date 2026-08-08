from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class CartPredictionRequest(BaseModel):
    session_duration: float = Field(..., gt=0, description="Session duration in minutes")
    items_in_cart: int = Field(..., ge=0, description="Number of items in cart")
    total_value: float = Field(..., ge=0, description="Cart total value")
    device_type: str = Field(..., description="Device type, e.g., desktop or mobile")
    source: str = Field(..., description="Traffic source, e.g., email or organic")


class CartPredictionResponse(BaseModel):
    abandonment_probability: float = Field(..., ge=0.0, le=1.0)
    recommendation: str


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    rating: float
    reviews: str
    category: str
    image: str

    model_config = ConfigDict(from_attributes=True)


class SessionCreate(CartPredictionRequest):
    pass


class PredictionResponse(BaseModel):
    id: int
    session_id: int
    prediction_score: float
    risk_level: str
    recommendation: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class SessionResponse(BaseModel):
    id: int
    session_duration: float
    items: int
    cart_value: float
    device: str
    traffic_source: str
    timestamp: datetime
    prediction: PredictionResponse

    model_config = ConfigDict(from_attributes=True)
