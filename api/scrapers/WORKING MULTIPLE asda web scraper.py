import bs4 as bs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Set up the Chrome browser with Selenium
browser = webdriver.Chrome()

# The ASDA product URL (replace with your desired URL)
url = "https://groceries.asda.com/search/maryland%20cookies"
browser.get(url)

# Wait for the products to load (up to 10 seconds)
try:
    element_present = EC.presence_of_all_elements_located((By.CLASS_NAME, 'co-product'))
    WebDriverWait(browser, 10).until(element_present)
except Exception as e:
    print("Error waiting for product containers:", e)

# Get page source after waiting
html_source = browser.page_source
browser.quit()

soup = bs.BeautifulSoup(html_source, "html.parser")

# Find all product containers
product_containers = soup.find_all('div', {'class': 'co-product'})

# List to store all product information
all_products = []

for container in product_containers:
    # Extracting the product name
    product_name_element = container.find('a', {'data-auto-id': 'linkProductTitle'})
    product_name = product_name_element.text.strip() if product_name_element else "Name not found"

    # Extracting the product price
    product_price_element = container.find('strong', {'class': 'co-product__price'})
    product_price = product_price_element.text.strip() if product_price_element else "Price not found"
    
    # Cleaning the price data
    product_price = product_price.replace('�', '')

    # Add product information to list
    all_products.append({"name": product_name, "price": product_price})

# Print all product information
for product in all_products:
    print("Product Name:", product["name"])
    print("Product Price:", product["price"])
    print("---")

# For debugging purposes, save the HTML source to a file
with open("output.html", "w", encoding="utf-8") as file:
    file.write(html_source)
