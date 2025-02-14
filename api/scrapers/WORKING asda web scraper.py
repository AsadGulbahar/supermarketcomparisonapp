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

# Wait for the product name container to load (up to 10 seconds)
try:
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'co-product__title'))
    WebDriverWait(browser, 1).until(element_present)
except Exception as e:
    print("Error waiting for product name container:", e)

# Get page source after waiting
html_source = browser.page_source
browser.quit()

soup = bs.BeautifulSoup(html_source, "html.parser")

# Extracting the product name
product_name_container = soup.find('h3', {'class': 'co-product__title'})
if product_name_container:
    product_name_element = product_name_container.find('a', {'data-auto-id': 'linkProductTitle'})
    if product_name_element:
        product_name = product_name_element.text.strip()
    else:
        product_name = "Product name link not found"
else:
    product_name = "Product name container not found"

# Extracting the product price
product_price_element = soup.find('strong', {'class': 'co-product__price'})
if product_price_element:
    product_price = product_price_element.text.strip()
else:
    product_price = "Not found"

print("Product Name:", product_name)
print("Product Price:", product_price)

# For debugging purposes, save the HTML source to a file
with open("output.html", "w", encoding="utf-8") as file:
    file.write(html_source)

# for each in 
# ():
    