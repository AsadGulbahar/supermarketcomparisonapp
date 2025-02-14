#Import Libraries
    #bs4 BeautifulSoup for parsing HTML
    #selenium Selenium for automating web browser interaction
import bs4 as bs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Set up the Chrome browser with Selenium WebDriver
browser = webdriver.Chrome()

#Navigate to MORRISONS URL
# The MORRISONS product URL (replace with your desired URL)
url = "https://groceries.morrisons.com/search?entry=maryland%20cookies"
browser.get(url)

# Find the Cookies button and click it
# button = browser.find_element(By.ID, "onetrust-accept-btn-handler")
# button.click()


# Uses WebDriver to wait up to 10 seconds for elements with class name 'main-column' (which represent products on the page) to be present.
# Wait for the products to load (up to 10 seconds)
# IF the products don't load within 10 seconds, it catches and prints any exceptions.
try:
    element_present = EC.presence_of_all_elements_located((By.CLASS_NAME, 'main-column'))
    WebDriverWait(browser, 10).until(element_present)
except Exception as e:
    print("Error waiting for product containers:", e)

# Get page source after waiting
html_source = browser.page_source
browser.quit()  # Sometimes I commented out to keep the browser open

# Parse HTML with BeautifulSoup to extract and manipulate HTML elements
soup = bs.BeautifulSoup(html_source, "html.parser")


# Locate the pagination element and determine the total number of items
pagination_element = soup.find('div', {'class': 'total-product-number'})
if pagination_element:
    total_items_text = pagination_element.find('span').text
    # Extract the number from the text (e.g., "6 products")
    total_items = int(''.join(filter(str.isdigit, total_items_text)))
else:
    total_items = 0



# Find all product lists
product_lists = soup.find_all('ul', {'class': 'fops fops-regular fops-shelf'})

# List to store all product information
all_products = []
item_count = 0


for product_list in product_lists:

    # Iterate over each product item in the list
    product_items = product_list.find_all('li', {'class': 'fops-item fops-item--cluster'})


    # Find the div with the specific class and then extract the SKU
    product_sku_container = container.find('div', {'class': 'fop-item'})
    product_sku = product_sku_container['data-sku'] if product_sku_container and 'data-sku' in product_sku_container.attrs else "SKU not found"

    # Extracting the product name
    product_name_element = container.find('h4', {'class': 'fop-title'})
    product_name = product_name_element.text.strip() if product_name_element else "Name not found"

    # Extracting the product URL
    product_url_element = container.find('a', href=True)
    product_url = "https://groceries.morrisons.com" + product_url_element['href'] if product_url_element else "URL not found"

    # Extracting the product image
    product_image_element = container.find('img', {'class': 'fop-img'})
    product_image_url = "https://groceries.morrisons.com" + product_image_element['src'] if product_image_element else "Image URL not found"

    # Extracting the product price
    product_price_element = container.find('div', {'class': 'price-group-wrapper'})
    if product_price_element:
        product_price_span = product_price_element.find('span', {'class': 'fop-price'})
        product_price = product_price_span.text.strip() if product_price_span else "Price not found"
    else:
        product_price = "Price not found"


    # Cleaning the price data
  

    # Add product information to list
    all_products.append({
        "sku": product_sku,
        "name": product_name,
        "price": product_price,
        "url": product_url,
        "image_url": product_image_url
    })

    # Stop if the total number of items has been reached
    if len(all_products) >= total_items:
        break

# [Remaining code sections for printing and saving data remain unchanged]


# Print all product information
for product in all_products:
    print("Product SKU:", product["sku"])
    print("Product Name:", product["name"])
    print("Product Price:", product["price"])
    print("Product URL:", product["url"])
    print("Product Image URL:", product["image_url"])
    print("---")


# For debugging purposes, save the HTML source to a file
with open("morrissons_output.html", "w", encoding="utf-8") as file:
    file.write(html_source)

print("Done")