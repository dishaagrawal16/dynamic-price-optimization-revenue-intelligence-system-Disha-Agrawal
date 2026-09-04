import time
import requests


BASE_URL = "http://127.0.0.1:8000"


# ============================================================
# PERFORMANCE TEST HELPER
# ============================================================

def measure_endpoint(
    name,
    endpoint,
    method="GET"
):

    url = BASE_URL + endpoint

    try:

        start_time = time.perf_counter()

        if method == "GET":

            response = requests.get(url)

        elif method == "POST":

            response = requests.post(url)

        else:

            print(
                f"❌ {name}: Unsupported method"
            )

            return None

        end_time = time.perf_counter()

        response_time = (
            end_time - start_time
        ) * 1000

        if response.status_code == 200:

            print(
                f"✅ {name:<40}"
                f"{response_time:>10.2f} ms"
            )

            return response_time

        else:

            print(
                f"❌ {name:<40}"
                f"HTTP {response.status_code}"
            )

            return None

    except Exception as e:

        print(
            f"❌ {name}: {str(e)}"
        )

        return None


# ============================================================
# PERFORMANCE TEST
# ============================================================

print("\n========================================")
print("PRICEPILOT API PERFORMANCE TEST")
print("========================================\n")


results = {}


# ============================================================
# DASHBOARD
# ============================================================

results["Dashboard Summary"] = measure_endpoint(
    "Dashboard Summary",
    "/dashboard/summary"
)

results["Monthly Revenue"] = measure_endpoint(
    "Monthly Revenue",
    "/dashboard/monthly-revenue"
)

results["Category Revenue"] = measure_endpoint(
    "Category Revenue",
    "/dashboard/category-revenue"
)

results["Recent Products"] = measure_endpoint(
    "Recent Products",
    "/dashboard/recent-products"
)

results["Payment Distribution"] = measure_endpoint(
    "Payment Distribution",
    "/dashboard/payment-distribution"
)


# ============================================================
# PREDICTION & FORECAST
# ============================================================

results["Demand Forecast"] = measure_endpoint(
    "Demand Forecast",
    "/forecast/demand"
)


# ============================================================
# COMPETITOR ANALYSIS
# ============================================================

results["Competitor Summary"] = measure_endpoint(
    "Competitor Summary",
    "/competitor/summary"
)

results["Competitor Comparison"] = measure_endpoint(
    "Competitor Comparison",
    "/competitor/comparison"
)

results["Competitor Products"] = measure_endpoint(
    "Competitor Products",
    "/competitor/products"
)

results["Category Competitor Prices"] = measure_endpoint(
    "Category Competitor Prices",
    "/competitor/category-prices"
)

results["Market Intelligence"] = measure_endpoint(
    "Market Intelligence",
    "/competitor/market-intelligence"
)


# ============================================================
# PROFITABILITY
# ============================================================

results["Profitability Summary"] = measure_endpoint(
    "Profitability Summary",
    "/profitability/summary"
)

results["Profitability Category Analysis"] = measure_endpoint(
    "Profitability Category Analysis",
    "/profitability/category-analysis"
)


# ============================================================
# PRICING STRATEGY
# ============================================================

results["Pricing Recommendations"] = measure_endpoint(
    "Pricing Recommendations",
    "/pricing-strategy/recommendations"
)


# ============================================================
# EXECUTIVE REPORT
# ============================================================

results["Executive Report Summary"] = measure_endpoint(
    "Executive Report Summary",
    "/executive-report/summary"
)

results["Executive Report Category Analysis"] = measure_endpoint(
    "Executive Report Category Analysis",
    "/executive-report/category-analysis"
)


# ============================================================
# PERFORMANCE SUMMARY
# ============================================================

valid_results = [
    value
    for value in results.values()
    if value is not None
]


print("\n========================================")
print("PERFORMANCE SUMMARY")
print("========================================")

if valid_results:

    average_time = (
        sum(valid_results)
        / len(valid_results)
    )

    fastest_time = min(
        valid_results
    )

    slowest_time = max(
        valid_results
    )

    print(
        "Endpoints Tested :",
        len(valid_results)
    )

    print(
        "Average Response :",
        round(average_time, 2),
        "ms"
    )

    print(
        "Fastest Response :",
        round(fastest_time, 2),
        "ms"
    )

    print(
        "Slowest Response :",
        round(slowest_time, 2),
        "ms"
    )

else:

    print(
        "No successful endpoints measured."
    )


print("\n========================================")
print("PERFORMANCE TEST COMPLETE")
print("========================================")