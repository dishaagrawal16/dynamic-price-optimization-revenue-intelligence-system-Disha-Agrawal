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
    "competitor_prices_browser.csv"
)


# ============================================================
# MYNTRA CONFIGURATION
# ============================================================

MYNTRA_URL = "https://www.myntra.com/dresses"


# ============================================================
# BROWSER SETUP
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
# SCRAPE MYNTRA
# ============================================================

def scrape_myntra():

    print("\n========================================")
    print("SCRAPING MYNTRA")
    print("========================================")

    driver.get(
        MYNTRA_URL
    )

    # Allow JavaScript to load
    time.sleep(5)


    # ========================================================
    # FIND PRODUCT CARDS
    # ========================================================

    products = driver.find_elements(
        By.CSS_SELECTOR,
        "li.product-base"
    )

    print(
        "Product cards found:",
        len(products)
    )


    results = []


    # ========================================================
    # EXTRACT PRODUCTS
    # ========================================================

    for product in products:

        try:

            text = product.text.strip()

            if not text:
                continue


            # ------------------------------------------------
            # Extract prices
            # ------------------------------------------------

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


            # ------------------------------------------------
            # Selling price
            # ------------------------------------------------

            selling_price = float(
                prices[0].replace(
                    ",",
                    ""
                )
            )


            # ------------------------------------------------
            # MRP
            # ------------------------------------------------

            if len(prices) >= 2:

                mrp = float(
                    prices[1].replace(
                        ",",
                        ""
                    )
                )

            else:

                mrp = selling_price


            # ------------------------------------------------
            # Product name
            # ------------------------------------------------

            lines = [
                line.strip()
                for line in text.split("\n")
                if line.strip()
            ]


            # Remove rating/review/badge lines
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


                if line.startswith(
                    "Rs."
                ):
                    continue


                clean_lines.append(
                    line
                )


            # ------------------------------------------------
            # Find product name
            # ------------------------------------------------

            # Usually:
            # Brand
            # Product Name

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


            # Remove discount information
            product_name = re.sub(
                r"\(.*?OFF\)",
                "",
                product_name,
                flags=re.IGNORECASE
            ).strip()


            if len(product_name) < 5:

                continue


            # ------------------------------------------------
            # Save
            # ------------------------------------------------

            results.append({

                "Category":
                    "Clothing",

                "Competitor":
                    "Myntra",

                "Brand":
                    brand,

                "Product_Name":
                    product_name,

                "Competitor_Price":
                    selling_price,

                "MRP":
                    mrp,

                "Source":
                    MYNTRA_URL,

                "Scraped_At":
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
            })


        except Exception as e:

            print(
                "Product extraction error:",
                e
            )


    return results


# ============================================================
# MAIN
# ============================================================

try:

    myntra_products = scrape_myntra()


    # ========================================================
    # DATAFRAME
    # ========================================================

    df = pd.DataFrame(
        myntra_products
    )


    if df.empty:

        print(
            "\n❌ No products extracted."
        )

    else:

        # Remove duplicates
        df = df.drop_duplicates(
            subset=[
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
        # OUTPUT
        # ====================================================

        print("\n========================================")
        print("COMPETITOR MONITORING SUCCESSFUL")
        print("========================================")

        print(
            "Products extracted:",
            len(df)
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
            .head(10)
            .to_string(index=False)
        )


        print("\n========================================")
        print("PRICE STATISTICS")
        print("========================================")

        print(
            "Average Selling Price:",
            round(
                df["Competitor_Price"].mean(),
                2
            )
        )

        print(
            "Minimum Selling Price:",
            round(
                df["Competitor_Price"].min(),
                2
            )
        )

        print(
            "Maximum Selling Price:",
            round(
                df["Competitor_Price"].max(),
                2
            )
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
            os.path.abspath(
                OUTPUT_PATH
            )
        )


finally:

    driver.quit()