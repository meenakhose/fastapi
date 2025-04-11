'''from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

def scrap_meshoo(base_url: str, pages: int):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    results = []
    try:
        for page in range(1, pages + 1):
            url = f"{base_url}&page={page}"
            driver.get(url)

            driver.implicitly_wait(5)

            products = driver.find_elements(By.CSS_SELECTOR, "a[href*='/item/']")
            for p in products:
                try:
                    name = p.find_element(By.CLASS_NAME, "Text__StyledText-sc-oo0kvp-0").text
                    price = p.find_element(By.CLASS_NAME, "Text__StyledText-sc-oo0kvp-0.bZNoZL").text
                    results.append({"name": name, "price": price})
                except:
                    continue
    finally:
        driver.quit()

    return {
        "Scrap_time": str(datetime.utcnow()),
        "Total_products": len(results),
        "Data": results
    }'''
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import time

def scrap_meshoo(base_url: str, pages: int):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    product = []
    prod_price = []
    reviews = []
    ratings = []

    try:
        for page in range(1, pages + 1):
            url = f"{base_url}?page={page}"
            driver.get(url)
            time.sleep(3)  # wait for JS to load

            containers = driver.find_elements(By.XPATH, "//div[contains(@class, 'sc-dkrFOg')]")
            for container in containers:
                try:
                    text = container.text.strip()
                    if "₹" not in text or "Free Delivery" not in text:
                        continue
                    scrap_data = text.split('₹', 1)
                    if len(scrap_data) != 2:
                        continue

                    prod, rest = scrap_data
                    price, rate_rav_details = rest.split(' Free Delivery', 1)

                    product.append(prod.strip())
                    prod_price.append(price.strip())

                    if 'supplier' in rate_rav_details.lower():
                        ratings.append(rate_rav_details[:3])
                        reviews.append('0')
                    elif 'reviews' in rate_rav_details.lower():
                        rat_rv = rate_rav_details.strip().split(' ')[0]
                        rat = rat_rv[:3]
                        rv = rat_rv[3:]
                        ratings.append(rat)
                        reviews.append(rv)
                    else:
                        ratings.append('N/A')
                        reviews.append('N/A')
                except Exception as e:
                    print(f"Error parsing product container: {e}")

    finally:
        driver.quit()

    all_data = {
        'Scrap_time': datetime.now(),
        'Product': product,
        'Price': prod_price,
        'Rating': ratings,
        'Reviews': reviews
    }

    table = pd.DataFrame(all_data)
    return table

