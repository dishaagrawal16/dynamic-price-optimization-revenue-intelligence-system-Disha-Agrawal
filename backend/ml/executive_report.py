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

PROFITABILITY_PATH = os.path.join(
    DATA_DIR,
    "profitability_analysis.csv"
)

MARKET_PATH = os.path.join(
    DATA_DIR,
    "market_intelligence.csv"
)

PRICING_PATH = os.path.join(
    DATA_DIR,
    "pricing_strategy_recommendations.csv"
)

OUTPUT_PATH = os.path.join(
    DATA_DIR,
    "executive_business_report.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("Loading profitability data...")

profitability = pd.read_csv(
    PROFITABILITY_PATH
)

print(
    "Profitability rows:",
    len(profitability)
)


print("\nLoading market intelligence data...")

market = pd.read_csv(
    MARKET_PATH
)

print(
    "Market intelligence rows:",
    len(market)
)


print("\nLoading pricing strategy data...")

pricing = pd.read_csv(
    PRICING_PATH
)

print(
    "Pricing recommendation rows:",
    len(pricing)
)


# ============================================================
# MERGE BUSINESS DATA
# ============================================================

report = profitability.merge(
    market[
        [
            "Category_Name",
            "Competitor_Average_Price",
            "Price_Gap_Percent",
            "Market_Position",
            "Competitive_Pressure",
            "Market_Opportunity",
            "Market_Insight"
        ]
    ],
    on="Category_Name",
    how="left"
)


report = report.merge(
    pricing[
        [
            "Category",
            "Priority",
            "Pricing_Recommendation"
        ]
    ],
    left_on="Category_Name",
    right_on="Category",
    how="left"
)


report.drop(
    columns=["Category"],
    inplace=True
)


# ============================================================
# EXECUTIVE STATUS
# ============================================================

def determine_status(row):

    priority = row["Priority"]

    profitability_level = (
        row["Profitability_Level"]
    )

    market_position = (
        row["Market_Position"]
    )

    if (
        priority == "High"
        and profitability_level == "High"
    ):
        return "Action Required"

    elif (
        priority == "Medium"
    ):
        return "Monitor"

    elif (
        market_position == "No competitor data"
    ):
        return "Data Required"

    elif (
        market_position ==
        "Insufficient Comparable Data"
    ):
        return "Data Validation Required"

    else:
        return "Stable"


report["Executive_Status"] = (
    report.apply(
        determine_status,
        axis=1
    )
)


# ============================================================
# EXECUTIVE PRIORITY
# ============================================================

def determine_priority(row):

    if row["Priority"] == "High":
        return 1

    elif row["Priority"] == "Medium":
        return 2

    return 3


report["Priority_Order"] = (
    report.apply(
        determine_priority,
        axis=1
    )
)


# ============================================================
# SELECT EXECUTIVE COLUMNS
# ============================================================

executive_columns = [

    "Category_Name",

    "Total_Demand",

    "Total_Revenue",

    "Estimated_Cost",

    "Estimated_Profit",

    "Estimated_Profit_Margin",

    "Profitability_Level",

    "Competitor_Average_Price",

    "Price_Gap_Percent",

    "Market_Position",

    "Competitive_Pressure",

    "Market_Opportunity",

    "Priority",

    "Executive_Status",

    "Pricing_Recommendation",

    "Market_Insight"

]


report = report[
    executive_columns
]


# ============================================================
# ROUND NUMERIC VALUES
# ============================================================

numeric_columns = [

    "Total_Demand",

    "Total_Revenue",

    "Estimated_Cost",

    "Estimated_Profit",

    "Estimated_Profit_Margin",

    "Competitor_Average_Price",

    "Price_Gap_Percent"

]


report[numeric_columns] = (
    report[numeric_columns]
    .round(2)
)


# ============================================================
# SORT BY PRIORITY / PROFIT
# ============================================================

priority_order = {
    "High": 1,
    "Medium": 2,
    "Low": 3
}


report["_priority"] = (
    report["Priority"]
    .map(priority_order)
)


report = (
    report
    .sort_values(
        [
            "_priority",
            "Estimated_Profit"
        ],
        ascending=[
            True,
            False
        ]
    )
    .drop(
        columns=["_priority"]
    )
    .reset_index(
        drop=True
    )
)


# ============================================================
# SAVE CATEGORY REPORT
# ============================================================

report.to_csv(
    OUTPUT_PATH,
    index=False
)


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

total_revenue = (
    report["Total_Revenue"]
    .sum()
)

estimated_profit = (
    report["Estimated_Profit"]
    .sum()
)

estimated_cost = (
    report["Estimated_Cost"]
    .sum()
)

profit_margin = (
    estimated_profit
    /
    total_revenue
    * 100
)


most_profitable = report.loc[
    report["Estimated_Profit"].idxmax(),
    "Category_Name"
]


high_priority_count = (
    report["Priority"]
    .eq("High")
    .sum()
)


data_required_count = (
    report["Executive_Status"]
    .isin(
        [
            "Data Required",
            "Data Validation Required"
        ]
    )
    .sum()
)


# ============================================================
# DISPLAY
# ============================================================

print("\n")
print("=" * 60)
print("EXECUTIVE BUSINESS INTELLIGENCE REPORT")
print("=" * 60)


print(
    "\nTotal Revenue:",
    f"₹{total_revenue:,.2f}"
)


print(
    "Estimated Cost:",
    f"₹{estimated_cost:,.2f}"
)


print(
    "Estimated Profit:",
    f"₹{estimated_profit:,.2f}"
)


print(
    "Estimated Profit Margin:",
    f"{profit_margin:.2f}%"
)


print(
    "Most Profitable Category:",
    most_profitable
)


print(
    "High Priority Actions:",
    high_priority_count
)


print(
    "Categories Requiring Better Data:",
    data_required_count
)


print("\nCategory Executive Summary:")


print(
    report[
        [
            "Category_Name",
            "Estimated_Profit",
            "Estimated_Profit_Margin",
            "Market_Position",
            "Priority",
            "Executive_Status"
        ]
    ].to_string(
        index=False
    )
)


print("\nSaved at:")

print(
    os.path.abspath(
        OUTPUT_PATH
    )
)