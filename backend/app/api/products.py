from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from app.security import get_current_user
from app.models.user import User
from app.database import SessionLocal
from app.models.product import Product
from app.schemas.product import ProductCreate

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# ---------------- GET ----------------
# ---------------- GET ----------------
@router.get("/")
def get_products(skip: int = 0, limit: int = 20,current_user: User = Depends(get_current_user)):
    db = SessionLocal()

    products = (
        db.query(Product)
        .offset(skip)
        .limit(limit)
        .all()
    )

    db.close()

    return products


# ---------------- POST ----------------
@router.post("/")
def create_product(
    
    
    product: ProductCreate,
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admins can add products."
        )
    
    db = SessionLocal()

    new_product = Product(
        product_id=product.product_id,
        category=product.category,
        original_price=product.original_price,
        discount=product.discount,
        final_price=product.final_price,
        payment_method=product.payment_method,
        purchase_date=product.purchase_date
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    db.close()

    return {
        "message": "Product Added Successfully",
        "product": new_product
    }


# ---------------- PUT ----------------
@router.put("/{id}")
def update_product(
    id: int,
    product: ProductCreate,
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
          status_code=403,
          detail="Only admins can update products."
        )
    db = SessionLocal()

    db_product = db.query(Product).filter(Product.id == id).first()

    if not db_product:
        db.close()
        raise HTTPException(status_code=404, detail="Product not found")

    db_product.product_id = product.product_id
    db_product.category = product.category
    db_product.original_price = product.original_price
    db_product.discount = product.discount
    db_product.final_price = product.final_price
    db_product.payment_method = product.payment_method
    db_product.purchase_date = product.purchase_date

    db.commit()
    db.refresh(db_product)
    db.close()

    return {
        "message": "Product Updated Successfully",
        "product": db_product
    }


# ---------------- DELETE ----------------
@router.delete("/{id}")
def delete_product(
    id: int,
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "admin":
        raise HTTPException(
          status_code=403,
          detail="Only admins can delete products."
    )
    db = SessionLocal()

    db_product = db.query(Product).filter(Product.id == id).first()

    if not db_product:
        db.close()
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
    db.close()

    return {
        "message": "Product Deleted Successfully"
    }