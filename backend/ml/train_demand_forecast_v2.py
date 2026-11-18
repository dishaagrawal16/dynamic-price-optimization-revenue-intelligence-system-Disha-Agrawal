import os
import joblib
import pandas as pd
import numpy as np

from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

input_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "forecast_dataset_v2.csv"
)

model_path = os.path.join(
    BASE_DIR,
    "demand_forecast_model_v3.pkl"
)

metrics_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "demand_forecast_validation_v3.csv"
)

predictions_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "demand_forecast_predictions_v3.csv"
)


# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(input_path)

df["Date"] = pd.to_datetime(df["Date"])

df = (
    df.sort_values("Date")
    .reset_index(drop=True)
)

print("Dataset Shape:", df.shape)

print(
    "Date Range:",
    df["Date"].min(),
    "to",
    df["Date"].max()
)


# ==========================================
# FEATURE ENGINEERING
# ==========================================

# Lag features
df["Demand_Lag_1"] = df["Demand"].shift(1)

df["Demand_Lag_7"] = df["Demand"].shift(7)

df["Demand_Lag_14"] = df["Demand"].shift(14)

df["Demand_Lag_30"] = df["Demand"].shift(30)


# Rolling demand features
df["Demand_Rolling_7"] = (
    df["Demand"]
    .shift(1)
    .rolling(7)
    .mean()
)

df["Demand_Rolling_14"] = (
    df["Demand"]
    .shift(1)
    .rolling(14)
    .mean()
)

df["Demand_Rolling_30"] = (
    df["Demand"]
    .shift(1)
    .rolling(30)
    .mean()
)


# Rolling standard deviation
df["Demand_Std_7"] = (
    df["Demand"]
    .shift(1)
    .rolling(7)
    .std()
)


# ==========================================
# TIME FEATURES
# ==========================================

df["DayOfYear"] = df["Date"].dt.dayofyear

df["WeekOfYear"] = (
    df["Date"].dt.isocalendar().week.astype(int)
)

df["Days_Since_Start"] = (
    df["Date"] - df["Date"].min()
).dt.days


# ==========================================
# CYCLICAL FEATURES
# ==========================================

df["Month_Sin"] = np.sin(
    2 * np.pi * df["Month"] / 12
)

df["Month_Cos"] = np.cos(
    2 * np.pi * df["Month"] / 12
)

df["Weekday_Sin"] = np.sin(
    2 * np.pi * df["Weekday"] / 7
)

df["Weekday_Cos"] = np.cos(
    2 * np.pi * df["Weekday"] / 7
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
    "Demand_Lag_30",

    "Demand_Rolling_7",
    "Demand_Rolling_14",
    "Demand_Rolling_30",

    "Demand_Std_7",

    "Month",
    "Weekday",

    "DayOfYear",
    "WeekOfYear",
    "Days_Since_Start",

    "Month_Sin",
    "Month_Cos",

    "Weekday_Sin",
    "Weekday_Cos"
]

X = df[features]

y = df["Demand"]


# ==========================================
# CHRONOLOGICAL TRAIN-TEST SPLIT
# ==========================================

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]

X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]

y_test = y.iloc[split_index:]


print("\nTraining Samples:", len(X_train))

print("Testing Samples:", len(X_test))


# ==========================================
# NAIVE FORECAST BASELINE
# ==========================================

# Predict today's demand using the previous day's demand
naive_predictions = df.iloc[split_index:]["Demand_Lag_1"].values

naive_mae = mean_absolute_error(
    y_test,
    naive_predictions
)

naive_rmse = mean_squared_error(
    y_test,
    naive_predictions
) ** 0.5

naive_r2 = r2_score(
    y_test,
    naive_predictions
)

print("\n==========================================")
print("NAIVE FORECAST BASELINE")
print("==========================================")

