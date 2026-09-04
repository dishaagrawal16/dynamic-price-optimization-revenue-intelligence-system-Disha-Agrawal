import os
import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

INPUT_PATH = os.path.join(
    DATA_DIR,
    "demand_dataset.csv"
)

OUTPUT_PATH = os.path.join(
    DATA_DIR,
    "profitability_analysis.csv"
)


# ============================================================
# CATEGORY MAPPING
# ============================================================

category_mapping = {
    0: "Beauty",
    1: "Books",
    2: "Clothing",
    3: "Electronics",
    4: "Home & Kitchen",
    5: "Sports",
    6: "Toys"
}

# ============================================================
# ESTIMATED COST RATIO
# ============================================================

# Actual product cost is not available in the source dataset.
# These configurable ratios are used only for estimated
# profitability analysis.

estimated_cost_ratio = {
    "Beauty": 0.65,
    "Books": 0.70,
    "Clothing": 0.60,
    "Electronics": 0.75,
    "Home & Kitchen": 0.68,
    "Sports": 0.65,
    "Toys": 0.70
}

# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(INPUT_PATH)

print("Dataset Shape:", df.shape)


# ============================================================
# MAP CATEGORY
# ============================================================

df["Category_Name"] = df["Category"].map(
    category_mapping
)


# ============================================================
# CALCULATE REVENUE
# ============================================================

df["Revenue"] = (
    df["Final_Price(Rs.)"]
    * df["Demand"]
)

# ============================================================
# ESTIMATED COST
# ============================================================

df["Estimated_Cost_Ratio"] = (
    df["Category_Name"]
    .map(estimated_cost_ratio)
)

df["Estimated_Cost"] = (
    df["Revenue"]
    * df["Estimated_Cost_Ratio"]
)


# ============================================================
# ESTIMATED PROFIT
# ============================================================

df["Estimated_Profit"] = (
    df["Revenue"]
    - df["Estimated_Cost"]
)
# ============================================================
# CALCULATE GROSS SALES
# ============================================================

df["Gross_Sales"] = (
    df["Price (Rs.)"]
    * df["Demand"]
)


# ============================================================
# DISCOUNT AMOUNT
# ============================================================

df["Discount_Amount"] = (
    df["Price (Rs.)"]
    - df["Final_Price(Rs.)"]
)


# ============================================================
# CATEGORY PROFITABILITY
# ============================================================

analysis = (
    df.groupby("Category_Name")
    .agg(
        Total_Products=(
            "Product_ID",
            "count"
        ),

        Average_Price=(
            "Price (Rs.)",
            "mean"
        ),

        Average_Final_Price=(
            "Final_Price(Rs.)",
            "mean"
        ),

        Average_Demand=(
            "Demand",
            "mean"
        ),

        Total_Demand=(
            "Demand",
            "sum"
        ),

        Total_Revenue=(
            "Revenue",
            "sum"
        ),

        Estimated_Cost=(
            "Estimated_Cost",
            "sum"
        ),
        
        Estimated_Profit=(
            "Estimated_Profit",
            "sum"
        ),

        Average_Revenue=(
            "Revenue",
            "mean"
        ),

        Total_Gross_Sales=(
            "Gross_Sales",
            "sum"
        ),

        Average_Discount=(
            "Discount (%)",
            "mean"
        ),

        Total_Discount=(
            "Discount_Amount",
            "sum"
        )
    )
    .reset_index()
)

# ============================================================
# ESTIMATED PROFIT MARGIN
# ============================================================

analysis["Estimated_Profit_Margin"] = (
    analysis["Estimated_Profit"]
    /
    analysis["Total_Revenue"]
    * 100
)


# ============================================================
# PROFITABILITY LEVEL
# ============================================================

def classify_profitability(margin):

    if margin >= 30:
        return "High"

    elif margin >= 15:
        return "Moderate"

    else:
        return "Low"


analysis["Profitability_Level"] = (
    analysis["Estimated_Profit_Margin"]
    .apply(classify_profitability)
)

# ============================================================
# ROUND VALUES
# ============================================================

numeric_columns = analysis.select_dtypes(
    include="number"
).columns

analysis[numeric_columns] = analysis[
    numeric_columns
].round(2)


# ============================================================
# SAVE
# ============================================================

analysis.to_csv(
    OUTPUT_PATH,
    index=False
)


# ============================================================
# DISPLAY
# ============================================================

print("\n========================================")
print("PROFITABILITY ANALYSIS")
print("========================================")

print(
    analysis.to_string(
        index=False
    )
)

print("\nSaved at:")

print(
    os.path.abspath(
        OUTPUT_PATH
    )
) 