import os
import pandas as pd

# -----------------------------
# Paths
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

input_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "demand_dataset.csv"
)

output_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "forecast_dataset.csv"
)

# -----------------------------
# Load dataset
# -----------------------------

df = pd.read_csv(input_path)

print("Original Dataset Shape:", df.shape)

# -----------------------------
# Convert Purchase_Date
# -----------------------------

df["Purchase_Date"] = pd.to_datetime(
    df["Purchase_Date"],
    errors="coerce"
)

# Remove invalid dates
df = df.dropna(subset=["Purchase_Date"])

# -----------------------------
# Sort chronologically
# -----------------------------

df = df.sort_values("Purchase_Date")

# -----------------------------
# Aggregate demand by date
# -----------------------------

forecast_df = (
    df.groupby("Purchase_Date")["Demand"]
    .sum()
    .reset_index()
)

# Rename columns
forecast_df.columns = ["Date", "Demand"]

# -----------------------------
# Add time-based features
# -----------------------------

forecast_df["Year"] = forecast_df["Date"].dt.year
forecast_df["Month"] = forecast_df["Date"].dt.month
forecast_df["Day"] = forecast_df["Date"].dt.day
forecast_df["Weekday"] = forecast_df["Date"].dt.weekday

# -----------------------------
# Save dataset
# -----------------------------

forecast_df.to_csv(
    output_path,
    index=False
)

# -----------------------------
# Display results
# -----------------------------

print("\nForecast Dataset Created Successfully!")

print("Shape:", forecast_df.shape)

print("\nFirst 10 rows:")
print(forecast_df.head(10))

print("\nLast 10 rows:")
print(forecast_df.tail(10))

print("\nSaved at:")
print(output_path)