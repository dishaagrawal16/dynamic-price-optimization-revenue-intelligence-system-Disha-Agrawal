from fastapi import APIRouter
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.product import Product
from app.models.user import User
from app.security import get_current_user
router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/summary")
def dashboard_summary(
    db: Session = Depends(get_db)
):
    

    total_products = db.query(Product).count()

    total_revenue = db.query(
        func.sum(Product.final_price)
    ).scalar()

    total_discount = db.query(
        func.sum(Product.discount)
    ).scalar()

    average_price = db.query(
        func.avg(Product.final_price)
    ).scalar()

    

    return {
        "total_products": total_products,
        "total_revenue": total_revenue or 0,
        "total_discount": total_discount or 0,
        "average_price": round(average_price or 0, 2)
    }




@router.get("/monthly-revenue")
def get_monthly_revenue(
    db: Session = Depends(get_db),
):
    revenue = (
        db.query(
            func.month(Product.purchase_date).label("month"),
            func.sum(Product.final_price).label("revenue")
        )
        .group_by(func.month(Product.purchase_date))
        .order_by(func.month(Product.purchase_date))
        .all()
    )

    return [
        {
            "month": row.month,
            "revenue": float(row.revenue)
        }
        for row in revenue
    ]

@router.get("/category-revenue")
def get_category_revenue(
    db: Session = Depends(get_db)
):
    data = (
        db.query(
            Product.category,
            func.sum(Product.final_price).label("revenue")
        )
        .group_by(Product.category)
        .order_by(func.sum(Product.final_price).desc())
        .all()
    )

    return [
        {
            "category": row.category,
            "revenue": float(row.revenue)
        }
        for row in data
    ]

@router.get("/recent-products")
def get_recent_products(
    db: Session = Depends(get_db)
):
    products = (
        db.query(Product)
        .order_by(Product.id.desc())
        .limit(5)
        .all()
    )

    return [
        {
            "product_id": product.product_id,
            "category": product.category,
            "price": product.final_price,
            "payment_method": product.payment_method,
            "purchase_date": product.purchase_date
        }
        for product in products
    ]

@router.get("/payment-distribution")
def get_payment_distribution(
    db: Session = Depends(get_db)
):
    data = (
        db.query(
            Product.payment_method,
            func.count(Product.id).label("count")
        )
        .group_by(Product.payment_method)
        .all()
    )

    return [
        {
            "payment_method": row.payment_method,
            "count": row.count
        }
        for row in data
    ]