print("MAE :", round(naive_mae, 2))
print("RMSE:", round(naive_rmse, 2))
print("R2  :", round(naive_r2, 4))
# ==========================================
# MODEL 1 — RANDOM FOREST
# ==========================================

rf_model = RandomForestRegressor(
    n_estimators=300,
    max_depth=12,
    min_samples_leaf=2,
    random_state=42
)

rf_model.fit(
    X_train,
    y_train
)

rf_pred = rf_model.predict(X_test)


# ==========================================
# MODEL 2 — GRADIENT BOOSTING
# ==========================================

gb_model = GradientBoostingRegressor(
    n_estimators=300,
    learning_rate=0.03,
    max_depth=3,
    min_samples_leaf=3,
    random_state=42
)

gb_model.fit(
    X_train,
    y_train
)

gb_pred = gb_model.predict(X_test)


# ==========================================
# EVALUATION FUNCTION
# ==========================================

def evaluate_model(
    model_name,
    y_actual,
    y_prediction
):

    mae = mean_absolute_error(
        y_actual,
        y_prediction
    )

    rmse = mean_squared_error(
        y_actual,
        y_prediction
    ) ** 0.5

    r2 = r2_score(
        y_actual,
        y_prediction
    )

    return {
        "Model": model_name,
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "R2": round(r2, 4)
    }


# ==========================================
# COMPARE MODELS
# ==========================================

rf_results = evaluate_model(
    "Random Forest",
    y_test,
    rf_pred
)

gb_results = evaluate_model(
    "Gradient Boosting",
    y_test,
    gb_pred
)

comparison = pd.DataFrame([
    {
        "Model": "Naive Baseline",
        "MAE": round(naive_mae, 2),
        "RMSE": round(naive_rmse, 2),
        "R2": round(naive_r2, 4)
    },
    rf_results,
    gb_results
])


print("\n==========================================")
print("DEMAND FORECAST MODEL COMPARISON")
print("==========================================")

print(comparison.to_string(index=False))


# ==========================================
# SELECT BEST MODEL
# ==========================================

if rf_results["RMSE"] <= gb_results["RMSE"]:

    best_model = rf_model
    best_predictions = rf_pred
    best_model_name = "Random Forest"

else:

    best_model = gb_model
    best_predictions = gb_pred
    best_model_name = "Gradient Boosting"


print("\n==========================================")
print("BEST MODEL")
print("==========================================")

print("Selected Model:", best_model_name)


# ==========================================
# SAVE VALIDATION RESULTS
# ==========================================

comparison.to_csv(
    metrics_path,
    index=False
)

print("\nValidation metrics saved at:")

print(metrics_path)


# ==========================================
# SAVE ACTUAL VS PREDICTED
# ==========================================

prediction_results = pd.DataFrame({

    "Date": df.iloc[
        split_index:
    ]["Date"].values,

    "Actual_Demand": y_test.values,

    "Predicted_Demand": best_predictions

})

prediction_results["Absolute_Error"] = (
    prediction_results["Actual_Demand"]
    - prediction_results["Predicted_Demand"]
).abs()


prediction_results.to_csv(
    predictions_path,
    index=False
)

print("\nPrediction results saved at:")

print(predictions_path)


# ==========================================
# FEATURE IMPORTANCE
# ==========================================

if hasattr(best_model, "feature_importances_"):

    feature_importance = pd.DataFrame({

        "Feature": features,

        "Importance": (
            best_model.feature_importances_
            * 100
        )

    })

    feature_importance = (
        feature_importance
        .sort_values(
            "Importance",
            ascending=False
        )
    )

    print("\n==========================================")
    print("FEATURE IMPORTANCE")
    print("==========================================")

    print(
        feature_importance
        .to_string(index=False)
    )


# ==========================================
# SAVE BEST MODEL
# ==========================================

joblib.dump(
    best_model,
    model_path
)

print("\n==========================================")

print("✅ V3 Demand Forecast Model Saved!")

print("Model:", best_model_name)

print("Saved at:")

print(model_path)