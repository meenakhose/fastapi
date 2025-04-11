'''from bs4 import BeautifulSoup
import requests as r
import pandas as pd
from datetime import datetime
from fastapi.responses import JSONResponse

def scrap_meshoo(base_url: str, pages: int = 1):
    all_class = [
        'sc-dkrFOg ProductListItem__GridCol-sc-1baba2g-0 dAbGbG kdQjpv',
        'sc-dkrFOg Pagestyled__ColStyled-sc-ynkej6-2 eSAbia rttYu',
        'sc-dkrFOg Pagestyled__ColStyled-sc-ynkej6-2 eSAbia rttYu'
    ]

    product = []
    prod_price = []
    reviews = []
    ratings = []

    for page in range(1, pages + 1):
        url = f"{base_url}?page={page}"
        print(f"Scraping page: {page}")
        try:
            response = r.get(url, timeout=10)
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')

        for cls in all_class:
            for i in soup.find_all('div', {'class': cls}):
                try:
                    scrap_data = i.text.strip().split('₹', 1)
                    if len(scrap_data) == 2:
                        prod, rest_details = scrap_data
                        price, *detail_parts = rest_details.split(' Free Delivery', 1)

                        product.append(prod.strip())
                        prod_price.append(price.strip())

                        rate_rav_details = detail_parts[0] if detail_parts else ""

                        if 'supplier' in rate_rav_details.lower():
                            ratings.append(rate_rav_details[:3])
                            reviews.append("0")
                        elif 'reviews' in rate_rav_details.lower():
                            parts = rate_rav_details.split()
                            ratings.append(parts[0] if len(parts) > 0 else "N/A")
                            reviews.append(parts[1] if len(parts) > 1 else "N/A")
                        else:
                            ratings.append('N/A')
                            reviews.append('N/A')
                except Exception as e:
                    print("Error processing item:", e)

    all_data = {
        'Scrap_time': datetime.now().isoformat(),
        'Total_products': len(product),
        'Data': [
            {
                'Product': p,
                'Price': pr,
                'Rating': r,
                'Reviews': rv
            }
            for p, pr, r, rv in zip(product, prod_price, ratings, reviews)
        ]
    }

    return JSONResponse(content=all_data)'''
from selenium import webdriver
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
    }
