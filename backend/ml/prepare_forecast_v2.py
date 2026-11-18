import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

input_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "demand_dataset_v2.csv"
)

output_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "forecast_dataset_v2.csv"
)

df = pd.read_csv(input_path)

df["Purchase_Date"] = pd.to_datetime(
    df["Purchase_Date"]
)

df = df.sort_values("Purchase_Date")

forecast_df = (
    df.groupby("Purchase_Date")["Demand"]
    .sum()
    .reset_index()
)

forecast_df.columns = [
    "Date",
    "Demand"
]

forecast_df["Year"] = (
    forecast_df["Date"].dt.year
)

forecast_df["Month"] = (
    forecast_df["Date"].dt.month
)

forecast_df["Day"] = (
    forecast_df["Date"].dt.day
)

forecast_df["Weekday"] = (
    forecast_df["Date"].dt.weekday
)

forecast_df.to_csv(
    output_path,
    index=False
)

print("✅ Forecast Dataset V2 Created!")

print("Shape:", forecast_df.shape)

print("\nDemand Statistics:")
print(forecast_df["Demand"].describe())

print("\nFirst 10 rows:")
print(forecast_df.head(10))

print("\nLast 10 rows:")
print(forecast_df.tail(10))

print("\nSaved at:")
print(output_path)