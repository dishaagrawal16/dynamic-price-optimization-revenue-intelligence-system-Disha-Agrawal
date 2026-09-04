import requests

BASE_URL = "http://127.0.0.1:8000"

TEST_USERNAME = "aman"
TEST_PASSWORD = "aman123"
TEST_ROLE = "business_analyst"

# ============================================================
# AUTHENTICATION
# ============================================================

def get_access_token():

    url = BASE_URL + "/auth/login"

    payload = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD,
        "role": TEST_ROLE
    }

    try:

        response = requests.post(
            url,
            json=payload
        )

        if response.status_code != 200:

            print(
                "❌ Authentication failed"
            )

            print(
                "Response:",
                response.text
            )

            return None

        data = response.json()

        token = data.get(
            "access_token"
        )

        if not token:

            print(
                "❌ Authentication succeeded "
                "but access token was not returned."
            )

            return None

        print(
            "✅ Authentication: PASS (200)"
        )

        return token

    except requests.exceptions.ConnectionError:

        print(
            "❌ Authentication: Backend is not running"
        )

        return None

    except Exception as e:

        print(
            "❌ Authentication:",
            str(e)
        )

        return None


# ============================================================
# AUTHENTICATED API TEST
# ============================================================

def test_authenticated_endpoint(
    name,
    endpoint,
    token,
    expected_status=200
):

    url = BASE_URL + endpoint

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:

        response = requests.get(
            url,
            headers=headers
        )

        if response.status_code == expected_status:

            print(
                f"✅ {name}: PASS "
                f"({response.status_code})"
            )

            return True

        else:

            print(
                f"❌ {name}: FAIL "
                f"(Expected {expected_status}, "
                f"Got {response.status_code})"
            )

            print(
                "Response:",
                response.text[:300]
            )

            return False

    except Exception as e:

        print(
            f"❌ {name}: {str(e)}"
        )

        return False

# ============================================================
# POST API TEST
# ============================================================

def test_post_endpoint(
    name,
    endpoint,
    payload,
    expected_status=200
):

    url = BASE_URL + endpoint

    try:

        response = requests.post(
            url,
            json=payload
        )

        if response.status_code == expected_status:

            print(
                f"✅ {name}: PASS "
                f"({response.status_code})"
            )

            return True

        else:

            print(
                f"❌ {name}: FAIL "
                f"(Expected {expected_status}, "
                f"Got {response.status_code})"
            )

            print(
                "Response:",
                response.text[:500]
            )

            return False

    except Exception as e:

        print(
            f"❌ {name}: {str(e)}"
        )

        return False

# ============================================================
# API TEST HELPER
# ============================================================

def test_endpoint(
    name,
    method,
    endpoint,
    expected_status=200
):

    url = BASE_URL + endpoint

    try:

        if method == "GET":
            response = requests.get(url)

        elif method == "POST":
            response = requests.post(url)

        else:
            print(
                f"❌ {name}: Unsupported HTTP method"
            )
            return False

        if response.status_code == expected_status:

            print(
                f"✅ {name}: PASS "
                f"({response.status_code})"
            )

            return True

        else:

            print(
                f"❌ {name}: FAIL "
                f"(Expected {expected_status}, "
                f"Got {response.status_code})"
            )

            print(
                "Response:",
                response.text[:300]
            )

            return False

    except requests.exceptions.ConnectionError:

        print(
            f"❌ {name}: Backend is not running"
        )

        return False

    except Exception as e:

        print(
            f"❌ {name}: {str(e)}"
        )

        return False


# ============================================================
# MAIN API TESTS
# ============================================================

print("\n========================================")
print("PRICEPILOT API VALIDATION")
print("========================================\n")


results = []


# ------------------------------------------------------------
# BASIC BACKEND
# ------------------------------------------------------------

results.append(
    test_endpoint(
        "Backend Root",
        "GET",
        "/"
    )
)


