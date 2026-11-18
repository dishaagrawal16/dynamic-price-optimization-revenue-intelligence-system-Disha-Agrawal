import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# -----------------------------
# Load Dataset
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.join(BASE_DIR, "..", "data", "demand_dataset.csv")

df = pd.read_csv(data_path)

print("Dataset Shape:", df.shape)


X = df[
    [
        "Category",
        "Price (Rs.)",
        "Discount (%)",
        "Payment_Method",
        "Year",
        "Month",
        "Day",
        "Weekday",
    ]
]

y = df["Demand"]

# -----------------------------
# Train-Test Split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

# -----------------------------
# Train Model
# -----------------------------

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
)
print(df.head())
print(df.dtypes)
model.fit(X_train, y_train)

# -----------------------------
# Evaluation
# -----------------------------

predictions = model.predict(X_test)

print("MAE :", mean_absolute_error(y_test, predictions))
print("R2 Score :", r2_score(y_test, predictions))

# -----------------------------
# Save Model
# -----------------------------

model_path = os.path.join(BASE_DIR, "demand_model.pkl")

joblib.dump(model, model_path)

print("\n Demand Model Saved Successfully!")
print("Saved at:", model_path)


