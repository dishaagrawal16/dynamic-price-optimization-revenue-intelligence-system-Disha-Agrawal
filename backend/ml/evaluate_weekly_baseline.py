import os
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ==========================================
# PATH
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

input_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "weekly_forecast_dataset.csv"
)

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(input_path)

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date").reset_index(drop=True)

# ==========================================
# REMOVE INCOMPLETE FINAL WEEK
# ==========================================

last_date = df["Date"].max()

source_end_date = pd.Timestamp("2024-11-21")

if last_date + pd.Timedelta(days=6) > source_end_date:
    df = df.iloc[:-1].copy()

print("Weekly Dataset Shape:", df.shape)

print(
    "Date Range:",
    df["Date"].min(),
    "to",
    df["Date"].max()
)

# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

split_index = int(len(df) * 0.8)

train = df.iloc[:split_index].copy()
test = df.iloc[split_index:].copy()

print("\nTraining Weeks:", len(train))
print("Testing Weeks:", len(test))

# ==========================================
# BASELINE 1: PREVIOUS WEEK
# ==========================================

test["Previous_Week_Forecast"] = (
    df["Demand"]
    .shift(1)
    .iloc[split_index:]
    .values
)

test = test.dropna(
    subset=["Previous_Week_Forecast"]
)

actual = test["Demand"]

previous_week_prediction = test[
    "Previous_Week_Forecast"
]

mae_previous = mean_absolute_error(
    actual,
    previous_week_prediction
)

rmse_previous = mean_squared_error(
    actual,
    previous_week_prediction
) ** 0.5

r2_previous = r2_score(
    actual,
    previous_week_prediction
)

print("\n===== PREVIOUS WEEK BASELINE =====")

print("MAE :", round(mae_previous, 2))
print("RMSE:", round(rmse_previous, 2))
print("R2  :", round(r2_previous, 4))

# ==========================================
# BASELINE 2: 4-WEEK MOVING AVERAGE
# ==========================================

df["Rolling_4"] = (
    df["Demand"]
    .shift(1)
    .rolling(4)
    .mean()
)

test_rolling = df.iloc[split_index:].copy()

test_rolling = test_rolling.dropna(
    subset=["Rolling_4"]
)

actual_rolling = test_rolling["Demand"]

rolling_prediction = test_rolling[
    "Rolling_4"
]

mae_rolling = mean_absolute_error(
    actual_rolling,
    rolling_prediction
)

rmse_rolling = mean_squared_error(
    actual_rolling,
    rolling_prediction
) ** 0.5

r2_rolling = r2_score(
    actual_rolling,
    rolling_prediction
)

print("\n===== 4-WEEK MOVING AVERAGE =====")

print("MAE :", round(mae_rolling, 2))
print("RMSE:", round(rmse_rolling, 2))
print("R2  :", round(r2_rolling, 4))