results.append(
    test_endpoint(
        "Database Connection",
        "GET",
        "/test-db"
    )
)


# ------------------------------------------------------------
# DASHBOARD
# ------------------------------------------------------------

results.append(
    test_endpoint(
        "Dashboard Summary",
        "GET",
        "/dashboard/summary"
    )
)


results.append(
    test_endpoint(
        "Monthly Revenue",
        "GET",
        "/dashboard/monthly-revenue"
    )
)


results.append(
    test_endpoint(
        "Category Revenue",
        "GET",
        "/dashboard/category-revenue"
    )
)


results.append(
    test_endpoint(
        "Recent Products",
        "GET",
        "/dashboard/recent-products"
    )
)


results.append(
    test_endpoint(
        "Payment Distribution",
        "GET",
        "/dashboard/payment-distribution"
    )
)

# ============================================================
# PRICE PREDICTION
# ============================================================

prediction_payload = {
    "category": 0,
    "original_price": 500,
    "discount": 10,
    "payment_method": 1,
    "year": 2024,
    "month": 6,
    "day": 15
}

results.append(
    test_post_endpoint(
        "Price Prediction",
        "/prediction/predict-price",
        prediction_payload
    )
)

# ============================================================
# DEMAND FORECAST
# ============================================================

results.append(
    test_endpoint(
        "Demand Forecast",
        "GET",
        "/forecast/demand"
    )
)

# ============================================================
# COMPETITOR ANALYSIS
# ============================================================

results.append(
    test_endpoint(
        "Competitor Summary",
        "GET",
        "/competitor/summary"
    )
)

results.append(
    test_endpoint(
        "Competitor Comparison",
        "GET",
        "/competitor/comparison"
    )
)

results.append(
    test_endpoint(
        "Competitor Products",
        "GET",
        "/competitor/products"
    )
)

results.append(
    test_endpoint(
        "Category Competitor Prices",
        "GET",
        "/competitor/category-prices"
    )
)

results.append(
    test_endpoint(
        "Market Intelligence",
        "GET",
        "/competitor/market-intelligence"
    )
)

# ------------------------------------------------------------
# PRODUCTS
# ------------------------------------------------------------

# ============================================================
# AUTHENTICATED PRODUCTS API
# ============================================================

token = get_access_token()

if token:

    results.append(
        test_authenticated_endpoint(
            "Products API",
            "/products",
            token
        )
    )

else:

    results.append(False)


# ------------------------------------------------------------
# PROFITABILITY
# ------------------------------------------------------------

results.append(
    test_endpoint(
        "Profitability Summary",
        "GET",
        "/profitability/summary"
    )
)

results.append(
    test_endpoint(
        "Profitability Category Analysis",
        "GET",
        "/profitability/category-analysis"
    )
)


# ------------------------------------------------------------
# PRICING STRATEGY
# ------------------------------------------------------------

results.append(
    test_endpoint(
        "Pricing Strategy Recommendations",
        "GET",
        "/pricing-strategy/recommendations"
    )
)


# ------------------------------------------------------------
# EXECUTIVE REPORT
# ------------------------------------------------------------

results.append(
    test_endpoint(
        "Executive Report Summary",
        "GET",
        "/executive-report/summary"
    )
)

results.append(
    test_endpoint(
        "Executive Report Category Analysis",
        "GET",
        "/executive-report/category-analysis"
    )
)


# ============================================================
# SUMMARY
# ============================================================

passed = sum(results)

total = len(results)

failed = total - passed

success_rate = (
    passed / total * 100
    if total > 0
    else 0
)


print("\n========================================")
print("API VALIDATION SUMMARY")
print("========================================")

print("Total Tests :", total)

print("Passed      :", passed)

print("Failed      :", failed)

print(
    "Success Rate:",
    round(success_rate, 2),
    "%"
)


if failed == 0:

    print(
        "\n🎉 All tested APIs are working successfully!"
    )

else:

    print(
        "\n⚠️ Some APIs require investigation."
    )