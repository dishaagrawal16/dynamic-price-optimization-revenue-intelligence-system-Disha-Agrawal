import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

input_path = os.path.join(BASE_DIR, "..", "data", "encoded_dataset.csv")

df = pd.read_csv(input_path)
# Reproducible randomness
np.random.seed(42)

# Base demand
demand = 120

# Higher discount → higher demand
demand += df["Discount (%)"] * 3

# Higher price → lower demand
demand -= df["Price (Rs.)"] * 0.20

# Seasonal effect
demand += np.where(df["Month"].isin([10, 11, 12]), 30, 0)

# Category effect
electronics_bonus = np.where(df["Category"] == 0, 20, 0)
fashion_bonus = np.where(df["Category"] == 1, 10, 0)

demand += electronics_bonus
demand += fashion_bonus

# Random variation
demand += np.random.randint(-5, 6, len(df))

# Prevent negative demand
df["Demand"] = demand.clip(lower=10).astype(int)

# Save dataset
output_path = os.path.join(BASE_DIR, "..", "data", "demand_dataset.csv")

df.to_csv(output_path, index=False)

print("✅ Demand dataset created successfully!")
print("Saved at:", output_path)
print(df[["Demand"]].head())
