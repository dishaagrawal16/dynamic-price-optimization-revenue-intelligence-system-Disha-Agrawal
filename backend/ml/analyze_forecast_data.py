import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

input_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "forecast_dataset.csv"
)

df = pd.read_csv(input_path)

df["Date"] = pd.to_datetime(df["Date"])

print("===== DATASET INFO =====")

print("Rows:", len(df))

print("Date Range:")
print(df["Date"].min(), "to", df["Date"].max())

print("\n===== DEMAND STATISTICS =====")

print(df["Demand"].describe())

print("\n===== FIRST 20 DAYS =====")

print(
    df[["Date", "Demand"]]
    .head(20)
    .to_string(index=False)
)

print("\n===== LAST 20 DAYS =====")

print(
    df[["Date", "Demand"]]
    .tail(20)
    .to_string(index=False)
)

print("\n===== MONTHLY DEMAND =====")

monthly = (
    df.groupby("Month")["Demand"]
    .agg(["mean", "min", "max", "sum"])
)

print(monthly)

print("\n===== WEEKDAY DEMAND =====")

weekday = (
    df.groupby("Weekday")["Demand"]
    .agg(["mean", "min", "max"])
)

print(weekday)

print("\n===== MISSING VALUES =====")

print(df.isnull().sum())