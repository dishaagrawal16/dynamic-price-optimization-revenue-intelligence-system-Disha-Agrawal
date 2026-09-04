from fastapi import APIRouter, HTTPException
import pandas as pd
import os


router = APIRouter(
    prefix="/pricing-strategy",
    tags=["Pricing Strategy"]
)


# ============================================================
# PATH
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

RECOMMENDATION_FILE = os.path.join(
    DATA_DIR,
    "pricing_strategy_recommendations.csv"
)


# ============================================================
# PRICING STRATEGY RECOMMENDATIONS
# ============================================================

@router.get("/recommendations")
def get_pricing_recommendations():

    try:

        df = pd.read_csv(
            RECOMMENDATION_FILE
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