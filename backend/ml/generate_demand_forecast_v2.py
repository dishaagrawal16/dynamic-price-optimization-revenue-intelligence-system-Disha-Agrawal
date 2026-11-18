import os
import pandas as pd

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

seasonal_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "seasonal_analysis.csv"
)

output_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "demand_forecasts_v2.csv"
)

# ==========================================
# LOAD HISTORICAL DATA
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
# LOAD SEASONAL FACTORS
# ==========================================

seasonal_df = pd.read_csv(seasonal_path)

seasonal_factors = dict(
    zip(
        seasonal_df["Month"],
        seasonal_df["Seasonal_Factor"]
    )
)

# ==========================================
# RECENT DEMAND
# ==========================================

recent_average = (
    df["Demand"]
    .tail(7)
    .mean()
)

overall_average = (
    df["Demand"]
    .mean()
)

# ==========================================
# CURRENT MONTH
# ==========================================

last_date = df["Date"].max()

current_month = last_date.month

current_seasonal_factor = seasonal_factors.get(
    current_month,
    1.0
)

# Remove current seasonal effect
# so that we don't apply it twice.

seasonally_adjusted_baseline = (
    recent_average /
    current_seasonal_factor
)

# ==========================================
# TREND
# ==========================================

recent_7 = (
    df["Demand"]
    .tail(7)
    .mean()
)

previous_7 = (
    df["Demand"]
    .iloc[-14:-7]
    .mean()
)

if recent_7 > previous_7 * 1.05:

    trend = "Increasing"
    trend_multiplier = 1.03

elif recent_7 < previous_7 * 0.95:

    trend = "Decreasing"
    trend_multiplier = 0.97

else:

    trend = "Stable"
    trend_multiplier = 1.00

# ==========================================
# FORECAST FUNCTION
# ==========================================

def calculate_forecast(
    forecast_date,
    days
):

    month = forecast_date.month

    # If historical seasonal information
    # does not exist, use neutral factor.

    future_seasonal_factor = seasonal_factors.get(
        month,
        1.0
    )

    daily_forecast = (
        seasonally_adjusted_baseline
        * future_seasonal_factor
        * trend_multiplier
    )

    total_forecast = (
        daily_forecast * days
    )

    return (
        daily_forecast,
        total_forecast,
        future_seasonal_factor
    )

# ==========================================
# SHORT-TERM
# ==========================================

short_term = []

for i in range(1, 8):

    forecast_date = (
        last_date +
        pd.Timedelta(days=i)
    )

    daily_forecast, _, seasonal_factor = (
        calculate_forecast(
            forecast_date,
            1
        )
    )

    short_term.append({

        "Date": forecast_date,

        "Forecast_Demand": round(
            daily_forecast,
            2
        ),

        "Seasonal_Factor": seasonal_factor,

        "Trend": trend,

        "Horizon": "Short Term"

    })

short_term_df = pd.DataFrame(
    short_term
)

# ==========================================
# MEDIUM-TERM
# FOLLOWING 4 WEEKS AFTER SHORT-TERM
# ==========================================

medium_term = []

for i in range(2, 6):

    forecast_date = (
        last_date +
        pd.Timedelta(weeks=i)
    )

    daily_forecast, weekly_forecast, seasonal_factor = (
        calculate_forecast(
            forecast_date,
            7
        )
    )

    medium_term.append({
        "Date": forecast_date,
        "Forecast_Demand": round(
            weekly_forecast,
            2
        ),
        "Seasonal_Factor": seasonal_factor,
        "Trend": trend,
        "Horizon": "Medium Term"
    })

medium_term_df = pd.DataFrame(
    medium_term
)
# ==========================================
# LONG-TERM
# ==========================================

# ==========================================
# LONG-TERM
# NEXT 3 MONTHS AFTER MEDIUM-TERM
# ==========================================

long_term = []

for i in range(2, 5):

    forecast_date = (
        last_date +
        pd.DateOffset(months=i)
    )

    daily_forecast, _, seasonal_factor = (
        calculate_forecast(
            forecast_date,
            30
        )
    )

    monthly_forecast = (
        daily_forecast * 30
    )

    long_term.append({
        "Date": forecast_date,
        "Forecast_Demand": round(
            monthly_forecast,
            2
        ),
        "Seasonal_Factor": seasonal_factor,
        "Trend": trend,
        "Horizon": "Long Term"
    })

long_term_df = pd.DataFrame(
    long_term
)

# ==========================================
# COMBINE
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
# RELIABILITY SCORE
# ==========================================

validation_mae = 401.36

mean_demand = df["Demand"].mean()

error_rate = (
    validation_mae /
    mean_demand
)

reliability_score = max(
    0,
    (1 - error_rate) * 100
)

reliability_score = round(
    reliability_score,
    2
)

forecast_df["Reliability_Score"] = (
    reliability_score
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

print("\n========================================")
print("FORECAST SUMMARY")
print("========================================")

print(
    "Overall Average Demand:",
    round(overall_average, 2)
)

print(
    "Recent 7-Day Average:",
    round(recent_average, 2)
)

print(
    "Current Seasonal Factor:",
    current_seasonal_factor
)

print(
    "Seasonally Adjusted Baseline:",
    round(
        seasonally_adjusted_baseline,
        2
    )
)

print(
    "Trend:",
    trend
)

print(
    "Reliability Score:",
    reliability_score,
    "%"
)

print("\n========================================")
print("SHORT-TERM FORECAST")
print("========================================")

print(
    short_term_df.to_string(
        index=False
    )
)

print("\n========================================")
print("MEDIUM-TERM FORECAST")
print("========================================")

print(
    medium_term_df.to_string(
        index=False
    )
)

print("\n========================================")
print("LONG-TERM FORECAST")
print("========================================")

print(
    long_term_df.to_string(
        index=False
    )
)

print("\n✅ Corrected V2 Forecast Generated!")

print("\nSaved at:")
print(output_path)