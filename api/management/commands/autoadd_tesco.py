from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Command(BaseCommand):
    help = 'Automatically adds specified products to the Tesco basket.'

    def handle(self, *args, **options):
        
        options = webdriver.ChromeOptions()
        options.add_argument('start-maximized')
        options.add_argument('disable-infobars')
        browser = webdriver.Chrome(options=options)

        products = [
            {"url": "https://www.tesco.com/groceries/en-GB/products/306650319", "quantity": 2},
        ]

        def add_product_to_basket(product_url, quantity):
            browser.get(product_url)
            input_box = WebDriverWait(browser, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input.ddsweb-quantity-controls__input"))
            )
            input_box.clear()
            input_box.send_keys(str(quantity))

            add_button = WebDriverWait(browser, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ddsweb-quantity-controls__add-button"))
            )
            add_button.click()
            time.sleep(2)  

        for product in products:
            add_product_to_basket(product["url"], product["quantity"])

        print("Done")
        browser.quit()

