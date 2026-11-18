import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ==========================================
# PATHS
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
    "demand_forecast_model.pkl"
)


# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(input_path)

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date").reset_index(drop=True)

print("Dataset Shape:", df.shape)

print("\nDate Range:")
print(df["Date"].min(), "to", df["Date"].max())


# ==========================================
# CREATE LAG FEATURES
# ==========================================

df["Demand_Lag_1"] = df["Demand"].shift(1)

df["Demand_Lag_7"] = df["Demand"].shift(7)

df["Demand_Lag_14"] = df["Demand"].shift(14)


# ==========================================
# CREATE ROLLING FEATURES
# ==========================================

df["Demand_Rolling_7"] = (
    df["Demand"]
    .shift(1)
    .rolling(7)
    .mean()
)

df["Demand_Rolling_30"] = (
    df["Demand"]
    .shift(1)
    .rolling(30)
    .mean()
)


# ==========================================
# REMOVE MISSING VALUES
# ==========================================

df = df.dropna().reset_index(drop=True)


# ==========================================
# FEATURES
# ==========================================

features = [
    "Demand_Lag_1",
    "Demand_Lag_7",
    "Demand_Lag_14",
    "Demand_Rolling_7",
    "Demand_Rolling_30",
    "Month",
    "Weekday"
]

X = df[features]

y = df["Demand"]


# ==========================================
# TIME-BASED TRAIN TEST SPLIT
# ==========================================

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]

X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]

y_test = y.iloc[split_index:]


print("\nTraining Samples:", len(X_train))

print("Testing Samples:", len(X_test))


# ==========================================
# TRAIN MODEL
# ==========================================

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)


# ==========================================
# PREDICTION
# ==========================================

y_pred = model.predict(X_test)


# ==========================================
# EVALUATION
# ==========================================

mae = mean_absolute_error(y_test, y_pred)

rmse = mean_squared_error(
    y_test,
    y_pred
) ** 0.5

r2 = r2_score(
    y_test,
    y_pred
)


print("\n===== MODEL PERFORMANCE =====")

print("MAE :", round(mae, 2))

print("RMSE:", round(rmse, 2))

print("R2  :", round(r2, 4))


# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(
    model,
    model_path
)

print("\n✅ Demand Forecast Model Saved!")

print("Saved at:")
print(model_path)