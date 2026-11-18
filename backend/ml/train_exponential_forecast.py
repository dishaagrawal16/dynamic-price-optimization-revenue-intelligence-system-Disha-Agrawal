import os
import joblib
import pandas as pd

from statsmodels.tsa.holtwinters import ExponentialSmoothing
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

model_path = os.path.join(
    BASE_DIR,
    "exponential_demand_forecast.pkl"
)


# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(input_path)

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date")

df = df.set_index("Date")

# Make sure frequency is daily
df = df.asfreq("D")

# Fill any missing dates using interpolation
df["Demand"] = df["Demand"].interpolate()

print("Dataset Shape:", df.shape)

print(
    "Date Range:",
    df.index.min(),
    "to",
    df.index.max()
)


# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

split_index = int(len(df) * 0.8)

train = df["Demand"].iloc[:split_index]

test = df["Demand"].iloc[split_index:]

print("\nTraining Samples:", len(train))
print("Testing Samples:", len(test))


# ==========================================
# EXPONENTIAL SMOOTHING MODEL
# ==========================================

model = ExponentialSmoothing(
    train,
    trend="add",
    seasonal="add",
    seasonal_periods=7,
    initialization_method="estimated"
)

fitted_model = model.fit(
    optimized=True
)


# ==========================================
# FORECAST
# ==========================================

forecast = fitted_model.forecast(
    len(test)
)


# ==========================================
# EVALUATION
# ==========================================

mae = mean_absolute_error(
    test,
    forecast
)

rmse = mean_squared_error(
    test,
    forecast
) ** 0.5

r2 = r2_score(
    test,
    forecast
)


print("\n===== EXPONENTIAL SMOOTHING PERFORMANCE =====")

print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R2  :", round(r2, 4))


# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(
    fitted_model,
    model_path
)

print("\n✅ Exponential Smoothing Model Saved!")

print("Saved at:")
print(model_path)