import os
import numpy as np
import pandas as pd

# ==========================================
# PATHS
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

input_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "encoded_dataset.csv"
)

output_path = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "demand_dataset_v2.csv"
)

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(input_path)

df["Purchase_Date"] = pd.to_datetime(
    df["Purchase_Date"]
)

df = df.sort_values("Purchase_Date").reset_index(drop=True)

print("Input Dataset Shape:", df.shape)

# ==========================================
# REPRODUCIBILITY
# ==========================================

np.random.seed(42)

# ==========================================
# DATE FEATURES
# ==========================================

df["Month"] = df["Purchase_Date"].dt.month

df["Day"] = df["Purchase_Date"].dt.day

df["Weekday"] = df["Purchase_Date"].dt.weekday

# Days since beginning of dataset
df["Days_From_Start"] = (
    df["Purchase_Date"] -
    df["Purchase_Date"].min()
).dt.days

# ==========================================
# DAILY SEASONAL DEMAND
# ==========================================

# Base demand per transaction
base_demand = 120

# ------------------------------------------
# Long-term trend
# ------------------------------------------

trend_effect = (
    df["Days_From_Start"] / 365
) * 25

# ------------------------------------------
# Monthly / seasonal effect
# ------------------------------------------

monthly_effect = df["Month"].map({
    1: 0,
    2: -5,
    3: 5,
    4: 10,
    5: 3,
    6: -2,
    7: 2,
    8: 5,
    9: 10,
    10: 25,
    11: 30,
    12: 35
}).fillna(0)

# ------------------------------------------
# Weekday effect
# ------------------------------------------

weekday_effect = df["Weekday"].map({
    0: 0,    # Monday
    1: 3,    # Tuesday
    2: 0,    # Wednesday
    3: 5,    # Thursday
    4: 8,    # Friday
    5: 15,   # Saturday
    6: 20    # Sunday
}).fillna(0)

# ==========================================
# CATEGORY EFFECT
# ==========================================

category_effect = df["Category"].map({
    0: 10,
    1: 5,
    2: 0,
    3: 15
}).fillna(0)

# ==========================================
# DISCOUNT EFFECT
# ==========================================

discount_effect = (
    df["Discount (%)"] * 1.2
)

# ==========================================
# PRICE EFFECT
# ==========================================

# Normalize price effect
price_effect = (
    -(df["Price (Rs.)"] / 1000) * 8
)

# ==========================================
# COMBINE EFFECTS
# ==========================================

demand = (
    base_demand
    + trend_effect
    + monthly_effect
    + weekday_effect
    + category_effect
    + discount_effect
    + price_effect
)

# ==========================================
# ADD SMALL REALISTIC NOISE
# ==========================================

noise = np.random.normal(
    loc=0,
    scale=5,
    size=len(df)
)

demand = demand + noise

# ==========================================
# ENSURE VALID DEMAND
# ==========================================

demand = np.maximum(
    demand,
    20
)

df["Demand"] = np.round(
    demand
).astype(int)

# ==========================================
# KEEP REQUIRED COLUMNS
# ==========================================

columns_to_keep = [
    "User_ID",
    "Product_ID",
    "Category",
    "Price (Rs.)",
    "Discount (%)",
    "Final_Price(Rs.)",
    "Payment_Method",
    "Purchase_Date",
    "Year",
    "Month",
    "Day",
    "Weekday",
    "Demand"
]

# Only keep columns that exist
columns_to_keep = [
    col for col in columns_to_keep
    if col in df.columns
]

df = df[columns_to_keep]

# ==========================================
# SAVE
# ==========================================

df.to_csv(
    output_path,
    index=False
)

# ==========================================
# RESULTS
# ==========================================

print("\n✅ Realistic Demand Dataset Created!")

print("Shape:", df.shape)

print("\nDemand Statistics:")
print(df["Demand"].describe())

print("\nFirst 10 rows:")
print(
    df[
        [
            "Purchase_Date",
            "Category",
            "Price (Rs.)",
            "Discount (%)",
            "Demand"
        ]
    ].head(10)
)

print("\nSaved at:")
print(output_path)