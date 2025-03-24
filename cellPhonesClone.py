import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://cellphones.com.vn/mobile/apple.html")
sleep(random.randint(5, 10))

df_all = pd.DataFrame(columns=['Id', 'Name', 'Price', 'image'])
index_count = 1

while True:
    try:
        # Close Popup (if exists)
        try:
            popup = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, "subscriber-popup"))
            )
            print("Popup detected.")

            close_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "cancel-button-top"))
            )
            close_button.click()
            print("Popup closed.")
            sleep(2)
        except TimeoutException:
            print("No popup found.")

        # Check if "Show More" Button Exists
        try:
            while True:
                show_more_btn = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".cps-block-content_btn-showmore .button.btn-show-more.button__show-more-product"))
                )
                print("✅ 'Show More' button detected.")
                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", show_more_btn)
                sleep(1)  # Small delay to ensure scrolling completes
                driver.execute_script("arguments[0].click();", show_more_btn)
                print("Clicked 'Show More' button.")
                sleep(3)
        except TimeoutException:
            print("🚀 No more 'Show More' button. Exiting loop.")
            break  # Exit loop when button is gone
    except Exception as ex:
        print(f"⚠️ Error: {ex}")
        break  # Exit loop on unexpected errors
    
def RawPrice(price):
    if (price != 'N/A'):
        cleaned_price = price.replace('.' ,'').replace('đ' , '')
        return cleaned_price
    return 'N/A'

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Extract product data using BeautifulSoup
products = soup.select(".product-info")  # Select all product containers
title = []
price = []
image = []

for product in products:
    # Extract title
    title_elem = product.select_one(".product__name")
    title.append(title_elem.get_text(strip=True) if title_elem else "N/A")

    # Extract price
    price_elem = product.select_one(".block-box-price .box-info__box-price .product__price--show")
    price.append(RawPrice(price_elem.get_text(strip=True) if price_elem else "N/A"))

    # Extract image
    image_elem = product.select_one(".product__image .product__img")
    image.append(image_elem['src'] if image_elem and 'src' in image_elem.attrs else "N/A")

# Create DataFrame with the extracted data
df1 = pd.DataFrame(list(zip(title, price, image)), columns=['Name', 'Price', 'image'])
df1['Id'] = np.arange(index_count, index_count + len(df1))
print(df1)

# Concatenate with the main DataFrame
df_all = pd.concat([df_all, df1], ignore_index=True)
# Save results to CSV
df_all.to_csv("cellphones_products.csv", index=False , mode='w' , encoding='utf-8')
print("✅ Scraping complete. Data saved.")
