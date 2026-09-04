from fastapi import APIRouter, HTTPException
import pandas as pd
import os


router = APIRouter(
    prefix="/competitor",
    tags=["Competitor Analysis"]
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

COMPETITOR_FILE = os.path.join(
    DATA_DIR,
    "competitor_prices_final.csv"
)

COMPARISON_FILE = os.path.join(
    DATA_DIR,
    "pricing_comparison.csv"
)

MARKET_INTELLIGENCE_FILE = os.path.join(
    DATA_DIR,
    "market_intelligence.csv"
)


# ============================================================
# 1. COMPETITOR SUMMARY
# ============================================================

@router.get("/summary")
def competitor_summary():

    try:

        df = pd.read_csv(
            COMPETITOR_FILE
        )

        total_products = len(df)

        competitors = df[
            "Competitor"
        ].nunique()

        categories = df[
            "Category"
        ].nunique()

        average_price = round(
            df[
                "Competitor_Price"
            ].mean(),
            2
        )

        return {
            "total_products": total_products,
            "competitors_monitored": competitors,
            "categories_covered": categories,
            "average_competitor_price": average_price
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# 2. PRICE COMPARISON
# ============================================================
@router.get("/comparison")
def competitor_comparison():

    try:

        df = pd.read_csv(
            COMPARISON_FILE
        )

        # Replace infinite values with NaN first
        df = df.replace(
            [float("inf"), float("-inf")],
            pd.NA
        )

        # Convert to object so NaN can actually become None
        df = df.astype(object).where(
            pd.notna(df),
            None
        )

        return df.to_dict(
            orient="records"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ============================================================
# 3. COMPETITOR PRODUCTS
# ============================================================

@router.get("/products")
def get_competitor_products():
    import os
    import pandas as pd

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    csv_path = os.path.join(
        BASE_DIR,
        "..",
        "..",
        "data",
        "competitor_prices_final.csv"
    )

    df = pd.read_csv(csv_path)

    # Replace NaN / infinite values with None
    df = df.astype(object).where(pd.notna(df), None)

    return df.to_dict(orient="records")


# ============================================================
# 4. CATEGORY-WISE COMPETITOR PRICES
# ============================================================
# ============================================================
# 4. CATEGORY-WISE COMPETITOR PRICES
# ============================================================

@router.get("/category-prices")
def category_prices():

    try:

        df = pd.read_csv(
            COMPETITOR_FILE
        )

        # Make sure numeric columns are numeric
        df["Competitor_Price"] = pd.to_numeric(
            df["Competitor_Price"],
            errors="coerce"
        )

        df["MRP"] = pd.to_numeric(
            df["MRP"],
            errors="coerce"
        )

        # Calculate discount percentage
        df["Discount_Percent"] = (
            (
                df["MRP"] - df["Competitor_Price"]
            )
            / df["MRP"]
        ) * 100

        result = (
            df.groupby(
                [
                    "Category",
                    "Competitor"
                ]
            )
            .agg(
                Product_Count=(
                    "Competitor_Price",
                    "count"
                ),
                Average_Price=(
                    "Competitor_Price",
                    "mean"
                ),
                Minimum_Price=(
                    "Competitor_Price",
                    "min"
                ),
                Maximum_Price=(
                    "Competitor_Price",
                    "max"
                ),
                Average_Discount=(
                    "Discount_Percent",
                    "mean"
                )
            )
            .reset_index()
        )

        # Round values
        result["Average_Price"] = (
            result["Average_Price"]
            .round(2)
        )

        result["Minimum_Price"] = (
            result["Minimum_Price"]
            .round(2)
        )

        result["Maximum_Price"] = (
            result["Maximum_Price"]
            .round(2)
        )

        result["Average_Discount"] = (
            result["Average_Discount"]
            .round(2)
        )

        return result.to_dict(
            orient="records"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ============================================================
# 5. MARKET INTELLIGENCE
# ============================================================

@router.get("/market-intelligence")
def get_market_intelligence():

    try:

        df = pd.read_csv(
            MARKET_INTELLIGENCE_FILE
        )

        # Replace NaN with None
        df = df.astype(object).where(
            pd.notna(df),
            None
        )

        return df.to_dict(
            orient="records"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )    