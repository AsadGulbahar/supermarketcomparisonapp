# #Import Libraries
#     #bs4 BeautifulSoup for parsing HTML
#     #selenium Selenium for automating web browser interaction
# import bs4 as bs
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By

# # Set up the Chrome browser with Selenium WebDriver
# browser = webdriver.Chrome()

# #Navigate to ASDA URL
# # The ASDA product URL (replace with your desired URL)
# url = "https://groceries.asda.com/aisle/drinks/squash-cordial/no-added-sugar-squash/1215135760614-1215685911615-1215685911616"
# browser.get(url)

# # Find the Cookies button and click it
# button = browser.find_element(By.ID, "onetrust-accept-btn-handler")
# button.click()


# # Uses WebDriver to wait up to 10 seconds for elements with class name 'co-product' (which represent products on the page) to be present.
# # Wait for the products to load (up to 10 seconds)
# # IF the products don't load within 10 seconds, it catches and prints any exceptions.
# try:
#     element_present = EC.presence_of_all_elements_located((By.CLASS_NAME, 'co-product'))
#     WebDriverWait(browser, 10).until(element_present)
# except Exception as e:
#     print("Error waiting for product containers:", e)

# # Get page source after waiting
# html_source = browser.page_source
# browser.quit()  # Sometimes I commented out to keep the browser open

# # Parse HTML with BeautifulSoup to extract and manipulate HTML elements
# soup = bs.BeautifulSoup(html_source, "html.parser")

# # Locate the pagination element and determine the total number of items
# pagination_element = soup.find('div', {'class': 'search-pagination__item-count'})
# if pagination_element:
#     total_items_text = pagination_element.find('span', {'class': 'search-pagination__count-text--total'}).text
#     total_items = int(total_items_text)
# else:
#     total_items = 0

# # Find all product containers
# # Locates all HTML elements representing individual products using their class name
# product_containers = soup.find_all('div', {'class': 'co-product'})


# # List to store all product information
# all_products = []
# item_count = 0

# for container in product_containers:
#     # Stop if the total number of items has been reached
#     if item_count >= total_items:
#         break

#     # Extracting the product name
#     product_name_element = container.find('a', {'data-auto-id': 'linkProductTitle'})
#     product_name = product_name_element.text.strip() if product_name_element else "Name not found"

#     # Extracting the product URL
#     product_url = product_name_element['href'] if product_name_element else "URL not found"

#     # Extracting the product price
#     product_price_element = container.find('strong', {'class': 'co-product__price'})
#     product_price = product_price_element.text.strip() if product_price_element else "Price not found"
    
#     # Cleaning the price data
#     product_price = product_price.replace('�', '')

#     # Add product information to list
#     all_products.append({"name": product_name, "price": product_price, "url": product_url})
#     item_count += 1

# # Print all product information
# for product in all_products:
#     print("Product Name:", product["name"])
#     print("Product Price:", product["price"])
#     print("Product URL:", product["url"])
#     print("---")


# # For debugging purposes, save the HTML source to a file
# with open("output.html", "w", encoding="utf-8") as file:
#     file.write(html_source)

# print("Done")

import bs4 as bs
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Setup Chrome WebDriver
browser = webdriver.Chrome()

# Navigate to the URL
url = "https://groceries.asda.com/aisle/food-cupboard/biscuits-crackers/chocolate-biscuits/1215337189632-1215686353224-1215686354822"
browser.get(url)

# Accept cookies if needed
try:
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
except Exception as e:
    print("Cookies button not found or not clickable:", e)

# Wait for the product listings to load
try:
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'co-product-list')))
except Exception as e:
    print("Error waiting for product data:", e)
    browser.quit()
    exit()

# Get the HTML source
html_source = browser.page_source
browser.quit()

# Parse HTML with BeautifulSoup
soup = bs.BeautifulSoup(html_source, "html.parser")
product_list = soup.find('div', class_='co-product-list')
product_containers = product_list.find_all('div', {'class': 'co-product'}) if product_list else []

all_products = []
product_index = 1
noOfFailImage = 1

for container in product_containers:
    try:
        name_element = container.find('a', {'data-auto-id': 'linkProductTitle'})
        name = name_element.text.strip() if name_element else "Product name not found"
        link = "https://groceries.asda.com" + name_element['href'] if name_element else "Product link not found"
        
        # Enhanced image extraction logic
        picture_element = container.find('picture', {'class': 'asda-image'})
        image_element = picture_element.find('img') if picture_element else None
        source_element = picture_element.find('source') if picture_element else None
        
        if image_element and image_element.get('src'):
            image_url = image_element.get('src')
        elif source_element and source_element.get('srcset'):
            image_url = source_element.get('srcset').split(",")[0].split(" ")[0]
        else:
            image_url = "Image URL not found"
            noOfFailImage += 1

        # Extracting weight/volume
        volume_tag = container.find('div', {'class': 'co-item__volume-container'}).find('span', {'class': 'co-product__volume'})
        weight = volume_tag.text.strip() if volume_tag else "Volume not specified"

        price_info = container.find('div', {'class': 'co-item__price-container'})
        was_price_tag = price_info.find('span', {'class': 'co-product__was-price'})
        sale_price_tag = price_info.find('strong', {'class': 'co-product__price'})
        rrp = re.search(r"\d+\.\d+", was_price_tag.text.strip()).group() if was_price_tag else \
              (re.search(r"\d+\.\d+", sale_price_tag.text.strip()).group() if sale_price_tag else "RRP not found")
        sale_price = re.search(r"\d+\.\d+", sale_price_tag.text.strip()).group() if sale_price_tag and was_price_tag else "No sale price/not found"
        
        promo_tag = container.find('div', {'class': 'link-save-banner-large__meat-sticker'})
        promo_parts = promo_tag.find_all('span', class_='link-save-banner-large__config') if promo_tag else []
        promo_text = ''.join([part.text for part in promo_parts]).replace('�', '£') if promo_parts else "Promo deal not found"
        
        price_per_measure_tag = price_info.find('span', {'class': 'co-product__price-per-uom'})
        price_per_measure = price_per_measure_tag.text.strip() if price_per_measure_tag else "Price per measure not found"

        all_products.append({
            'name': name,
            'link': link,
            'image_url': image_url,
            'rrp': rrp,
            'sale_price': sale_price,
            'promo_deal': promo_text,
            'price_per_measure': price_per_measure,
            'weight': weight
        })
    except Exception as e:
        print(f"Error processing Product {product_index} ({name if 'name' in locals() else 'Unknown'}): {e}")
    
    product_index += 1  # Increment the product index

# Output extracted data
for product in all_products:
    print(product)
    print(" ")

print("Finished processing all products.")
print("Number of failed image: " + str(noOfFailImage))