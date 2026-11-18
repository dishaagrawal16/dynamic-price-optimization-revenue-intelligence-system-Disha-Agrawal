import os
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime


# ============================================================
# CONFIGURATION
# ============================================================

URL = "https://www.decathlon.in/c/24055"

COMPETITOR = "Decathlon"
CATEGORY = "Sports"


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

OUTPUT_PATH = os.path.join(
    DATA_DIR,
    "competitor_prices.csv"
)


# ============================================================
# FETCH PAGE
# ============================================================

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    )
}

print("Fetching competitor page...")

response = requests.get(
    URL,
    headers=headers,
    timeout=20
)

print("Status Code:", response.status_code)

if response.status_code != 200:
    print("❌ Unable to access competitor page.")
    exit()


# ============================================================
# PARSE PAGE
# ============================================================

soup = BeautifulSoup(
    response.text,
    "html.parser"
)

text = soup.get_text(
    " ",
    strip=True
)

print("Response text length:", len(text))


# ============================================================
# SPLIT PRODUCTS
# ============================================================

product_sections = text.split("Add to cart")

print(
    "Product sections detected:",
    len(product_sections)
)


products = []


# ============================================================
# EXTRACT PRICE + MRP
# ============================================================

for section in product_sections:

    # We intentionally IGNORE the rupee symbol.
    #
    # Examples:
    #
    # 99 MRP 299
    # 5,999 MRP 8,999
    # 399 MRP 649
    #
    price_pattern = re.search(
        r"([\d,]+)\s+MRP\s*[^\d]*([\d,]+)",
        section
    )

    if not price_pattern:
        continue


    competitor_price = float(
        price_pattern.group(1).replace(",", "")
    )

    mrp = float(
        price_pattern.group(2).replace(",", "")
    )


    # ========================================================
    # GET PRODUCT NAME
    # ========================================================

    before_price = section[
        :price_pattern.start()
    ].strip()


    # Remove page/header text
    if "Explore all our collections" in before_price:

        before_price = before_price.split(
            "Explore all our collections"
        )[-1].strip()


    # Remove rating such as:
    #
    # 7.0k
    # 4.9k
    # 3.0k +6
    #
    before_price = re.sub(
        r"\s+\d+(?:\.\d+)?k(?:\s*\+\d+)?\s*$",
        "",
        before_price
    ).strip()


    # Remove trailing rupee/encoding garbage
    before_price = re.sub(
        r"[^A-Za-z0-9)\]}'\"&%:/,\- ]+$",
        "",
        before_price
    ).strip()


    product_name = before_price


    # ========================================================
    # VALIDATION
    # ========================================================

    if len(product_name) < 5:
        continue

    if competitor_price <= 0:
        continue

    if mrp <= 0:
        continue


    # ========================================================
    # STORE
    # ========================================================

    products.append({
        "Category": CATEGORY,
        "Competitor": COMPETITOR,
        "Product_Name": product_name,
        "Competitor_Price": competitor_price,
        "MRP": mrp,
        "Source": URL,
        "Scraped_At": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    })


# ============================================================
# CREATE DATAFRAME
# ============================================================

df = pd.DataFrame(products)


if df.empty:

    print("\n❌ No products extracted.")

    print("\nDebug: checking numeric MRP patterns...")

    matches = re.findall(
        r"([\d,]+)\s+MRP\s*[^\d]*([\d,]+)",
        text
    )

    print(
        "Price/MRP pairs found:",
        len(matches)
    )

    print(
        "First 10 pairs:",
        matches[:10]
    )

    exit()


# ============================================================
# REMOVE DUPLICATES
# ============================================================

df = df.drop_duplicates(
    subset=[
        "Product_Name",
        "Competitor_Price"
    ]
)


# ============================================================
# SAVE
# ============================================================

df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ============================================================
# RESULTS
# ============================================================

print("\n========================================")
print("COMPETITOR MONITORING SUCCESSFUL")
print("========================================")

print(
    "Products extracted:",
    len(df)
)

print("\nSample products:")

print(
    df.head(10).to_string(
        index=False
    )
)

print("\n========================================")
print("PRICE STATISTICS")
print("========================================")

print(
    "Average Price:",
    round(
        df["Competitor_Price"].mean(),
        2
    )
)

print(
    "Minimum Price:",
    df["Competitor_Price"].min()
)

print(
    "Maximum Price:",
    df["Competitor_Price"].max()
)

print(
    "Average MRP:",
    round(
        df["MRP"].mean(),
        2
    )
)

print("\nSaved at:")

print(
    os.path.abspath(OUTPUT_PATH)
)