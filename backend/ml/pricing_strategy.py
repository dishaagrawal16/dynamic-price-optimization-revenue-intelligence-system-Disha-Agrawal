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

MARKET_INTELLIGENCE_PATH = os.path.join(
    DATA_DIR,
    "market_intelligence.csv"
)

OUTPUT_PATH = os.path.join(
    DATA_DIR,
    "pricing_strategy_recommendations.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("Loading profitability data...")

profitability = pd.read_csv(
    PROFITABILITY_PATH
)

print(
    "Profitability dataset shape:",
    profitability.shape
)


print("\nLoading market intelligence data...")

market = pd.read_csv(
    MARKET_INTELLIGENCE_PATH
)

print(
    "Market intelligence dataset shape:",
    market.shape
)

# Create a category-level lookup for efficient market data access
market_lookup = (
    market
    .drop_duplicates(subset=["Category_Name"])
    .set_index("Category_Name")
    .to_dict("index")
)

# ============================================================
# CATEGORY-LEVEL RECOMMENDATIONS
# ============================================================

recommendations = []


for _, row in profitability.iterrows():

    category = row["Category_Name"]

    avg_price = row["Average_Final_Price"]

    avg_demand = row["Average_Demand"]

    total_revenue = row["Total_Revenue"]

    discount = row["Average_Discount"]

    profit_margin = row.get(
        "Estimated_Profit_Margin",
        None
    )


    # --------------------------------------------------------
    # DEFAULT VALUES
    # --------------------------------------------------------

    market_position = "No competitor data"

    price_gap_percent = None

    recommendation = (
        "Competitor pricing data is unavailable. "
        "Monitor category performance."
    )

    priority = "Low"


    # --------------------------------------------------------
    # FIND MARKET INTELLIGENCE DATA
    # --------------------------------------------------------

    market_row = market_lookup.get(category)
    
    if market_row is not None:
    
        market_position = (
            market_row["Market_Position"]
        )
    
        price_gap_percent = (
            market_row["Price_Gap_Percent"]
        )


        # ====================================================
        # NO COMPETITOR DATA
        # ====================================================

        if market_position == "No competitor data":

            recommendation = (
                "Competitor pricing data is unavailable "
                "for this category. Monitor demand, "
                "revenue and profitability."
            )

            priority = "Low"


        # ====================================================
        # INSUFFICIENT COMPARABLE DATA
        # ====================================================

        elif market_position == "Insufficient Comparable Data":

            recommendation = (
                "Competitor pricing data is not "
                "comparable for this category. "
                "Do not make automated pricing changes "
                "until reliable competitor data is available."
            )

            priority = "Low"


        # ====================================================
        # BELOW COMPETITOR
        # ====================================================

        elif market_position == "Below Competitor":

            if (
                price_gap_percent <= -50
                and avg_demand >= 130
            ):

                recommendation = (
                    "Our price is substantially below "
                    "the observed competitor level while "
                    "demand remains healthy. Consider a "
                    "controlled upward price adjustment "
                    "and monitor demand response."
                )

                priority = "High"


            elif (
                price_gap_percent <= -20
                and avg_demand >= 120
            ):

                recommendation = (
                    "Our price is below the observed "
                    "competitor level and demand is "
                    "relatively healthy. Consider a "
                    "gradual price increase while "
                    "monitoring demand."
                )

                priority = "Medium"


            else:

                recommendation = (
                    "Our price is below the observed "
                    "competitor level. Monitor demand "
                    "before making pricing changes."
                )

                priority = "Medium"


        # ====================================================
        # ABOVE COMPETITOR
        # ====================================================

        elif market_position == "Above Competitor":

            if avg_demand < 130:

                recommendation = (
                    "Our price is above the observed "
                    "competitor level while demand is "
                    "relatively low. Consider a controlled "
                    "price reduction or targeted discount."
                )

                priority = "High"

            else:

                recommendation = (
                    "Our price is above the observed "
                    "competitor level but demand remains "
                    "healthy. Monitor price sensitivity "
                    "before making changes."
                )

                priority = "Medium"


        # ====================================================
        # COMPETITIVE
        # ====================================================

        elif market_position == "Competitive":

            recommendation = (
                "Our pricing is relatively close to the "
                "observed competitor level. Maintain "
                "competitive pricing and optimize "
                "discounts based on demand."
            )

            priority = "Low"


    # ========================================================
    # DISCOUNT CONSIDERATION
    # ========================================================

    if discount >= 20:

        recommendation += (
            " Current discount levels are already "
            "relatively high, so avoid broad additional "
            "discounting."
        )


    # ========================================================
    # PROFITABILITY CONSIDERATION
    # ========================================================

    if (
        profit_margin is not None
        and not pd.isna(profit_margin)
    ):

        if profit_margin >= 35:

            recommendation += (
                " Estimated profitability margin is "
                "strong, supporting cautious price "
                "optimization."
            )

        elif profit_margin < 25:

            recommendation += (
                " Estimated profitability margin is "
                "relatively low, so pricing changes "
                "should be approached cautiously."
            )


    # ========================================================
    # STORE RESULT
    # ========================================================

    recommendations.append({

        "Category":
            category,

        "Average_Final_Price":
            round(
                avg_price,
                2
            ),

        "Average_Demand":
            round(
                avg_demand,
                2
            ),

        "Total_Revenue":
            round(
                total_revenue,
                2
            ),

        "Average_Discount":
            round(
                discount,
                2
            ),

        "Estimated_Profit_Margin":
            (
                round(
                    profit_margin,
                    2
                )
                if profit_margin is not None
                else None
            ),

        "Market_Position":
            market_position,

        "Price_Gap_Percent":
            (
                round(
                    price_gap_percent,
                    2
                )
                if not pd.isna(price_gap_percent)
                else None
            ),

        "Priority":
            priority,

        "Pricing_Recommendation":
            recommendation
    })


# ============================================================
# CREATE DATAFRAME
# ============================================================

result = pd.DataFrame(
    recommendations
)

# ============================================================
# RECOMMENDATION QUALITY VALIDATION
# ============================================================

print("\n========================================")
print("RECOMMENDATION QUALITY VALIDATION")
print("========================================")

validation_results = []

for _, row in result.iterrows():

    category = row["Category"]

    market_position = row["Market_Position"]

    price_gap = row["Price_Gap_Percent"]

    priority = row["Priority"]

    recommendation = row["Pricing_Recommendation"]

    validation_status = "PASS"

    validation_reason = ""


    # --------------------------------------------------------
    # RULE 1 — No competitor data
    # --------------------------------------------------------

    if market_position == "No competitor data":

        if price_gap is not None and not pd.isna(price_gap):

            validation_status = "FAIL"

            validation_reason = (
                "Price gap should not exist when "
                "competitor data is unavailable."
            )

        elif priority != "Low":

            validation_status = "FAIL"

            validation_reason = (
                "Priority should be Low when "
                "competitor data is unavailable."
            )

        else:

            validation_reason = (
                "No competitor data correctly results "
                "in a monitoring recommendation."
            )


    # --------------------------------------------------------
    # RULE 2 — Insufficient comparable data
    # --------------------------------------------------------

    elif market_position == "Insufficient Comparable Data":

        if priority != "Low":

            validation_status = "FAIL"

            validation_reason = (
                "Priority should be Low when "
                "competitor data is not comparable."
            )

        elif (
            "Do not make automated pricing changes"
            not in recommendation
        ):

            validation_status = "FAIL"

            validation_reason = (
                "Recommendation should prevent "
                "automated pricing changes."
            )

        else:

            validation_reason = (
                "Insufficient comparable data correctly "
                "prevents automated pricing changes."
            )


    # --------------------------------------------------------
    # RULE 3 — Below competitor
    # --------------------------------------------------------

    elif market_position == "Below Competitor":

        if price_gap is None or pd.isna(price_gap):

            validation_status = "FAIL"

            validation_reason = (
                "Below Competitor requires a valid "
                "price gap percentage."
            )

        elif price_gap > 0:

            validation_status = "FAIL"

            validation_reason = (
                "Price gap should be negative when "
                "our price is below competitor."
            )

        else:

            validation_reason = (
                "Below-competitor recommendation is "
                "consistent with the negative price gap."
            )


    # --------------------------------------------------------
    # RULE 4 — Above competitor
    # --------------------------------------------------------

    elif market_position == "Above Competitor":

        if price_gap is None or pd.isna(price_gap):

            validation_status = "FAIL"

            validation_reason = (
                "Above Competitor requires a valid "
                "price gap percentage."
            )

        elif price_gap < 0:

            validation_status = "FAIL"

            validation_reason = (
                "Price gap should be positive when "
                "our price is above competitor."
            )

        else:

            validation_reason = (
                "Above-competitor recommendation is "
                "consistent with the positive price gap."
            )


    # --------------------------------------------------------
    # RULE 5 — Competitive pricing
    # --------------------------------------------------------

    elif market_position == "Competitive":

        validation_reason = (
            "Competitive pricing correctly results "
            "in a maintenance/optimization recommendation."
        )


    # --------------------------------------------------------
    # UNKNOWN MARKET POSITION
    # --------------------------------------------------------

    else:

        validation_status = "FAIL"

        validation_reason = (
            "Unknown market position detected."
        )


    validation_results.append({

        "Category":
            category,

        "Market_Position":
            market_position,

        "Price_Gap_Percent":
            price_gap,

        "Priority":
            priority,

        "Validation_Status":
            validation_status,

        "Validation_Reason":
            validation_reason
    })


validation_df = pd.DataFrame(
    validation_results
)


# ============================================================
# VALIDATION SUMMARY
# ============================================================

total_recommendations = len(
    validation_df
)

passed_recommendations = len(
    validation_df[
        validation_df["Validation_Status"] == "PASS"
    ]
)

failed_recommendations = len(
    validation_df[
        validation_df["Validation_Status"] == "FAIL"
    ]
)

validation_rate = (
    passed_recommendations
    / total_recommendations
    * 100
    if total_recommendations > 0
    else 0
)


print("\nTotal Recommendations:",
      total_recommendations)

print("Passed:",
      passed_recommendations)

print("Failed:",
      failed_recommendations)

print(
    "Validation Rate:",
    round(validation_rate, 2),
    "%"
)


print("\nValidation Details:")

print(
    validation_df.to_string(
        index=False
    )
)


# ============================================================
# SAVE VALIDATION RESULTS
# ============================================================

VALIDATION_PATH = os.path.join(
    DATA_DIR,
    "pricing_recommendation_validation.csv"
)

validation_df.to_csv(
    VALIDATION_PATH,
    index=False
)

print("\nValidation results saved at:")

print(
    os.path.abspath(
        VALIDATION_PATH
    )
)


# ============================================================
# SAVE
# ============================================================

result.to_csv(
    OUTPUT_PATH,
    index=False
)


# ============================================================
# DISPLAY
# ============================================================

print("\n========================================")
print("PRICING STRATEGY RECOMMENDATIONS")
print("========================================")

print(
    result.to_string(
        index=False
    )
)

print("\nSaved at:")

print(
    os.path.abspath(
        OUTPUT_PATH
    )
)