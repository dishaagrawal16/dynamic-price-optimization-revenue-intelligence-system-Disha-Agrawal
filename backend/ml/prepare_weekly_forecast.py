import os
import pandas as pd

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

output_path = os.path.join(
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

df = df.sort_values("Date")

print("Daily Dataset Shape:", df.shape)

print(
    "Date Range:",
    df["Date"].min(),
    "to",
    df["Date"].max()
)

# ==========================================
# CREATE WEEKLY DATA
# ==========================================

df = df.set_index("Date")

weekly_df = (
    df["Demand"]
    .resample("W-MON", label="left", closed="left")
    .sum()
    .reset_index()
)

# ==========================================
# ADD TIME FEATURES
# ==========================================

weekly_df["Year"] = weekly_df["Date"].dt.year

weekly_df["Month"] = weekly_df["Date"].dt.month

weekly_df["Week"] = weekly_df["Date"].dt.isocalendar().week.astype(int)

# ==========================================
# REMOVE INCOMPLETE FINAL WEEK
# ==========================================

last_date = df.index.max()

if weekly_df.iloc[-1]["Date"] > last_date:
    weekly_df = weekly_df.iloc[:-1]

# ==========================================
# SAVE
# ==========================================

weekly_df.to_csv(
    output_path,
    index=False
)

# ==========================================
# OUTPUT
# ==========================================

print("\n✅ Weekly Forecast Dataset Created!")

print("Shape:", weekly_df.shape)

print("\nFirst 10 weeks:")
print(
    weekly_df.head(10).to_string(index=False)
)

print("\nLast 10 weeks:")
print(
    weekly_df.tail(10).to_string(index=False)
)

print("\nSaved at:")
print(output_path)