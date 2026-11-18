import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


NYKAA_URL = "https://www.nykaa.com/nykaa-beauty-store/c/2"


options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)


try:

    print("Opening Nykaa...")

    driver.get(NYKAA_URL)

    time.sleep(7)

    print("Page title:", driver.title)
    print("Page source length:", len(driver.page_source))


    # Try common product containers
    selectors = [
        "div.css-1rd7vky",
        "div.css-d5z3ro",
        "div.css-1y5a2p0",
        "div[class*='product']",
        "li[class*='product']"
    ]

    products = []

    for selector in selectors:

        found = driver.find_elements(
            By.CSS_SELECTOR,
            selector
        )

        if len(found) > 5:

            products = found

            print(
                "Selector:",
                selector
            )

            print(
                "Products found:",
                len(products)
            )

            break


    # Fallback: search page elements containing ₹
    if not products:

        print(
            "Product containers not detected."
        )

        print(
            "Trying price-containing elements..."
        )

        elements = driver.find_elements(
            By.XPATH,
            "//*[contains(text(),'₹')]"
        )

        print(
            "Price elements found:",
            len(elements)
        )

        products = elements


    print("\n========================================")
    print("NYKAA EXTRACTION TEST")
    print("========================================")


    count = 0

    for product in products:

        text = product.text.strip()

        if not text:
            continue

        if "₹" not in text:
            continue

        # Find prices
        prices = re.findall(
            r"₹\s*([\d,]+(?:\.\d+)?)",
            text
        )

        if not prices:
            continue

        print("\n--------------------------------")
        print(text[:500])

        print(
            "Prices:",
            prices
        )

        count += 1

        if count >= 20:
            break


    print("\nProducts displayed:", count)


finally:

    driver.quit()