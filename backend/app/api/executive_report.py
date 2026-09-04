from fastapi import APIRouter, HTTPException
import pandas as pd
import os


router = APIRouter(
    prefix="/executive-report",
    tags=["Executive Business Intelligence"]
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

REPORT_FILE = os.path.join(
    DATA_DIR,
    "executive_business_report.csv"
)


# ============================================================
# HELPER
# ============================================================

def load_report():

    if not os.path.exists(REPORT_FILE):

        raise HTTPException(
            status_code=404,
            detail=(
                "Executive business report not found. "
                "Run executive_report.py first."
            )
        )

    df = pd.read_csv(
        REPORT_FILE
    )

    # Clean formatting issue from market intelligence
    if "Market_Position" in df.columns:

        df["Market_Position"] = (
            df["Market_Position"]
            .astype(str)
            .str.replace(
                "BelowCompetitor",
                "Below Competitor",
                regex=False
            )
        )

    # Convert NaN to None
    df = df.astype(object).where(
        pd.notna(df),
        None
    )

    return df


# ============================================================
# 1. EXECUTIVE SUMMARY
# ============================================================

@router.get("/summary")
def executive_summary():

    try:

        df = load_report()

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

        high_priority = int(
            (
                df["Priority"] == "High"
            ).sum()
        )

        data_required = int(
            df[
                "Executive_Status"
            ].isin(
                [
                    "Data Required",
                    "Data Validation Required"
                ]
            ).sum()
        )

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
                most_profitable,

            "high_priority_actions":
                high_priority,

            "categories_requiring_better_data":
                data_required
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# 2. CATEGORY EXECUTIVE ANALYSIS
# ============================================================

@router.get("/category-analysis")
def executive_category_analysis():

    try:

        df = load_report()

        return df.to_dict(
            orient="records"
        )

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )