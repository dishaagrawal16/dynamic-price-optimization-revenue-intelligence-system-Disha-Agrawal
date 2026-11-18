import os
import re
import time
import pandas as pd

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


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

OUTPUT_PATH = os.path.join(
    DATA_DIR,
    "competitor_prices_v2.csv"
)


# ============================================================
# URLs
# ============================================================

MYNTRA_URL = "https://www.myntra.com/dresses"

NYKAA_URL = "https://www.nykaa.com/nykaa-beauty-store/c/2"


# ============================================================
# BROWSER
# ============================================================

options = Options()

options.add_argument(
    "--start-maximized"
)

options.add_argument(
    "--disable-blink-features=AutomationControlled"
)

driver = webdriver.Chrome(
    options=options
)


# ============================================================
# MYNTRA
# ============================================================

def scrape_myntra():

    print("\n========================================")
    print("SCRAPING MYNTRA")
    print("========================================")

    driver.get(MYNTRA_URL)

    time.sleep(5)

    products = driver.find_elements(
        By.CSS_SELECTOR,
        "li.product-base"
    )

    print(
        "Product cards found:",
        len(products)
    )

    results = []

    for product in products:

        try:

            text = product.text.strip()

            if not text:
                continue

            prices = re.findall(
                r"Rs\.\s*([\d,]+)",
                text
            )

            if not prices:

                prices = re.findall(
                    r"₹\s*([\d,]+)",
                    text
                )

            if not prices:
                continue

            selling_price = float(
                prices[0].replace(",", "")
            )

            if len(prices) >= 2:

                mrp = float(
                    prices[1].replace(",", "")
                )

            else:

                mrp = selling_price


            lines = [
                line.strip()
                for line in text.split("\n")
                if line.strip()
            ]


            clean_lines = []

            for line in lines:

                if re.fullmatch(
                    r"\d+(\.\d+)?",
                    line
                ):
                    continue

                if line == "|":
                    continue

                if re.fullmatch(
                    r"\d+(\.\d+)?k",
                    line,
                    re.IGNORECASE
                ):
                    continue

                if line.upper() in [
                    "AD",
                    "NEW"
                ]:
                    continue

                if line.startswith("Rs."):
                    continue

                clean_lines.append(line)


            if len(clean_lines) >= 2:

                brand = clean_lines[0]

                product_name = " ".join(
                    clean_lines[1:]
                )

            elif len(clean_lines) == 1:

                brand = ""

                product_name = clean_lines[0]

            else:

                continue


            product_name = re.sub(
                r"\(.*?OFF\)",
                "",
                product_name,
                flags=re.IGNORECASE
            ).strip()


            if len(product_name) < 5:
                continue


            results.append({

                "Category": "Clothing",

                "Subcategory": "Dresses",

                "Competitor": "Myntra",

                "Brand": brand,

                "Product_Name": product_name,

                "Competitor_Price":
                    selling_price,

                "MRP": mrp,

                "Source": MYNTRA_URL,

                "Scraped_At":
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
            })

        except Exception as e:

            print(
                "Myntra product error:",
                e
            )


    return results


# ============================================================
# NYKAA
# ============================================================

