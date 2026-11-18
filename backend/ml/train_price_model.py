import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dataset_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "encoded_dataset.csv"
)

metrics_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "price_model_validation.csv"
)

predictions_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "price_model_predictions.csv"
)

# ==============================
# Load Dataset
# ==============================

df = pd.read_csv(dataset_path)

print("Dataset Shape:", df.shape)

# ==============================
# Features and Target
# ==============================

X = df[
    [
        "Category",
        "Price (Rs.)",
        "Discount (%)",
        "Payment_Method",
        "Year",
        "Month",
        "Day"
    ]
]

y = df["Final_Price(Rs.)"]

# ==============================
# Train-Test Split
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training Samples:", len(X_train))
print("Testing Samples:", len(X_test))

# ==============================
# Train Model
# ==============================

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# ==============================
# Predictions
# ==============================

predictions = model.predict(X_test)

# ==============================
# Model Validation
# ==============================

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

r2 = r2_score(
    y_test,
    predictions
)

print("\n===== PRICE MODEL PERFORMANCE =====")

print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R2  :", round(r2, 4))

# ==============================
# Save Validation Metrics
# ==============================

validation_results = pd.DataFrame([
    {
        "Model": "Random Forest Price Prediction",
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "R2": round(r2, 4)
    }
])

validation_results.to_csv(
    metrics_path,
    index=False
)

print("\nValidation metrics saved at:")
print(metrics_path)

# ==============================
# Save Actual vs Predicted
# ==============================

prediction_results = pd.DataFrame({
    "Actual_Price": y_test.values,
    "Predicted_Price": predictions
})

prediction_results["Absolute_Error"] = (
    prediction_results["Actual_Price"]
    - prediction_results["Predicted_Price"]
).abs()

prediction_results.to_csv(
    predictions_path,
    index=False
)

print("\nPrediction results saved at:")
print(predictions_path)

# ==============================
# Save Model
# ==============================

model_path = os.path.join(
    BASE_DIR,
    "price_model.pkl"
)

joblib.dump(
    model,
    model_path
)

print("\n✅ Price Model Saved Successfully!")
print(model_path)