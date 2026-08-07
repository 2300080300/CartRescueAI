from pydantic import BaseModel, Field


class CartPredictionRequest(BaseModel):
    session_duration: float = Field(..., gt=0, description="Session duration in minutes")
    items_in_cart: int = Field(..., ge=0, description="Number of items in cart")
    total_value: float = Field(..., ge=0, description="Cart total value")
    device_type: str = Field(..., description="Device type, e.g., desktop or mobile")
    source: str = Field(..., description="Traffic source, e.g., email or organic")


class CartPredictionResponse(BaseModel):
    abandonment_probability: float = Field(..., ge=0.0, le=1.0)
    recommendation: str
