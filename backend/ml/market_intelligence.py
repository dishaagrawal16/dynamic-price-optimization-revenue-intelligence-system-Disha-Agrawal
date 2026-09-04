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

INTERNAL_FILE = os.path.join(
    DATA_DIR,
    "demand_dataset.csv"
)

COMPETITOR_FILE = os.path.join(
    DATA_DIR,
    "competitor_prices_final.csv"
)

OUTPUT_FILE = os.path.join(
    DATA_DIR,
    "market_intelligence.csv"
)

PRICING_COMPARISON_FILE = os.path.join(
    DATA_DIR,
    "pricing_comparison.csv"
)
# ============================================================
# CATEGORY MAPPING
# ============================================================

CATEGORY_MAP = {
    0: "Beauty",
    1: "Books",
    2: "Clothing",
    3: "Electronics",
    4: "Home & Kitchen",
    5: "Sports",
    6: "Toys"
}


# ============================================================
# LOAD DATA
# ============================================================

print("Loading internal ecommerce data...")

internal = pd.read_csv(
    INTERNAL_FILE
)

print(
    f"Internal dataset shape: {internal.shape}"
)


print("\nLoading competitor data...")

competitor = pd.read_csv(
    COMPETITOR_FILE
)

print("\nLoading pricing comparison data...")

pricing_comparison = pd.read_csv(
    PRICING_COMPARISON_FILE
)

print(
    f"Competitor dataset shape: {competitor.shape}"
)


# ============================================================
# INTERNAL DATA PREPARATION
# ============================================================

internal["Category_Name"] = (
    internal["Category"]
    .map(CATEGORY_MAP)
)


# ============================================================
# INTERNAL CATEGORY METRICS
# ============================================================

internal_summary = (
    internal
    .groupby("Category_Name")
    .agg(
        Our_Average_Price=(
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
            "Final_Price(Rs.)",
            "sum"
        ),

        Average_Discount=(
            "Discount (%)",
            "mean"
        )
    )
    .reset_index()
)


# ============================================================
# COMPETITOR DISCOUNT
# ============================================================

competitor["Competitor_Discount"] = (
    (
        competitor["MRP"]
        - competitor["Competitor_Price"]
    )
    / competitor["MRP"]
    * 100
)


# Remove invalid values

competitor = competitor[
    competitor["MRP"] > 0
]


# ============================================================
# COMPETITOR CATEGORY METRICS
# ============================================================

competitor_summary = (
    competitor
    .groupby("Category")
    .agg(
        Competitor_Average_Price=(
            "Competitor_Price",
            "mean"
        ),

        Competitor_Average_MRP=(
            "MRP",
            "mean"
        ),

        Competitor_Average_Discount=(
            "Competitor_Discount",
            "mean"
        ),

        Competitor_Product_Count=(
            "Product_Name",
            "count"
        )
    )
    .reset_index()
)


# ============================================================
# MERGE OUR DATA + COMPETITOR DATA
# ============================================================

market = internal_summary.merge(
    competitor_summary,
    left_on="Category_Name",
    right_on="Category",
    how="left"
)


market.drop(
    columns=["Category"],
    inplace=True
)


# ============================================================
# PRICE GAP
# ============================================================

market["Price_Gap"] = (
    market["Our_Average_Price"]
    - market["Competitor_Average_Price"]
)

market["Price_Gap_Percent"] = (
    market["Price_Gap"]
    / market["Competitor_Average_Price"]
    * 100
)


# ============================================================
# COMPARABILITY
# ============================================================

# Get comparability information from pricing comparison analysis

comparability = pricing_comparison[
    [
        "Category",
        "Comparable"
    ]
].drop_duplicates(
    subset=["Category"]
)

market = market.merge(
    comparability,
    left_on="Category_Name",
    right_on="Category",
    how="left"
)

market.drop(
    columns=["Category"],
    inplace=True
)


# Categories without a comparability flag are assumed comparable
market["Comparable"] = (
    market["Comparable"]
    .fillna(True)
)


# Electronics currently has non-comparable competitor data
# because Croma products are much higher-priced than our
# internal Electronics products.

market.loc[
    market["Comparable"] == False,
    "Price_Gap"
] = None

market.loc[
    market["Comparable"] == False,
    "Price_Gap_Percent"
] = None

# ============================================================
# DISCOUNT GAP
# ============================================================

market["Discount_Gap"] = (
    market["Average_Discount"]
    - market["Competitor_Average_Discount"]
)


