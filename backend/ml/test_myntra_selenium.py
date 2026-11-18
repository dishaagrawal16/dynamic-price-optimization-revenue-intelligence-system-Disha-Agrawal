from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re


# ============================================================
# BROWSER SETUP
# ============================================================

options = Options()

options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")


driver = webdriver.Chrome(
    options=options
)


try:

    print("Opening Myntra...")

    driver.get(
        "https://www.myntra.com/dresses"
    )

    # Give JavaScript time to load
    time.sleep(5)


    # ========================================================
    # FIND PRODUCT CONTAINERS
    # ========================================================

    products = driver.find_elements(
        By.CSS_SELECTOR,
        "li.product-base"
    )

    print(
        "Product containers found:",
        len(products)
    )


    # ========================================================
    # EXTRACT PRODUCTS
    # ========================================================

    extracted = []


    for product in products[:20]:

        text = product.text.strip()

        if not text:
            continue


        print("\n--------------------------------")
        print(text)


        # ----------------------------------------------------
        # Find prices
        # ----------------------------------------------------

        prices = re.findall(
            r"Rs\.\s*([\d,]+)",
            text
        )


        if not prices:

            # Sometimes ₹ is used
            prices = re.findall(
                r"₹\s*([\d,]+)",
                text
            )


        if prices:

            price = float(
                prices[0].replace(
                    ",",
                    ""
                )
            )

        else:

            price = None


        extracted.append({

            "raw_text": text,

            "price": price
        })


    # ========================================================
    # SUMMARY
    # ========================================================

    print("\n========================================")
    print("MYNTRA EXTRACTION TEST")
    print("========================================")

    print(
        "Products extracted:",
        len(extracted)
    )


    for item in extracted:

        print(
            item
        )


finally:

    driver.quit()