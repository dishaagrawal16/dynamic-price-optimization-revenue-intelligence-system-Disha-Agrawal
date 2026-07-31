from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    original_price = Column(Float, nullable=False)
    discount = Column(Float, nullable=False)
    final_price = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=False)
    purchase_date = Column(Date, nullable=False)