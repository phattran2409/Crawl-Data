import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# Open URL
driver.get("https://cellphones.com.vn/mobile/apple.html")
sleep(random.randint(5,10))
df_all = pd.DataFrame(columns=['index_', 'title', 'price',  'image'])
index_count = 1
exit_loop = False;
while True: 
    try:
        # ================================ GET link/title
        elems = driver.find_elements(By.CSS_SELECTOR , ".product-info .product__name ")
        title = [elem.text for elem in elems]
        # ================================ Get Image 
        # elems_image = driver.find_elements(By.CSS_SELECTOR , "._95X4G  a.picture-wrapper")
        elems_image = driver.find_elements(By.CSS_SELECTOR , ".product-info .product__image .product__img")
        image = [elem.get_attribute("src") for elem in elems_image]
        # ================================ GET price
        elems_price = driver.find_elements(By.CSS_SELECTOR , ".block-box-price .box-info__box-price .product__price--show")
        len(elems_price)
        price = [elem_price.text for elem_price in elems_price]

        df1 = pd.DataFrame(list(zip(title, price ,image)), columns = ['title', 'price','image'])
        df1['index_']= np.arange(index_count, index_count+len(df1))
        print(df1)
        index_count += len(df1)
        
        df_all = pd.concat([df_all, df1], ignore_index=True)
        # tim nut next page

        try:

    # Wait until the popup appears (max 5s)
            popup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "subscriber-popup"))
            )
            print("Popup detected.")

    # Wait until the close button is clickable
            close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "cancel-button-top"))
            )
            close_button.click()
            print("Popup closed.")
        except:
            print("No popup found.")
        
        while True:
            try:
                show_more_btn = WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "btn-show-more"))
                 )
                driver.execute_script("arguments[0].scrollIntoView();", show_more_btn)
                show_more_btn.click()
                print("Clicked 'Show More' button.")
                sleep(2)  # Wait for new products to load
            except:
                print("No more 'Show More' button found.")
                break  # Exit loop if the button is gone
        
     
        # next_page = driver.find_element(By.CSS_SELECTOR , "li.ant-pagination-next")

        # aria_disabled = next_page.get_attribute("aria-disabled")
        # if aria_disabled == "true":
        #     print("📌 Hết trang! Dừng lại.")
        #     break
        # next_page.click()
        # print("📌 Đang chuyển sang trang tiếp theo...")
        # sleep(5)  # Chờ trang tải xong
         # Cuộn xuống để tránh lỗi ClickIntercepted
        # driver.execute_script("arguments[0].scrollIntoView();", next_page)

        # Click vào nút "Next"
        # ActionChains(driver).move_to_element(next_page).click().perform()
    except Exception as ex:
            print(f"⚠️ Lỗi: {ex}")
            break  # Nếu gặp lỗi, dừng vòng lặ
    

