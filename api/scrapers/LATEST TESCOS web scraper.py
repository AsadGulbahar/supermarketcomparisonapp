import bs4 as bs
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Setup Chrome WebDriver
browser = webdriver.Chrome()

# Navigate to the URL
url = "https://www.tesco.com/groceries/en-GB/shop/food-cupboard/biscuits-and-cereal-bars/chocolate-biscuits-and-jaffa-cakes"
browser.get(url)

# Wait for the page elements to load
try:
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-list')))
except Exception as e:
    print("Error waiting for product data:", e)
    browser.quit()
    exit()

# Get the HTML source and quit the browser
html_source = browser.page_source
browser.quit()

# Save the HTML source for offline inspection (optional)
with open('tesco_page_source.html', 'w', encoding='utf-8') as file:
    file.write(html_source)

# Parse the HTML with BeautifulSoup
soup = bs.BeautifulSoup(html_source, "html.parser")
product_data = []

# Regular expression to extract decimal numbers and weight
decimal_pattern = re.compile(r"\d+\.\d+(/\w+)?")
first_number_pattern = re.compile(r'\d+.*')

# Iterate over each product and extract details
for product in soup.select('ul.product-list > li'):
    try:
        # Extract the title located within <div class="product-details--wrapper"> <h3><a><span>
        title_tag = product.select_one("div.product-details--wrapper h3 a span")
        title = title_tag.get_text(strip=True) if title_tag else "Title not found"

        weight_match = first_number_pattern.search(title)
        weight = weight_match.group(0) if weight_match else "Weight not specified"

        # Extract the product link
        link_tag = product.select_one("div.product-details--wrapper h3 a")
        link = link_tag['href'] if link_tag else "Link not found"

        # Extracting image URL from srcset
        image_tag = product.select_one("div.product-image__container img")
        image_url = image_tag['srcset'].split(",")[0].strip().split(" ")[0] if image_tag and image_tag['srcset'] else "Image not found"

        # Extract regular price (RRP)
        rrp_tag = product.select_one("p.styled__StyledHeading-sc-119w3hf-2")
        rrp = decimal_pattern.search(rrp_tag.get_text(strip=True)).group() if rrp_tag and decimal_pattern.search(rrp_tag.get_text(strip=True)) else "RRP not found"
        
        # Extract price per measure
        ppm_tag = product.select_one("p.styled__StyledFootnote-sc-119w3hf-7")
        price_per_measure = decimal_pattern.search(ppm_tag.get_text(strip=True)).group() if ppm_tag and decimal_pattern.search(ppm_tag.get_text(strip=True)) else "Price per measure not found"

        # Extract clubcard price, if available
        cc_price_tag = product.select_one("span.offer-text")
        clubcard_price = decimal_pattern.search(cc_price_tag.get_text(strip=True)).group() if cc_price_tag and decimal_pattern.search(cc_price_tag.get_text(strip=True)) else "No Clubcard price available"
        
        # Extract clubcard price per measure, if available
        cc_ppm_tag = product.select_one("span.offer-secondary-text")
        clubcard_price_per_measure = decimal_pattern.search(cc_ppm_tag.get_text(strip=True)).group() if cc_ppm_tag and decimal_pattern.search(cc_ppm_tag.get_text(strip=True)) else "No Clubcard price per measure available"

        # Extract clubcard promo deal, if available
        promo_tag = product.select_one("span.offer-text")
        promo_deal = promo_tag.get_text(strip=True) if promo_tag else "No promo deal available"

        # Append all data to the list
        product_data.append({
            'title': title,
            'weight': weight,
            'link': "https://www.tesco.com" + link,
            'image_url': image_url,
            'rrp': rrp,
            'price_per_measure': price_per_measure,
            'clubcard_price': clubcard_price,
            'clubcard_price_per_measure': clubcard_price_per_measure,
            'promo_deal': promo_deal 
        })

    except Exception as e:
        print(f"Error processing product: {e}")

# Output the extracted data
for item in product_data:
    print(item)
    print("")