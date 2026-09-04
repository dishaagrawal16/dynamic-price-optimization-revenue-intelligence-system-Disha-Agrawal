import os
import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "..",
    "data"
)

INTERNAL_PATH = os.path.join(
    DATA_DIR,
    "demand_dataset.csv"
)

COMPETITOR_PATH = os.path.join(
    DATA_DIR,
    "competitor_prices_final.csv"
)

OUTPUT_PATH = os.path.join(
    DATA_DIR,
    "pricing_comparison.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("Loading internal ecommerce data...")

internal = pd.read_csv(
    INTERNAL_PATH
)

print(
    "Internal dataset shape:",
    internal.shape
)


print("\nLoading competitor data...")

competitor = pd.read_csv(
    COMPETITOR_PATH
)

print(
    "Competitor dataset shape:",
    competitor.shape
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


internal["Category_Name"] = (
    internal["Category"]
    .map(category_mapping)
)


# ============================================================
# INTERNAL PRICE SUMMARY
# ============================================================

internal_summary = (

    internal
    .groupby("Category_Name")
    .agg(
        Our_Average_Price=(
            "Price (Rs.)",
            "mean"
        ),

        Our_Average_Final_Price=(
            "Final_Price(Rs.)",
            "mean"
        ),

        Our_Average_Demand=(
            "Demand",
            "mean"
        ),

        Total_Demand=(
            "Demand",
            "sum"
        ),

        Total_Revenue=(
            "Final_Price(Rs.)",
            lambda x: 0
        )
    )
    .reset_index()

)


# ============================================================
# CALCULATE INTERNAL REVENUE
# ============================================================

internal["Revenue"] = (
    internal["Final_Price(Rs.)"]
    * internal["Demand"]
)


revenue_summary = (

    internal
    .groupby("Category_Name")["Revenue"]
    .sum()
    .reset_index()
    .rename(
        columns={
            "Revenue":
                "Total_Revenue"
        }
    )

)


# Remove placeholder revenue

internal_summary = internal_summary.drop(
    columns=["Total_Revenue"]
)


internal_summary = internal_summary.merge(
    revenue_summary,
    on="Category_Name",
    how="left"
)


# ============================================================
# COMPETITOR SUMMARY
# ============================================================

competitor_summary = (

    competitor
    .groupby(
        [
            "Category",
            "Competitor"
        ]
    )
    .agg(
        Competitor_Average_Price=(
            "Competitor_Price",
            "mean"
        ),

        Competitor_Min_Price=(
            "Competitor_Price",
            "min"
        ),

        Competitor_Max_Price=(
            "Competitor_Price",
            "max"
        ),

        Competitor_Product_Count=(
            "Product_Name",
            "count"
        )
    )
    .reset_index()

)


# ============================================================
# MERGE
# ============================================================

comparison = competitor_summary.merge(

    internal_summary,

    left_on="Category",

    right_on="Category_Name",

    how="left"

)


# ============================================================
# PRICE GAP
# ============================================================

comparison["Price_Gap"] = (
    comparison["Our_Average_Final_Price"]
    - comparison["Competitor_Average_Price"]
)

comparison["Price_Gap_Percent"] = (
    comparison["Price_Gap"]
    /
    comparison["Competitor_Average_Price"]
    * 100
)


# ============================================================
# COMPARABILITY
# ============================================================

# Croma currently contains high-value laptops/tablets,
# while our internal Electronics products are much lower priced.
# Therefore, a direct category-level price-gap calculation
# would not be a meaningful comparison.

comparison["Comparable"] = True

comparison.loc[
    comparison["Category"] == "Electronics",
    "Comparable"
] = False

comparison.loc[
    comparison["Category"] == "Electronics",
    "Price_Gap"
] = None

comparison.loc[
    comparison["Category"] == "Electronics",
    "Price_Gap_Percent"
] = None


# ============================================================
# MARKET POSITION
# ============================================================

def market_position(row):

    if not row["Comparable"]:
        return "Insufficient Comparable Data"

    gap = row["Price_Gap_Percent"]

    if gap <= -10:
        return "Below Competitor"

    elif gap >= 10:
        return "Above Competitor"

    else:
        return "Price Aligned"


comparison["Market_Position"] = (

    comparison.apply(
        market_position,
        axis=1
    )

)


# ============================================================
# ROUND NUMBERS
# ============================================================

numeric_columns = [

    "Our_Average_Price",

    "Our_Average_Final_Price",

    "Our_Average_Demand",

    "Total_Demand",

    "Total_Revenue",

    "Competitor_Average_Price",

    "Competitor_Min_Price",

    "Competitor_Max_Price",

    "Price_Gap",

    "Price_Gap_Percent"

]


for column in numeric_columns:

    comparison[column] = comparison[
        column
    ].round(2)


# ============================================================
# SAVE
# ============================================================

comparison.to_csv(
    OUTPUT_PATH,
    index=False
)


# ============================================================
# OUTPUT
# ============================================================

print("\n========================================")
print("PRICING COMPARISON REPORT")
print("========================================")

print(

    comparison[
        [
            "Category",
            "Competitor",
            "Our_Average_Final_Price",
            "Competitor_Average_Price",
            "Price_Gap",
            "Price_Gap_Percent",
            "Market_Position"
        ]
    ]
    .to_string(index=False)

)


print("\nSaved at:")

print(
    os.path.abspath(
        OUTPUT_PATH
    )
)