import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

original_path = os.path.join(
    DATA_DIR,
    "ecommerce_dataset_updated.csv"
)

demand_path = os.path.join(
    DATA_DIR,
    "demand_dataset.csv"
)

print("Original dataset path:")
print(os.path.abspath(original_path))

print("\nDemand dataset path:")
print(os.path.abspath(demand_path))

if not os.path.exists(original_path):
    print("\n❌ ecommerce_dataset.csv not found.")
    print("\nFiles available:")
    print(os.listdir(DATA_DIR))
    exit()

if not os.path.exists(demand_path):
    print("\n❌ demand_dataset.csv not found.")
    print("\nFiles available:")
    print(os.listdir(DATA_DIR))
    exit()

# Load datasets
original = pd.read_csv(original_path)
demand = pd.read_csv(demand_path)

print("\nOriginal dataset shape:", original.shape)
print("Demand dataset shape:", demand.shape)

# Product_ID -> original category
category_map = (
    original[["Product_ID", "Category"]]
    .drop_duplicates()
)

# Product_ID -> encoded category
encoded_map = (
    demand[["Product_ID", "Category"]]
    .drop_duplicates()
    .rename(
        columns={
            "Category": "Category_Code"
        }
    )
)

# Merge
result = category_map.merge(
    encoded_map,
    on="Product_ID",
    how="inner"
)

print("\n===== CATEGORY CODE MAPPING =====")

mapping = (
    result
    .groupby(["Category_Code", "Category"])
    .size()
    .reset_index(name="Products")
    .sort_values("Category_Code")
)

print(mapping.to_string(index=False))