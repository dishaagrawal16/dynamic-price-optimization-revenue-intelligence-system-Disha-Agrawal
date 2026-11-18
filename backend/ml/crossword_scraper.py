import os
import re
import time
import pandas as pd

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


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
    "crossword_competitor_prices.csv"
)

URL = "https://www.crossword.in/collections/books"


options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)


try:

    print("\n========================================")
    print("SCRAPING CROSSWORD")
    print("========================================")

    driver.get(URL)

    time.sleep(6)

    print("Current URL:", driver.current_url)

    # Get the entire rendered page text
    body_text = driver.find_element(
        By.TAG_NAME,
        "body"
    ).text

    print(
        "Page text length:",
        len(body_text)
    )

    # --------------------------------------------------------
    # Split around Add to Bag
    # --------------------------------------------------------

    blocks = body_text.split("Add to Bag")

    print(
        "Potential product blocks:",
        len(blocks)
    )

    results = []


    for block in blocks:

        lines = [
            line.strip()
            for line in block.split("\n")
            if line.strip()
        ]

        if len(lines) < 4:
            continue


        # ----------------------------------------------------
        # Find price lines
        # ----------------------------------------------------

        price_values = []

        for line in lines:

            match = re.fullmatch(
                r"₹\s*([\d,]+)",
                line
            )

            if match:

                price_values.append(
                    float(
                        match.group(1).replace(
                            ",",
                            ""
                        )
                    )
                )


        # Need selling price + MRP
        if len(price_values) < 2:
            continue


        # Usually first = selling price
        # second = MRP

        selling_price = price_values[0]
        mrp = price_values[1]


        # ----------------------------------------------------
        # Find discount
        # ----------------------------------------------------

        discount_index = None

        for i, line in enumerate(lines):

            if "Off" in line and "₹" in line:

                discount_index = i
                break


        if discount_index is None:
            continue


        # ----------------------------------------------------
        # Everything before price is product information
        # ----------------------------------------------------

        price_index = None

        for i, line in enumerate(lines):

            if re.fullmatch(
                r"₹\s*[\d,]+",
                line
            ):

                price_index = i

                break


        if price_index is None:
            continue


        info_lines = lines[:price_index]


        # Remove obvious navigation/filter text

        ignored = {
            "Books",
            "Add to Bag",
            "Buy Now",
            "Filter",
            "Sort By",
            "Relevance"
        }


        info_lines = [
            x
            for x in info_lines
            if x not in ignored
        ]


        if len(info_lines) < 2:
            continue


        # Last two meaningful lines before price
        # are normally:
        #
        # Book Name
        # Author

        product_name = info_lines[-2]
        author = info_lines[-1]


        # ----------------------------------------------------
        # Basic validation
        # ----------------------------------------------------

        if len(product_name) < 3:
            continue

        if len(author) < 2:
            continue


        # Reject obvious navigation/filter text

        bad_words = [
            "Category",
            "Sub Category",
            "Format",
            "Language",
            "Price",
            "Stationery",
            "Toys",
            "Gifts"
        ]

        if product_name in bad_words:
            continue


        results.append({

            "Category": "Books",

            "Subcategory": "Books",

            "Competitor": "Crossword",

            "Brand": "",

            "Product_Name": product_name,

            "Author": author,

            "Competitor_Price":
                selling_price,

            "MRP":
                mrp,

            "Source": URL,

            "Scraped_At":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

        })


    # --------------------------------------------------------
    # DataFrame
    # --------------------------------------------------------

    df = pd.DataFrame(results)


    if df.empty:

        print("\n❌ No books extracted.")

    else:

        df = df.drop_duplicates(
            subset=[
                "Product_Name",
                "Competitor_Price"
            ]
        )


        df.to_csv(
            OUTPUT_PATH,
            index=False
        )


        print("\n========================================")
        print("CROSSWORD SCRAPING SUCCESSFUL")
        print("========================================")

        print(
            "Books extracted:",
            len(df)
        )


        print("\nSample books:")

        print(
            df[
                [
                    "Product_Name",
                    "Author",
                    "Competitor_Price",
                    "MRP"
                ]
            ]
            .head(15)
            .to_string(index=False)
        )


        print("\nAverage Price:",
              round(
                  df["Competitor_Price"].mean(),
                  2
              ))

        print(
            "Minimum Price:",
            df["Competitor_Price"].min()
        )

        print(
            "Maximum Price:",
            df["Competitor_Price"].max()
        )


        print("\nSaved at:")

        print(
            os.path.abspath(
                OUTPUT_PATH
            )
        )


finally:

    driver.quit()