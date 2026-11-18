import os
import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")


INTERNAL_DATA = os.path.join(
    DATA_DIR,
    "demand_dataset.csv"
)

COMPETITOR_DATA = os.path.join(
    DATA_DIR,
    "competitor_prices.csv"
)

OUTPUT_DATA = os.path.join(
    DATA_DIR,
    "competitor_analysis.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("Loading internal ecommerce data...")

internal = pd.read_csv(
    INTERNAL_DATA
)

print(
    "Internal dataset shape:",
    internal.shape
)


print("\nLoading competitor data...")

competitor = pd.read_csv(
    COMPETITOR_DATA
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


internal["Category_Name"] = internal[
    "Category"
].map(category_mapping)


# ============================================================
# INTERNAL SPORTS DATA
# ============================================================

sports_internal = internal[
    internal["Category_Name"] == "Sports"
].copy()


# ============================================================
# INTERNAL PRICE
# ============================================================

our_average_price = sports_internal[
    "Final_Price(Rs.)"
].mean()


our_average_demand = sports_internal[
    "Demand"
].mean()


# ============================================================
# COMPETITOR PRICE
# ============================================================

competitor_average_price = competitor[
    "Competitor_Price"
].mean()


competitor_min_price = competitor[
    "Competitor_Price"
].min()


competitor_max_price = competitor[
    "Competitor_Price"
].max()


# ============================================================
# COMPETITOR DISCOUNT
# ============================================================

competitor["Discount_Percent"] = (
    (
        competitor["MRP"]
        - competitor["Competitor_Price"]
    )
    /
    competitor["MRP"]
) * 100


average_competitor_discount = (
    competitor["Discount_Percent"].mean()
)


# ============================================================
# PRICE GAP
# ============================================================

price_gap = (
    our_average_price
    - competitor_average_price
)


price_gap_percent = (
    price_gap
    / competitor_average_price
) * 100


# ============================================================
# MARKET POSITION
# ============================================================

if price_gap_percent > 5:

    market_position = "Above Market"

elif price_gap_percent < -5:

    market_position = "Below Market"

else:

    market_position = "Near Market"


# ============================================================
# ANALYSIS RESULT
# ============================================================

result = pd.DataFrame([
    {
        "Category": "Sports",

        "Our_Average_Price":
            round(
                our_average_price,
                2
            ),

        "Competitor":
            "Decathlon",

        "Competitor_Average_Price":
            round(
                competitor_average_price,
                2
            ),

        "Competitor_Min_Price":
            round(
                competitor_min_price,
                2
            ),

        "Competitor_Max_Price":
            round(
                competitor_max_price,
                2
            ),

        "Price_Gap":
            round(
                price_gap,
                2
            ),

        "Price_Gap_Percent":
            round(
                price_gap_percent,
                2
            ),

        "Market_Position":
            market_position,

        "Our_Average_Demand":
            round(
                our_average_demand,
                2
            ),

        "Competitor_Average_Discount":
            round(
                average_competitor_discount,
                2
            )
    }
])


# ============================================================
# SAVE
# ============================================================

result.to_csv(
    OUTPUT_DATA,
    index=False
)


# ============================================================
# DISPLAY
# ============================================================

print("\n========================================")
print("COMPETITOR ANALYSIS")
print("========================================")

print(
    result.to_string(
        index=False
    )
)

print("\nSaved at:")

print(
    os.path.abspath(
        OUTPUT_DATA
    )
)