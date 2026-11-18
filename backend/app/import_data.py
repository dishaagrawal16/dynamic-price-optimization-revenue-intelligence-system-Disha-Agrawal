"""
Load data/ecommerce_dataset_updated.csv into the products table.

Run from the backend folder:
    python -m app.import_data
"""
from datetime import datetime
from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.models import Product, User  # noqa: F401 (registers tables)

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "ecommerce_dataset_updated.csv"


def parse_date(value):
    # Convert all dates to YYYY-MM-DD
    value = str(value).strip()
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return datetime.strptime(value, "%d-%m-%Y").date()


Base.metadata.create_all(bind=engine)

df = pd.read_csv(CSV_PATH)

db: Session = SessionLocal()

try:
    # Clear old data to avoid duplicates
    db.query(Product).delete()
    db.commit()

    products = [
        Product(
            product_id=str(row["Product_ID"]),
            category=row["Category"],
            original_price=float(row["Price (Rs.)"]),
            discount=float(row["Discount (%)"]),
            final_price=float(row["Final_Price(Rs.)"]),
            payment_method=row["Payment_Method"],
            purchase_date=parse_date(row["Purchase_Date"]),
        )
        for _, row in df.iterrows()
    ]

    # Insert in batches (much faster over the internet to TiDB Cloud)
    batch_size = 500
    for i in range(0, len(products), batch_size):
        db.bulk_save_objects(products[i:i + batch_size])
        db.commit()
        print(f"  inserted {min(i + batch_size, len(products))}/{len(products)}")

    print(f"✅ Dataset Imported Successfully! ({len(products)} rows)")
finally:
    db.close()
