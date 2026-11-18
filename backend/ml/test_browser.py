from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


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

    time.sleep(5)

    print(
        "Page title:",
        driver.title
    )

    print(
        "Current URL:",
        driver.current_url
    )

    print(
        "Page source length:",
        len(driver.page_source)
    )

    print("\nBrowser test successful!")

finally:

    driver.quit()