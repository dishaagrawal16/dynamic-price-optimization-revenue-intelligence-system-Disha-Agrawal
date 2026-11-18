import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

OUTPUT_PATH = os.path.join(
    DATA_DIR,
    "competitor_prices_multi.csv"
)


# ============================================================
# COMPETITOR SOURCES
# ============================================================

SOURCES = {

    "Beauty": {
        "competitor": "Nykaa",
        "url": "https://www.nykaa.com/nykaa-beauty-store/c/2"
    },

    "Clothing": {
        "competitor": "Myntra",
        "url": "https://www.myntra.com/dresses"
    }

}


# ============================================================
# HEADERS
# ============================================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    ),

    "Accept-Language": "en-IN,en;q=0.9"
}


# ============================================================
# GENERIC PRICE EXTRACTION
# ============================================================

def extract_price(text):

    # Remove commas
    text = text.replace(",", "")

    # Look for Rs. / ₹ followed by price
    match = re.search(
        r"(?:₹|Rs\.?|INR)\s*([0-9]+(?:\.[0-9]+)?)",
        text,
        re.IGNORECASE
    )

    if match:
        return float(match.group(1))

    return None


# ============================================================
# NYKAA SCRAPER
# ============================================================

def scrape_nykaa(url):

    print("\n----------------------------------------")
    print("Scraping Nykaa")
    print("----------------------------------------")

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    print(
        "Status Code:",
        response.status_code
    )

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    products = []

    # ========================================================
    # SEARCH PRODUCT-LIKE ELEMENTS
    # ========================================================

    elements = soup.find_all(
        ["div", "li", "article"]
    )

    seen = set()

    for element in elements:

        text = element.get_text(
            " ",
            strip=True
        )

        if not text:
            continue

        # Ignore huge page-level containers
        if len(text) > 600:
            continue

        # Need at least one rupee price
        prices = re.findall(
            r"₹\s*([\d,]+(?:\.\d+)?)",
            text
        )

        if not prices:
            continue

        # Need a reasonable amount of text
        if len(text) < 15:
            continue

        # ====================================================
        # CLEAN PRICE LIST
        # ====================================================

        numeric_prices = []

        for price in prices:

            try:

                value = float(
                    price.replace(",", "")
                )

                numeric_prices.append(
                    value
                )

            except ValueError:
                continue

        if not numeric_prices:
            continue


        # ====================================================
        # PRODUCT NAME
        # ====================================================

        product_name = text

        # Remove badges
        product_name = re.sub(
            r"\bBESTSELLER\b",
            "",
            product_name,
            flags=re.IGNORECASE
        )

        product_name = re.sub(
            r"\bAD\b",
            "",
            product_name,
            flags=re.IGNORECASE
        )

        # Remove price section
        product_name = re.split(
            r"₹",
            product_name
        )[0]

        product_name = product_name.strip()


        # Remove rating/review information
        product_name = re.sub(
            r"\(\s*[\d,]+\s*\).*",
            "",
            product_name
        )

        # Remove wishlist/preview text
        product_name = re.split(
            r"Wishlist|Preview|Add to Bag",
            product_name,
            flags=re.IGNORECASE
        )[0]

        product_name = product_name.strip()


        # ====================================================
        # VALIDATE PRODUCT NAME
        # ====================================================

        if len(product_name) < 8:
            continue

        if len(product_name) > 250:
            continue

        # Avoid navigation/category text
        blocked_terms = [
            "Price List",
            "All Products",
            "Beauty Store",
            "Top Brands",
            "Wishlist",
            "Filters",
            "Sort By"
        ]

        if any(
            term.lower() in product_name.lower()
            for term in blocked_terms
        ):
            continue


        # ====================================================
        # PRICE LOGIC
        # ====================================================

        if len(numeric_prices) >= 2:

            mrp = numeric_prices[0]

            competitor_price = numeric_prices[1]

        else:

            mrp = numeric_prices[0]

            competitor_price = numeric_prices[0]


        # ====================================================
        # DUPLICATE CONTROL
        # ====================================================

        key = (
            product_name.lower(),
            competitor_price
        )

        if key in seen:
            continue

        seen.add(key)


        # ====================================================
        # SAVE
        # ====================================================

        products.append({

            "Category":
                "Beauty",

            "Competitor":
                "Nykaa",

            "Product_Name":
                product_name,

            "Competitor_Price":
                competitor_price,

            "MRP":
                mrp,

            "Source":
                url,

            "Scraped_At":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
        })


    return products

