from pydantic import BaseModel
from datetime import datetime
class PricePredictionRequest(BaseModel):
    category: int
    original_price: float
    discount: float
    payment_method: int
    year: int
    month: int
    day: int
