

import bs4 as bs
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Setup function for Chrome WebDriver
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

# Function to scrape data from the current page
def scrape_page(driver):
    soup = bs.BeautifulSoup(driver.page_source, 'html.parser')
    product_data = []
    decimal_pattern = re.compile(r"\d+\.\d+(/\w+)?")

    for product in soup.select('ul.product-list > li'):
        try:
            title = product.select_one("div.product-details--wrapper h3 a span").text.strip()
            link = product.select_one("div.product-details--wrapper h3 a").get('href')
            image_url = product.select_one("div.product-image__container img").get('srcset').split(",")[0].strip().split(" ")[0]
            rrp = decimal_pattern.search(product.select_one("p.styled__StyledHeading-sc-119w3hf-2").text).group() if product.select_one("p.styled__StyledHeading-sc-119w3hf-2") else "RRP not found"
            price_per_measure = decimal_pattern.search(product.select_one("p.styled__StyledFootnote-sc-119w3hf-7").text).group() if product.select_one("p.styled__StyledFootnote-sc-119w3hf-7") else "Price per measure not found"
            
            product_data.append({
                'title': title,
                'link': "https://www.tesco.com" + link,
                'image_url': image_url,
                'rrp': rrp,
                'price_per_measure': price_per_measure
            })
        except Exception as e:
            print(f"Error processing product: {e}")

    return product_data

# Main function to navigate and scrape data across multiple pages
def main():
    driver = setup_driver()
    url = "https://www.tesco.com/groceries/en-GB/shop/fresh-food/fresh-fruit/dried-fruit-nuts-and-seeds"
    driver.get(url)

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-list')))
        
        # Calculate the number of pages based on item count
        items_info = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".pagination__items-displayed > strong:last-child"))
        )
        total_items = int(items_info.text.split()[-1])
        total_pages = (total_items // 48) + (total_items % 48 > 0)

        for page in range(1, total_pages + 1):
            driver.get(f"{url}?page={page}&count=48")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-list')))
            products = scrape_page(driver)
            print(f"Scraped page {page}/{total_pages} with {len(products)} products.")
            # Process or store the products data

    except TimeoutException:
        print("Failed to load the webpage properly.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
