import bs4 as bs
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Setup Chrome WebDriver
browser = webdriver.Chrome()

# Navigate to the URL
url = "https://groceries.morrisons.com/browse/food-cupboard-102705/biscuits-182321/sweet-biscuits-182325/chocolate-biscuits-182339?showOOS=true"
browser.get(url)

# Wait for the product list to load
try:
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'fops-shelf')))
except Exception as e:
    print("Error waiting for product data:", e)
    browser.quit()
    exit()

# Get the HTML source and close the browser
html_source = browser.page_source
browser.quit()

# Parse HTML with BeautifulSoup
soup = bs.BeautifulSoup(html_source, "html.parser")
products = soup.find('ul', {'class': 'fops-shelf'}).find_all('li', {'class': 'fops-item'})

all_products = []
price_regex = re.compile(r"\d+\.?\d*")  # Adjusted regular expression to match integer and decimal numbers

for product in products:
    data_complete = True
    try:
        # Extracting product details
        content_wrapper = product.find('div', {'class': 'fop-contentWrapper'})
        link_element = content_wrapper.find('a', href=True)
        link = "https://groceries.morrisons.com" + link_element['href'] if link_element else None
        
        image_element = product.find('img', {'class': 'fop-img'})
        image_url = "https://groceries.morrisons.com" + image_element['srcset'].split(",")[0].strip().split(" ")[0] if image_element and 'srcset' in image_element.attrs else None

        name_element = product.find('h4', {'class': 'fop-title'}).find('span', recursive=False)
        name = name_element.text.strip() if name_element else None
        
        weight_element = product.find('span', {'class': 'fop-catch-weight'})
        weight = weight_element.text.strip() if weight_element else None
        
        price_per_measure = product.find('span', {'class': 'fop-unit-price'}).text.strip()

        # Promo and price details
        promo_offer = content_wrapper.find('a', {'class': 'fop-row-promo promotion-offer'})
        regular_price = None
        if promo_offer and 'Buy' in promo_offer.text:
            promo_deal = promo_offer.text.strip()
            regular_price = product.find('span', {'class': 'fop-price'}).text.strip()
            sale_price = None
        elif promo_offer:
            promo_deal = None
            regular_price = product.find('span', {'class': 'fop-old-price'}).text.strip()
            sale_price = product.find('span', {'class': 'fop-price price-offer'}).text.strip()
        else:
            promo_deal = None
            regular_price = product.find('span', {'class': 'fop-price'}).text.strip()
            sale_price = None

        # Extracting only decimal numbers
        regular_price = price_regex.search(regular_price).group() if price_regex.search(regular_price) else None
        sale_price = price_regex.search(sale_price).group() if sale_price != None and price_regex.search(sale_price) else sale_price

        # Check for missing essential data
        if not all([link, image_url, weight, regular_price]):
            data_complete = False

        all_products.append({
            'name': name,
            'weight': weight,
            'link': link,
            'image_url': image_url,
            'regular_price': regular_price,
            'sale_price': sale_price,
            'price_per_measure': price_per_measure,
            'promo_deal': promo_deal,
            'data_complete': data_complete
        })

    except Exception as e:
        print(f"Error processing product: {e}")

# Output the data
for product in all_products:
    print(product)
    print("\n")




# Now attempt to import your Django models
from api.models import Product, ProductPrice, Supermarket, Category

from django.core.files.base import ContentFile
import requests
from PIL import Image
from io import BytesIO
from django.db.models import Q
from django.utils import timezone

def save_image_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image_io = BytesIO()
        image.save(image_io, format='JPEG')  # Consider adjusting format based on the source image
        return ContentFile(image_io.getvalue())
    return None

def save_product_to_database(product_data):
    if product_data['data_complete']:
        image_content = save_image_from_url(product_data['image_url']) if product_data['image_url'] else None

        # Retrieve or create the Product instance
        product, created = Product.objects.get_or_create(
            product_name=product_data['name'],
            supermarket_id=4,  # Assuming supermarket ID for Morrisons is 4
            defaults={
                'product_weight': product_data['weight'],
                'product_image_url': image_content,
                'product_url': product_data['link'],
                'groupproduct': None
            }
        )

        # Update the product if it already exists and has changes
        if not created:
            update_fields = []
            if product.product_weight != product_data['weight']:
                product.product_weight = product_data['weight']
                update_fields.append('product_weight')
            if product.product_url != product_data['link']:
                product.product_url = product_data['link']
                update_fields.append('product_url')
            if image_content and product.product_image_url != image_content:
                product.product_image_url = image_content
                update_fields.append('product_image_url')
            if update_fields:
                product.save(update_fields=update_fields)
                print(f"Updated product: {product_data['name']}")

        # Check and update/create ProductPrice
        latest_price = ProductPrice.objects.filter(product=product).order_by('-datetime_price_updated').first()
        price_data_changed = (
            not latest_price or
            latest_price.rrp_price != float(product_data['regular_price']) or
            (latest_price.sale_price or 0) != float(product_data.get('sale_price', 0)) or
            latest_price.sale_deal != (product_data['promo_deal'] or None)
        )
        if price_data_changed:
            new_price = ProductPrice(
                product=product,
                rrp_price=float(product_data['regular_price']),
                sale_price=float(product_data.get('sale_price', 0)) or None,  # Assuming sale_price is optional
                loyalty_card_price = None,
                sale_deal = product_data['promo_deal'] or None,
                loyalty_card_deal = None,
                datetime_price_updated=timezone.now()
            )
            new_price.save()
            print(f"Added new price for product: {product_data['name']}")
        else:
            print("No price change, not updating price.")

        if created:
            print(f"Saved new product: {product_data['name']}")
    else:
        print("Incomplete product data, skipping.")

# Assuming 'all_products' is populated as before
for product in all_products:
    save_product_to_database(product)
