import time
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


BOOKS_URL = "https://www.crossword.in/collections/books"


options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)


try:

    print("Opening Crossword...")

    driver.get(BOOKS_URL)

    time.sleep(6)

    print("Page title:", driver.title)
    print("Current URL:", driver.current_url)
    print("Page source length:", len(driver.page_source))


    # ========================================================
    # FIND PRODUCT CARDS USING "ADD TO BAG"
    # ========================================================

    buttons = driver.find_elements(
        By.XPATH,
        "//*[contains(normalize-space(text()), 'Add to Bag')]"
    )

    print(
        "Add to Bag elements found:",
        len(buttons)
    )


    print("\n========================================")
    print("CROSSWORD PRODUCT TEST")
    print("========================================")


    count = 0


    for button in buttons[:20]:

        try:

            # ------------------------------------------------
            # Move upward until we find a useful container
            # ------------------------------------------------

            card = button

            for _ in range(6):

                parent = card.find_element(
                    By.XPATH,
                    "./.."
                )

                text = parent.text.strip()

                if (
                    "₹" in text
                    and "Add to Bag" in text
                    and len(text) < 1000
                ):

                    card = parent
                    break

                card = parent


            text = card.text.strip()


            if not text:
                continue


            print("\n--------------------------------")
            print(text)


            # ------------------------------------------------
            # Extract prices
            # ------------------------------------------------

            prices = re.findall(
                r"₹\s*([\d,]+)",
                text
            )


            print(
                "Prices:",
                prices
            )


            count += 1


        except Exception as e:

            print(
                "Error:",
                e
            )


    print("\nProducts detected:", count)


finally:

    driver.quit()