from pydantic import BaseModel

class ProductCreate(BaseModel):
    product_id: str
    category: str
    original_price: float
    discount: float
    final_price: float
    payment_method: str
    purchase_date: str