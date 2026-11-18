import os
import re
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "competitor_croma.csv"
)

URL = "https://www.croma.com/computers-tablets/c/3"


# ============================================================
# BROWSER
# ============================================================

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

print("Opening Croma...")

driver.get(URL)

time.sleep(5)


# ============================================================
# SCROLL
# ============================================================

print("\nLoading products...")

for i in range(8):

    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);"
    )

    time.sleep(2)

    print(
        f"Scroll {i + 1}/8 completed"
    )

# ============================================================
# INSPECT FIRST PRODUCT
# ============================================================

print("\n========================================")
print("INSPECTING FIRST CROMA PRODUCT")
print("========================================")

product_text = "Microsoft Surface Pro 11th Edition"

elements = driver.find_elements(
    By.XPATH,
    f"//*[contains(text(), '{product_text}')]"
)

print(
    "Matching elements:",
    len(elements)
)

for index, element in enumerate(elements[:5]):

    print("\n--------------------------------")
    print("MATCH", index + 1)
    print("--------------------------------")

    print("TAG:", element.tag_name)

    print("TEXT:")
    print(element.text[:1000])

    print("\nCLASS:")
    print(element.get_attribute("class"))

    print("\nOUTER HTML:")
    print(
        element.get_attribute("outerHTML")[:5000]
    )    


# ============================================================
# FIND PRODUCT CONTAINERS
# ============================================================

print("\nSearching for product containers...")

containers = driver.find_elements(
    By.XPATH,
    "//div[contains(., 'Compare')]"
)

print(
    "Potential containers:",
    len(containers)
)

# ============================================================
# INSPECT CROMA PRODUCT CARDS
# ============================================================

print("\n========================================")
print("INSPECTING CROMA PRODUCT CARDS")
print("========================================")

cards = driver.find_elements(
    By.XPATH,
    "//div[.//button[contains(., 'Compare')]]"
)

print("Cards found:", len(cards))

for index, card in enumerate(cards[:15]):

    try:
        card_text = card.text.strip()

        if card_text:

            print()
            print("--------------------------------")
            print(f"CARD {index + 1}")
            print("--------------------------------")
            print(card_text[:1000])

    except Exception:
        continue


# ============================================================
# USE PAGE TEXT
# ============================================================

body = driver.find_element(
    By.TAG_NAME,
    "body"
).text

lines = [
    line.strip()
    for line in body.splitlines()
    if line.strip()
]


# ============================================================
# PRODUCT EXTRACTION
# ============================================================

products = []

price_pattern = re.compile(
    r"₹\s*([\d,]+(?:\.\d+)?)"
)


for i, line in enumerate(lines):

    # --------------------------------------------------------
    # Skip obvious non-product lines
    # --------------------------------------------------------

    if (
        line.startswith("₹")
        or line in [
            "Compare",
            "Categories",
            "Price",
            "Discount",
            "Brand",
            "Processor Name",
            "All Filters",
            "Sort By",
            "Relevancy",
            "Update pincode for best prices and offers",
            "Add Pincode",
            "Express Delivery within 3 hours",
            "Standard Delivery by Tue, 1st Sep",
            "Standard Delivery by Mon, 24th Aug",
        ]
    ):
        continue


    # --------------------------------------------------------
    # Product names tend to be long
    # --------------------------------------------------------

    if len(line) < 35:
        continue

    # Ignore UI text
    ignored = [
        "SELECT YOUR LOCATION",
        "To Check Products",
        "Sign in to select",
        "Continue",
        "Croma",
        "Computers & Tablets",
        "Categories",
        "Filters",
        "Delivery",
    ]

    if any(
        word.lower() in line.lower()
        for word in ignored
    ):
        continue


    # --------------------------------------------------------
    # Search next 10 lines for prices
    # --------------------------------------------------------

    window = lines[
        i + 1:min(i + 12, len(lines))
    ]

    prices = []

    for item in window:

        matches = price_pattern.findall(item)

        for value in matches:

            prices.append(
                float(
                    value.replace(",", "")
                )
            )


    # --------------------------------------------------------
    # Need at least 2 prices
    # --------------------------------------------------------

    if len(prices) >= 2:

        selling_price = prices[0]
        mrp = prices[1]

        # Validate
        if mrp >= selling_price:

            products.append({
                "Category": "Electronics",
                "Competitor": "Croma",
                "Brand": "",
                "Product_Name": line,
                "Competitor_Price": selling_price,
                "MRP": mrp
            })


# ============================================================
# CLOSE BROWSER
# ============================================================

driver.quit()


# ============================================================
# DATAFRAME
# ============================================================

df = pd.DataFrame(products)


if df.empty:

    print()
    print("❌ No Croma products extracted.")

else:

    # Remove duplicates
    df = df.drop_duplicates(
        subset=[
            "Product_Name",
            "Competitor_Price"
        ]
    )

    # Keep first 30
    df = df.head(30)


    print()
    print("=" * 50)
    print("CROMA SCRAPING RESULT")
    print("=" * 50)

    print(
        "Products extracted:",
        len(df)
    )

    print()
    print(
        df.head(20).to_string(
            index=False
        )
    )


    # ========================================================
    # PRICE STATISTICS
    # ========================================================

    print()
    print("PRICE STATISTICS")

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


    # ========================================================
    # SAVE
    # ========================================================

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print("Saved at:")

    print(
        os.path.abspath(
            OUTPUT_FILE
        )
    )