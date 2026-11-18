import os
import pandas as pd

# ==========================================
# PATH
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

input_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "forecast_dataset_v2.csv"
)

output_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "seasonal_analysis.csv"
)

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(input_path)

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date")

# ==========================================
# MONTHLY DEMAND
# ==========================================

monthly = (
    df.groupby("Month")["Demand"]
    .agg(
        Average_Demand="mean",
        Total_Demand="sum"
    )
    .reset_index()
)

# ==========================================
# OVERALL AVERAGE
# ==========================================

overall_average = df["Demand"].mean()

# ==========================================
# SEASONAL FACTOR
# ==========================================

monthly["Seasonal_Factor"] = (
    monthly["Average_Demand"] /
    overall_average
)

monthly["Seasonal_Factor"] = (
    monthly["Seasonal_Factor"]
    .round(3)
)

# ==========================================
# SEASONAL CLASSIFICATION
# ==========================================

def classify_season(factor):

    if factor >= 1.10:
        return "High Demand"

    elif factor <= 0.90:
        return "Low Demand"

    else:
        return "Normal Demand"


monthly["Demand_Level"] = (
    monthly["Seasonal_Factor"]
    .apply(classify_season)
)

# ==========================================
# DISPLAY
# ==========================================

print("\n================================")
print("SEASONAL DEMAND ANALYSIS")
print("================================")

print(
    "\nOverall Average Demand:",
    round(overall_average, 2)
)

print("\nMonthly Analysis:")

print(
    monthly.to_string(index=False)
)

# ==========================================
# SAVE
# ==========================================

monthly.to_csv(
    output_path,
    index=False
)

print("\n✅ Seasonal Analysis Created!")

print("\nSaved at:")
print(output_path)
