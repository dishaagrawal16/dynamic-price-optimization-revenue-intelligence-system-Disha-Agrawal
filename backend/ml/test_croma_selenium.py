import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


URL = "https://www.croma.com/computers-tablets/c/3"

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

print("Opening Croma...")

driver.get(URL)

time.sleep(5)

print("Page title:", driver.title)
print("Current URL:", driver.current_url)


# ============================================================
# SCROLL TO LOAD PRODUCTS
# ============================================================

print("\nScrolling to load products...")

for i in range(8):

    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);"
    )

    time.sleep(2)

    print(
        f"Scroll {i + 1}/8 completed"
    )


# ============================================================
# PAGE TEXT
# ============================================================

body = driver.find_element(
    By.TAG_NAME,
    "body"
).text

print("\nPage text length:", len(body))


# ============================================================
# FIND PRICE VALUES
# ============================================================

prices = re.findall(
    r"₹\s*([\d,]+(?:\.\d+)?)",
    body
)


print("\n========================================")
print("CROMA EXTRACTION TEST")
print("========================================")

print(
    "Prices detected:",
    len(prices)
)

print("\nFirst 50 prices:")

for price in prices[:50]:
    print(price)


# ============================================================
# FIND PRODUCT-LIKE TEXT
# ============================================================

print("\n========================================")
print("PRODUCT TEXT SAMPLE")
print("========================================")

lines = [
    line.strip()
    for line in body.splitlines()
    if line.strip()
]

for i, line in enumerate(lines):

    # Show lines that look like actual product names
    if (
        len(line) > 30
        and not line.startswith("₹")
        and "Compare" not in line
        and "Filters" not in line
        and "Categories" not in line
    ):

        print(line)

        if i > 150:
            break


driver.quit()