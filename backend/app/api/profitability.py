from fastapi import APIRouter, HTTPException
import pandas as pd
import os


router = APIRouter(
    prefix="/profitability",
    tags=["Profitability Analytics"]
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

PROFITABILITY_FILE = os.path.join(
    DATA_DIR,
    "profitability_analysis.csv"
)


# ============================================================
# 1. PROFITABILITY SUMMARY
# ============================================================

@router.get("/summary")
def profitability_summary():

    try:

        df = pd.read_csv(
            PROFITABILITY_FILE
        )

        total_revenue = df[
            "Total_Revenue"
        ].sum()

        estimated_cost = df[
            "Estimated_Cost"
        ].sum()

        estimated_profit = df[
            "Estimated_Profit"
        ].sum()

        profit_margin = (
            estimated_profit
            / total_revenue
            * 100
        )

        most_profitable = df.loc[
            df["Estimated_Profit"].idxmax(),
            "Category_Name"
        ]

        return {
            "total_revenue": round(
                total_revenue,
                2
            ),

            "estimated_cost": round(
                estimated_cost,
                2
            ),

            "estimated_profit": round(
                estimated_profit,
                2
            ),

            "estimated_profit_margin": round(
                profit_margin,
                2
            ),

            "most_profitable_category":
                most_profitable
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# 2. CATEGORY-WISE PROFITABILITY
# ============================================================

@router.get("/category-analysis")
def category_profitability():

    try:

        df = pd.read_csv(
            PROFITABILITY_FILE
        )

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