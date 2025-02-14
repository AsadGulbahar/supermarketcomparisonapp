# import bs4 as bs
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By

# # Set up Chrome WebDriver
# browser = webdriver.Chrome()

# # Navigate to the URL
# url = "https://www.sainsburys.co.uk/gol-ui/groceries/fruit-and-vegetables/fresh-fruit/apples/c:1034099"
# browser.get(url)

# # Explicitly wait for product details to load and ignore placeholders
# try:
#     # Wait for the presence of a product name element that signifies data has loaded
#     element_present = EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h2.pt__info__description a'))
#     WebDriverWait(browser, 20).until(element_present)
# except Exception as e:
#     print("Error waiting for product data:", e)
#     browser.quit()
#     exit()

# # Get the page source and quit browser
# html_source = browser.page_source
# browser.quit()

# # Save the HTML to a file for inspection (optional)
# with open('page_source.html', 'w', encoding='utf-8') as file:
#     file.write(html_source)

# # Parse the HTML
# soup = bs.BeautifulSoup(html_source, "html.parser")
# product_data = []

# # Process each product
# products = soup.select('ul.ln-o-grid.ln-o-grid--matrix.ln-o-grid--equal-height > li')
# for product in products:
#     name_tag = product.select_one('h2.pt__info__description a')
#     if not name_tag:
#         continue  # Skip placeholder items
#     name = name_tag.text.strip()
#     link = name_tag['href']
#     rating_tag = product.select_one('div.star-rating-link')
#     rating = rating_tag['aria-label'].split(',')[0] if rating_tag else "No rating available"
#     reviews_tag = product.select_one('span.reviews')
#     reviews = reviews_tag.text.strip() if reviews_tag else "No reviews"
#     nectar_price_tag = product.select_one('span.pt__cost--price')
#     nectar_price = nectar_price_tag.text.strip() if nectar_price_tag else "No Nectar price available"
#     rrp = product.select_one('span.pt__cost__retail-price').text.strip()
#     price_per_measure = product.select_one('span.pt__cost__unit-price-per-measure').text.strip()

#     product_data.append({
#         'name': name,
#         'link': link,
#         'rating': rating,
#         'reviews': reviews,
#         'nectar_price': nectar_price,
#         'rrp': rrp,
#         'price_per_measure': price_per_measure
#     })

# # Print collected data
# for item in product_data:
#     print(item)



import bs4 as bs
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Setup Chrome WebDriver
browser = webdriver.Chrome()

# Navigate to the URL
url = "https://www.sainsburys.co.uk/gol-ui/groceries/food-cupboard/biscuits-and-crackers/biscuits/all-biscuits/c:1043010"
browser.get(url)

# Wait for the page elements to load
try:
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.pt__info__description a')))
except Exception as e:
    print("Error waiting for product data:", e)
    browser.quit()
    exit()

# Get the HTML source and quit the browser
html_source = browser.page_source
browser.quit()

# Save the HTML source for offline inspection (optional)
with open('page_source.html', 'w', encoding='utf-8') as file:
    file.write(html_source)

# Parse the HTML with BeautifulSoup
soup = bs.BeautifulSoup(html_source, "html.parser")
product_data = []

# Regex pattern to extract rating and price
rating_regex = re.compile(r"(\d+\.\d+) out of 5")
price_regex = re.compile(r"\d+\.\d+|\d+")
multipack_regex = re.compile(r'(Multipack|Twin Pack)\s*(.*)', re.IGNORECASE)
x_number_regex = re.compile(r'x\s*\d+')
weight_regex = re.compile(r'(\d+\s*[a-zA-Z]+)$')

# Iterate over each product and extract details
for product in soup.select('ul.ln-o-grid.ln-o-grid--matrix.ln-o-grid--equal-height > li'):
    try:
        name = product.select_one('h2.pt__info__description a').text.strip()
        link = product.select_one('h2.pt__info__description a')['href']
        image_tag = product.select_one('img[data-test-id="pt-image"]')
        image_link = image_tag['src'] if image_tag else "No image available"

        # Determine weight based on specified conditions
        if 'Multipack' in name or 'Twin Pack' in name:
            weight_match = multipack_regex.search(name)
            weight = weight_match.group(0) if weight_match else "Weight not specified"
        elif 'x' in name:
            weight_match = x_number_regex.search(name)
            weight = weight_match.group(0) if weight_match else "Weight not specified"
        else:
            weight_match = weight_regex.search(name)
            weight = weight_match.group(1) if weight_match else "Weight not specified"


        rating_tag = product.select_one('a.star-rating-link')
        if rating_tag:
            # Attempt to extract the rating using regex
            rating_result = rating_regex.search(rating_tag['aria-label'])
            rating = f"{rating_result.group(1)} out of 5" if rating_result else "Rating format not matched"
        else:
            rating = "Rating tag not found"

        # Extract other details
        reviews = product.select_one('span.reviews').text.strip() if product.select_one('span.reviews') else "No reviews"
       
        nectar_price_tag = product.select_one('span.pt__cost--price')
        nectar_price = price_regex.search(nectar_price_tag.text).group() if nectar_price_tag and price_regex.search(nectar_price_tag.text) else "No Nectar price available"
        
        rrp_tag = product.select_one('span.pt__cost__retail-price')
        rrp = price_regex.search(rrp_tag.text).group() if rrp_tag and price_regex.search(rrp_tag.text) else "RRP not found"
        
        price_per_measure = product.select_one('span.pt__cost__unit-price-per-measure').text.strip()

      
        # Append product data to the list
        product_data.append({
            'name': name,
            'link': link,
            'image_link': image_link,
            'rating': rating,
            'reviews': reviews,
            'nectar_price': nectar_price,
            'rrp': rrp,
            'price_per_measure': price_per_measure,
            'weight' : weight
        })
    except Exception as e:
        print(f"Error processing product: {e}")

# Output the extracted data
for item in product_data:
    print(item)
    print("")