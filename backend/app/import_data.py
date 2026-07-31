import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import SessionLocal
from app.models.product import Product

df = pd.read_csv("ecommerce_dataset_updated.csv")

db: Session = SessionLocal()

# Clear old data to avoid duplicates
db.query(Product).delete()
db.commit()

for _, row in df.iterrows():

    # Read the date from CSV
    date = str(row["Purchase_Date"]).strip()

    # Convert all dates to YYYY-MM-DD
    try:
      purchase_date = datetime.strptime(
        date, "%Y-%m-%d"
        ).date()
    except ValueError:
        purchase_date = datetime.strptime(
            date, "%d-%m-%Y"
        ).date()

    # Create Product object
    product = Product(
        product_id=str(row["Product_ID"]),
        category=row["Category"],
        original_price=float(row["Price (Rs.)"]),
        discount=float(row["Discount (%)"]),
        final_price=float(row["Final_Price(Rs.)"]),
        payment_method=row["Payment_Method"],
        purchase_date=purchase_date
    )

    db.add(product)

db.commit()
db.close()

print("✅ Dataset Imported Successfully!")