def scrape_nykaa():

    print("\n========================================")
    print("SCRAPING NYKAA")
    print("========================================")

    driver.get(NYKAA_URL)

    time.sleep(7)

    selector = "div.css-1rd7vky"

    products = driver.find_elements(
        By.CSS_SELECTOR,
        selector
    )

    print(
        "Product cards found:",
        len(products)
    )

    results = []

    seen = set()


    for product in products:

        try:

            text = product.text.strip()

            if not text:
                continue


            # ------------------------------------------------
            # Extract all prices
            # ------------------------------------------------

            prices = re.findall(
                r"₹\s*([\d,]+(?:\.\d+)?)",
                text
            )

            if not prices:
                continue


            numeric_prices = []

            for price in prices:

                value = float(
                    price.replace(",", "")
                )

                numeric_prices.append(value)


            # ------------------------------------------------
            # MRP + selling price
            # ------------------------------------------------

            if len(numeric_prices) >= 2:

                mrp = numeric_prices[0]

                selling_price = numeric_prices[1]

            else:

                mrp = numeric_prices[0]

                selling_price = numeric_prices[0]


            # ------------------------------------------------
            # Extract product name
            # ------------------------------------------------

            lines = [
                line.strip()
                for line in text.split("\n")
                if line.strip()
            ]


            product_lines = []

            for line in lines:

                if line.startswith("₹"):
                    continue

                if "Off" in line:
                    continue

                if "Regular price" in line:
                    continue

                if "Discounted price" in line:
                    continue

                if "Wishlist" in line:
                    continue

                if "Preview" in line:
                    continue

                if "Enjoy Complimentary" in line:
                    continue

                if "Enjoy Free Gift" in line:
                    continue

                if re.fullmatch(
                    r"\(\s*[\d,]+\s*\)",
                    line
                ):
                    continue

                if re.fullmatch(
                    r"\d+\s*(Sizes|Shades|Size|Shade)",
                    line,
                    re.IGNORECASE
                ):
                    continue

                product_lines.append(line)


            if not product_lines:
                continue


            product_name = product_lines[0]


            # Remove unwanted prefixes

            product_name = re.sub(
                r"^BESTSELLER\s+",
                "",
                product_name,
                flags=re.IGNORECASE
            )

            product_name = re.sub(
                r"^AD\s+",
                "",
                product_name,
                flags=re.IGNORECASE
            )

            product_name = product_name.strip()


            if len(product_name) < 5:
                continue


            # ------------------------------------------------
            # Duplicate protection
            # ------------------------------------------------

            key = (
                product_name.lower(),
                selling_price
            )

            if key in seen:
                continue

            seen.add(key)


            results.append({

                "Category": "Beauty",

                "Subcategory": "Beauty Products",

                "Competitor": "Nykaa",

                "Brand": "",

                "Product_Name": product_name,

                "Competitor_Price":
                    selling_price,

                "MRP": mrp,

                "Source": NYKAA_URL,

                "Scraped_At":
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
            })


        except Exception as e:

            print(
                "Nykaa product error:",
                e
            )


    return results


# ============================================================
# MAIN
# ============================================================

try:

    all_products = []


    # --------------------------------------------------------
    # Myntra
    # --------------------------------------------------------

    myntra_products = scrape_myntra()

    print(
        "Valid Myntra products:",
        len(myntra_products)
    )

    all_products.extend(
        myntra_products
    )


    # --------------------------------------------------------
    # Nykaa
    # --------------------------------------------------------

    nykaa_products = scrape_nykaa()

    print(
        "Valid Nykaa products:",
        len(nykaa_products)
    )

    all_products.extend(
        nykaa_products
    )


    # ========================================================
    # DATAFRAME
    # ========================================================

    df = pd.DataFrame(
        all_products
    )


    if df.empty:

        print(
            "\n❌ No competitor products collected."
        )

    else:

        df = df.drop_duplicates(
            subset=[
                "Category",
                "Competitor",
                "Product_Name",
                "Competitor_Price"
            ]
        )


        # ====================================================
        # SAVE
        # ====================================================

        df.to_csv(
            OUTPUT_PATH,
            index=False
        )


        # ====================================================
        # SUMMARY
        # ====================================================

        print("\n========================================")
        print("COMPETITOR MONITORING SUCCESSFUL")
        print("========================================")

        print(
            "Total products:",
            len(df)
        )


        print("\nProducts by category:")

        print(
            df.groupby(
                [
                    "Category",
                    "Competitor"
                ]
            ).size()
        )


        print("\nSample products:")

        print(
            df[
                [
                    "Category",
                    "Competitor",
                    "Brand",
                    "Product_Name",
                    "Competitor_Price",
                    "MRP"
                ]
            ]
            .head(15)
            .to_string(index=False)
        )


        print("\n========================================")
        print("PRICE STATISTICS")
        print("========================================")


        for competitor in df["Competitor"].unique():

            subset = df[
                df["Competitor"] == competitor
            ]

            print(
                f"\n{competitor}"
            )

            print(
                "Average Price:",
                round(
                    subset[
                        "Competitor_Price"
                    ].mean(),
                    2
                )
            )

            print(
                "Minimum Price:",
                round(
                    subset[
                        "Competitor_Price"
                    ].min(),
                    2
                )
            )

            print(
                "Maximum Price:",
                round(
                    subset[
                        "Competitor_Price"
                    ].max(),
                    2
                )
            )


        print("\nSaved at:")

        print(
            os.path.abspath(
                OUTPUT_PATH
            )
        )


finally:

    driver.quit()