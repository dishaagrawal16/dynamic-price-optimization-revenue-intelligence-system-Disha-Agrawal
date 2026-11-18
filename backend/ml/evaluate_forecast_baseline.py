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
    "forecast_dataset.csv"
)

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(input_path)

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date").reset_index(drop=True)

print("Dataset Shape:", df.shape)

# ==========================================
# TIME-BASED TEST SPLIT
# ==========================================

split_index = int(len(df) * 0.8)

train = df.iloc[:split_index].copy()
test = df.iloc[split_index:].copy()

print("\nTraining Samples:", len(train))
print("Testing Samples:", len(test))

# ==========================================
# BASELINE 1
# Previous Day Demand
# ==========================================

test["Previous_Day_Forecast"] = df["Demand"].shift(1).iloc[
    split_index:
].values

test = test.dropna()

actual = test["Demand"]

previous_day_prediction = test["Previous_Day_Forecast"]

# ==========================================
# EVALUATION
# ==========================================

mae = mean_absolute_error(
    actual,
    previous_day_prediction
)

rmse = mean_squared_error(
    actual,
    previous_day_prediction
) ** 0.5

r2 = r2_score(
    actual,
    previous_day_prediction
)

print("\n===== BASELINE PERFORMANCE =====")

print("Baseline: Previous Day Demand")

print("MAE :", round(mae, 2))

print("RMSE:", round(rmse, 2))

print("R2  :", round(r2, 4))

# ==========================================
# BASELINE 2
# 7-DAY MOVING AVERAGE
# ==========================================

df["Rolling_7"] = (
    df["Demand"]
    .shift(1)
    .rolling(7)
    .mean()
)

test_rolling = df.iloc[split_index:].copy()

test_rolling = test_rolling.dropna(
    subset=["Rolling_7"]
)

actual_rolling = test_rolling["Demand"]

rolling_prediction = test_rolling["Rolling_7"]

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

print("\n===== 7-DAY MOVING AVERAGE =====")

print("MAE :", round(mae_rolling, 2))

print("RMSE:", round(rmse_rolling, 2))

print("R2  :", round(r2_rolling, 4))