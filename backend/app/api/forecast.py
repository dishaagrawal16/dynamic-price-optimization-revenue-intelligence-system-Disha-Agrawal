import os
import pandas as pd
from fastapi import APIRouter

router = APIRouter(
    prefix="/forecast",
    tags=["Demand Forecasting"]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

forecast_path = os.path.join(
    BASE_DIR,
    "..",
    "..",
    "data",
    "demand_forecasts_v2.csv"
)


@router.get("/demand")
def get_demand_forecast():

    df = pd.read_csv(forecast_path)

    df["Date"] = pd.to_datetime(
        df["Date"]
    ).dt.strftime("%Y-%m-%d")

    short_term = df[
        df["Horizon"] == "Short Term"
    ].to_dict(orient="records")

    medium_term = df[
        df["Horizon"] == "Medium Term"
    ].to_dict(orient="records")

    long_term = df[
        df["Horizon"] == "Long Term"
    ].to_dict(orient="records")

    return {
        "trend": df["Trend"].iloc[0],

        "reliability_score": float(
            df["Reliability_Score"].iloc[0]
        ),

        "short_term": short_term,

        "medium_term": medium_term,

        "long_term": long_term
    }