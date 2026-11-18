import os
import pandas as pd
import numpy as np

# ==========================================
# PATHS
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

input_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "forecast_dataset_v2.csv"
)

output_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "demand_forecasts.csv"
)

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(input_path)

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date").reset_index(drop=True)

print("Historical Dataset Shape:", df.shape)

print(
    "Historical Date Range:",
    df["Date"].min(),
    "to",
    df["Date"].max()
)

# ==========================================
# HISTORICAL DEMAND
# ==========================================

historical_demand = df["Demand"]

# Use last 7 complete observations
recent_average = historical_demand.tail(7).mean()

print("\nLast 7-Day Average Demand:")
print(round(recent_average, 2))

# ==========================================
# TREND
# ==========================================

first_7_average = historical_demand.head(7).mean()

last_7_average = historical_demand.tail(7).mean()

if last_7_average > first_7_average * 1.05:
    trend = "Increasing"

elif last_7_average < first_7_average * 0.95:
    trend = "Decreasing"

else:
    trend = "Stable"

print("\nDemand Trend:", trend)

# ==========================================
# SHORT-TERM FORECAST
# NEXT 7 DAYS
# ==========================================

last_date = df["Date"].max()

short_term = []

for i in range(1, 8):

    forecast_date = (
        last_date +
        pd.Timedelta(days=i)
    )

    short_term.append({
        "Date": forecast_date,
        "Forecast_Demand": round(
            recent_average,
            2
        ),
        "Horizon": "Short Term"
    })

short_term_df = pd.DataFrame(
    short_term
)

# ==========================================
# MEDIUM-TERM FORECAST
# NEXT 4 WEEKS
# ==========================================

medium_term = []

for i in range(1, 5):

    forecast_date = (
        last_date +
        pd.Timedelta(weeks=i)
    )

    weekly_demand = (
        recent_average * 7
    )

    medium_term.append({
        "Date": forecast_date,
        "Forecast_Demand": round(
            weekly_demand,
            2
        ),
        "Horizon": "Medium Term"
    })

medium_term_df = pd.DataFrame(
    medium_term
)

# ==========================================
# LONG-TERM FORECAST
# NEXT 3 MONTHS
# ==========================================

long_term = []

for i in range(1, 4):

    forecast_date = (
        last_date +
        pd.DateOffset(months=i)
    )

    monthly_demand = (
        recent_average * 30
    )

    long_term.append({
        "Date": forecast_date,
        "Forecast_Demand": round(
            monthly_demand,
            2
        ),
        "Horizon": "Long Term"
    })

long_term_df = pd.DataFrame(
    long_term
)

# ==========================================
# COMBINE FORECASTS
# ==========================================

forecast_df = pd.concat(
    [
        short_term_df,
        medium_term_df,
        long_term_df
    ],
    ignore_index=True
)

# ==========================================
# SAVE
# ==========================================

forecast_df.to_csv(
    output_path,
    index=False
)

# ==========================================
# DISPLAY
# ==========================================

print("\n================================")
print("DEMAND FORECASTS")
print("================================")

print("\nShort-Term Forecast:")
print(short_term_df)

print("\nMedium-Term Forecast:")
print(medium_term_df)

print("\nLong-Term Forecast:")
print(long_term_df)

print("\n================================")
print("Forecast Trend:", trend)
print("================================")

print("\n✅ Demand Forecasts Generated!")

print("\nSaved at:")
print(output_path)