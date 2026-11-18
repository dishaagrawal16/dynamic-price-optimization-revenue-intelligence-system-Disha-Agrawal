import os
import re
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
    "competitor_books_crossword.csv"
)

URL = "https://www.crossword.in/collections/books"


# ============================================================
# BROWSER
# ============================================================

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

print("Opening Crossword...")

driver.get(URL)

# Wait for page
driver.implicitly_wait(5)


# ============================================================
# PAGE TEXT
# ============================================================

text = driver.find_element(
    By.TAG_NAME,
    "body"
).text

driver.quit()

print("Page text length:", len(text))


# ============================================================
# CLEAN LINES
# ============================================================

lines = [
    line.strip()
    for line in text.splitlines()
    if line.strip()
]


# ============================================================
# FIND BOOKS USING "OFF" LINE
# ============================================================

products = []

for i, line in enumerate(lines):

    # Example:
    # ₹ 81 Off
    # ₹ 143 Off

    discount_match = re.search(
        r"₹\s*([\d,]+(?:\.\d+)?)\s*Off",
        line,
        re.IGNORECASE
    )

    if not discount_match:
        continue

    discount = float(
        discount_match.group(1)
        .replace(",", "")
    )

    # Look backwards for the nearest two price values.
    #
    # Expected:
    #
    # Product Name
    # Author
    # ₹
    # 369
    # ₹
    # 450
    # ₹ 81 Off

    prices = []

    j = i - 1

    while j >= 0 and len(prices) < 2:

        current = lines[j]

        # Case 1:
        # current line itself is a number
        if re.fullmatch(
            r"[\d,]+(?:\.\d+)?",
            current
        ):
            prices.append(
                float(current.replace(",", ""))
            )

        j -= 1

    if len(prices) < 2:
        continue

    # Because we're going backwards:
    #
    # prices[0] = MRP
    # prices[1] = Selling price

    mrp = prices[0]
    selling_price = prices[1]

    # Validate
    if mrp < selling_price:
        continue

    if selling_price <= 0:
        continue

    # --------------------------------------------------------
    # Find product name
    # --------------------------------------------------------

    # Search backwards from the selling price area.
    #
    # Avoid:
    # ₹
    # Add to Bag
    # Filter
    # Books
    # Sort By
    # Price
    # etc.

    candidate_names = []

    for k in range(
        max(0, j - 5),
        j + 1
    ):
        value = lines[k].strip()

        if (
            value
            and value != "₹"
            and value != "Books"
            and value != "Filter"
            and value != "Price"
            and value != "Add to Bag"
            and value != "Sort By"
        ):
            candidate_names.append(value)

    if not candidate_names:
        continue

    # The first candidate is generally the product name
    product_name = candidate_names[-1]

    # Avoid obvious navigation/category text
    blocked = {
        "Relevance",
        "Books",
        "Stationery",
        "Toys",
        "Gifts",
        "Filter",
        "Category",
        "Sub Category",
        "Format",
        "Author",
        "Language",
        "Price",
        "Sort By"
    }

    if product_name in blocked:
        continue

    # Don't allow ₹ as name
    if product_name == "₹":
        continue

    products.append({
        "Category": "Books",
        "Competitor": "Crossword",
        "Product_Name": product_name,
        "Competitor_Price": selling_price,
        "MRP": mrp,
        "Discount": discount
    })


# ============================================================
# DATAFRAME
# ============================================================

df = pd.DataFrame(products)


if df.empty:

    print()
    print("❌ No valid books extracted.")

else:

    # Remove duplicate records
    df = df.drop_duplicates(
        subset=[
            "Product_Name",
            "Competitor_Price",
            "MRP"
        ]
    )

    # Keep reasonable number
    df = df.head(50)

    print()
    print("=" * 60)
    print("CROSSWORD SCRAPING SUCCESSFUL")
    print("=" * 60)

    print(
        "Valid products extracted:",
        len(df)
    )

    print()
    print(
        df.head(15).to_string(index=False)
    )

    print()
    print("Price statistics:")

    print(
        df[
            [
                "Competitor_Price",
                "MRP",
                "Discount"
            ]
        ].describe()
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
        os.path.abspath(OUTPUT_FILE)
    )