# ============================================================
# MARKET POSITION
# ============================================================

def determine_market_position(row):

    if pd.isna(
        row["Competitor_Average_Price"]
    ):
        return "No competitor data"

    if not row["Comparable"]:
        return "Insufficient Comparable Data"

    gap = row["Price_Gap_Percent"]

    if gap <= -10:
        return "Below Competitor"

    elif gap >= 10:
        return "Above Competitor"

    else:
        return "Competitive"


market["Market_Position"] = (
    market.apply(
        determine_market_position,
        axis=1
    )
)


# ============================================================
# COMPETITIVE PRESSURE
# ============================================================

def determine_pressure(row):

    if pd.isna(
        row["Competitor_Average_Price"]
    ):
        return "Unknown"

    if not row["Comparable"]:
        return "Unknown"

    gap = abs(
        row["Price_Gap_Percent"]
    )

    if gap >= 50:
        return "High"

    elif gap >= 20:
        return "Medium"

    else:
        return "Low"


market["Competitive_Pressure"] = (
    market.apply(
        determine_pressure,
        axis=1
    )
)


# ============================================================
# MARKET OPPORTUNITY
# ============================================================

def determine_opportunity(row):

    if pd.isna(
        row["Competitor_Average_Price"]
    ):
        return "Insufficient competitor data"

    if not row["Comparable"]:
        return "Insufficient comparable data"

    if (
        row["Price_Gap_Percent"] < -20
        and row["Average_Demand"] > 120
    ):
        return "Potential upward pricing opportunity"

    elif (
        row["Price_Gap_Percent"] > 20
        and row["Average_Demand"] < 130
    ):
        return "Consider price reduction"

    elif (
        row["Price_Gap_Percent"] < -20
    ):
        return "Monitor for controlled price increase"

    else:
        return "Maintain competitive pricing"

market["Market_Opportunity"] = (
    market.apply(
        determine_opportunity,
        axis=1
    )
)


# ============================================================
# MARKET INSIGHT
# ============================================================

def generate_insight(row):

    if pd.isna(
        row["Competitor_Average_Price"]
    ):
        return (
            "Competitor pricing data is currently "
            "unavailable for this category."
        )

    if not row["Comparable"]:
        return (
            "Competitor data is available, but the "
            "observed products are not sufficiently "
            "comparable with our internal products."
        )

    if (
        row["Price_Gap_Percent"] < -50
        and row["Average_Demand"] > 120
    ):
        return (
            "Our price is substantially below the "
            "observed competitor level while demand "
            "remains healthy. A controlled price "
            "increase could be tested."
        )

    elif (
        row["Price_Gap_Percent"] < -20
    ):
        return (
            "Our products are priced below the "
            "observed competitor level. Monitor "
            "demand and evaluate gradual price "
            "optimization."
        )

    elif (
        row["Price_Gap_Percent"] > 20
    ):
        return (
            "Our prices are above the observed "
            "competitor level. Demand should be "
            "monitored for possible price sensitivity."
        )

    else:
        return (
            "Our pricing is relatively close to "
            "the observed competitor level."
        )


market["Market_Insight"] = (
    market.apply(
        generate_insight,
        axis=1
    )
)


# ============================================================
# ROUND VALUES
# ============================================================

numeric_columns = [
    "Our_Average_Price",
    "Average_Demand",
    "Total_Demand",
    "Total_Revenue",
    "Average_Discount",
    "Competitor_Average_Price",
    "Competitor_Average_MRP",
    "Competitor_Average_Discount",
    "Price_Gap",
    "Price_Gap_Percent",
    "Discount_Gap"
]


market[numeric_columns] = (
    market[numeric_columns]
    .round(2)
)


# ============================================================
# DISPLAY
# ============================================================

print("\n")
print("=" * 60)
print("MARKET INTELLIGENCE ANALYSIS")
print("=" * 60)

print(
    market[
        [
            "Category_Name",
            "Our_Average_Price",
            "Competitor_Average_Price",
            "Price_Gap_Percent",
            "Average_Demand",
            "Average_Discount",
            "Competitor_Average_Discount",
            "Market_Position",
            "Competitive_Pressure",
            "Market_Opportunity"
        ]
    ].to_string(index=False)
)


# ============================================================
# SAVE
# ============================================================

market.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\nSaved at:")
print(
    os.path.abspath(OUTPUT_FILE)
)