# ============================================================
# MYNTRA SCRAPER
# ============================================================

def scrape_myntra(url):

    print("\n----------------------------------------")
    print("Scraping Myntra")
    print("----------------------------------------")

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    print(
        "Status Code:",
        response.status_code
    )

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    products = []

    # ========================================================
    # METHOD 1: PRODUCT BASE CONTAINERS
    # ========================================================

    elements = soup.select(
        "li.product-base"
    )

    print(
        "Product containers found:",
        len(elements)
    )

    for element in elements:

        text = element.get_text(
            " ",
            strip=True
        )

        if not text:
            continue

        if len(text) < 10:
            continue

        # ----------------------------------------------------
        # Find rupee prices
        # ----------------------------------------------------

        prices = re.findall(
            r"(?:₹|Rs\.?)\s*([\d,]+)",
            text,
            re.IGNORECASE
        )

        if not prices:
            continue

        # First price is normally selling price
        price = float(
            prices[0].replace(",", "")
        )

        # ----------------------------------------------------
        # Remove price information from product name
        # ----------------------------------------------------

        product_name = re.sub(
            r"(?:₹|Rs\.?)\s*[\d,]+.*",
            "",
            text,
            flags=re.IGNORECASE
        ).strip()

        if len(product_name) < 5:
            continue

        products.append({

            "Category": "Clothing",

            "Competitor": "Myntra",

            "Product_Name":
                product_name[:250],

            "Competitor_Price":
                price,

            "MRP": (
                float(
                    prices[1].replace(",", "")
                )
                if len(prices) > 1
                else None
            ),

            "Source": url,

            "Scraped_At":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
        })

    # ========================================================
    # METHOD 2: FALLBACK TO PAGE TEXT
    # ========================================================

    if not products:

        print(
            "Product containers not detected."
        )

        print(
            "Trying text-based extraction..."
        )

        page_text = soup.get_text(
            " ",
            strip=True
        )

        # Myntra's page contains product-price
        # information in the rendered/structured text.

        pattern = re.findall(
            r"([A-Za-z][A-Za-z0-9 ,.&'()\-\/]+?)"
            r"\s+Rs\.\s*([\d,]+)",
            page_text
        )

        for product_name, price in pattern:

            product_name = product_name.strip()

            if len(product_name) < 10:
                continue

            if len(product_name) > 200:
                continue

            products.append({

                "Category": "Clothing",

                "Competitor": "Myntra",

                "Product_Name":
                    product_name,

                "Competitor_Price":
                    float(
                        price.replace(",", "")
                    ),

                "MRP": None,

                "Source": url,

                "Scraped_At":
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
            })

    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    unique_products = []

    seen = set()

    for product in products:

        key = (
            product["Product_Name"],
            product["Competitor_Price"]
        )

        if key in seen:
            continue

        seen.add(key)

        unique_products.append(
            product
        )

    return unique_products


# ============================================================
# MAIN
# ============================================================

all_products = []


# ============================================================
# BEAUTY
# ============================================================

try:

    beauty_products = scrape_nykaa(
        SOURCES["Beauty"]["url"]
    )

    print(
        "Beauty products detected:",
        len(beauty_products)
    )

    all_products.extend(
        beauty_products
    )

except Exception as e:

    print(
        "❌ Nykaa scraping error:",
        e
    )


# ============================================================
# CLOTHING
# ============================================================

try:

    clothing_products = scrape_myntra(
        SOURCES["Clothing"]["url"]
    )

    print(
        "Clothing products detected:",
        len(clothing_products)
    )

    all_products.extend(
        clothing_products
    )

except Exception as e:

    print(
        "❌ Myntra scraping error:",
        e
    )


# ============================================================
# DATAFRAME
# ============================================================

df = pd.DataFrame(
    all_products
)


if df.empty:

    print("\n❌ No competitor products collected.")

    exit()


# ============================================================
# CLEAN DATA
# ============================================================

df = df.drop_duplicates(
    subset=[
        "Category",
        "Competitor",
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
print("MULTI-COMPETITOR SCRAPER")
print("========================================")

print(
    "Total products:",
    len(df)
)

print("\nProducts by category:")

print(
    df.groupby(
        ["Category", "Competitor"]
    ).size()
)


print("\nSample products:")

print(
    df[
        [
            "Category",
            "Competitor",
            "Product_Name",
            "Competitor_Price"
        ]
    ]
    .head(15)
    .to_string(index=False)
)


print("\nSaved at:")

print(
    os.path.abspath(
        OUTPUT_PATH
    )
)