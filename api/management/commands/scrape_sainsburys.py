from django.core.management.base import BaseCommand
from api.models import Product, ProductPrice, Supermarket
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import bs4 as bs
import re
import os
import requests
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse

class Command(BaseCommand):
    help = 'Scrape data from Sainsbury\'s website'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting the Sainsbury's scraper...")
        self.scrape_sainsburys()

    def scrape_sainsburys(self):
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
                image_link = image_tag['src'] if image_tag else None

                # Determine weight based on specified conditions
                if 'Multipack' in name or 'Twin Pack' in name:
                    weight_match = multipack_regex.search(name)
                    weight = weight_match.group(0) if weight_match else None
                elif 'x' in name:
                    weight_match = x_number_regex.search(name)
                    weight = weight_match.group(0) if weight_match else None
                else:
                    weight_match = weight_regex.search(name)
                    weight = weight_match.group(1) if weight_match else None

                rating_tag = product.select_one('a.star-rating-link')
                if rating_tag:
                    # Attempt to extract the rating using regex
                    rating_result = rating_regex.search(rating_tag['aria-label'])
                    rating = f"{rating_result.group(1)} out of 5" if rating_result else None
                else:
                    rating = None

                # Extract other details
                reviews = product.select_one('span.reviews').text.strip() if product.select_one('span.reviews') else None
            
                nectar_price_tag = product.select_one('span.pt__cost--price')
                nectar_price = price_regex.search(nectar_price_tag.text).group() if nectar_price_tag and price_regex.search(nectar_price_tag.text) else None
                
                rrp_tag = product.select_one('span.pt__cost__retail-price')
                rrp = price_regex.search(rrp_tag.text).group() if rrp_tag and price_regex.search(rrp_tag.text) else None
                
                price_per_measure = product.select_one('span.pt__cost__unit-price-per-measure').text.strip()

                # Check if essential data is not None
                data_complete = all([name, link, image_link, weight, rrp])

                # Append product data to the list if data is complete
                if data_complete:
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
                else:
                    print(f"Incomplete data for product: {name}")

            except Exception as e:
                print(f"Error processing product: {e}")

        # Output the extracted data
        for item in product_data:
            print(item)


        def validate_product_data(product):
            # Check each field for the correct type and conditions
            if not isinstance(product.get('name'), str) or not product['name'].strip():
                return False, "Invalid or missing product name."
            if not isinstance(product.get('link'), str):
                return False, "Invalid or missing product link."
            if product.get('image_link') and not isinstance(product['image_link'], str):
                return False, "Invalid image link."
            if not isinstance(product.get('weight'), str) or not product['weight'].strip():
                return False, "Invalid or missing weight."
            if not isinstance(product.get('rrp'), (float, int)) and not product['rrp'].replace('.', '', 1).isdigit():
                return False, "Invalid RRP."
            if product.get('nectar_price') and not (isinstance(product['nectar_price'], (float, int)) and product['nectar_price'].replace('.', '', 1).isdigit()):
                return False, "Invalid Nectar price."
            if not isinstance(product.get('price_per_measure'), str) or not product['price_per_measure'].strip():
                return False, "Invalid or missing price per measure."

            return True, "Product data is valid."

        def save_image_from_url(product_name, url):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    image_io = BytesIO()
                    image.save(image_io, format='JPEG')
                    filename = f"{product_name.replace(' ', '_')}-Sainsburys.jpg"
                    filepath = os.path.join('product_image', filename)
                    with open(filepath, 'wb') as f:
                        f.write(image_io.getvalue())
                    return filepath
                else:
                    print(f"Failed to download image for {product_name}. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error saving image for {product_name}: {e}")



        def save_product_to_database(product_data):
            valid, message = validate_product_data(product_data)
            if not valid:
                print(f"Validation failed: {message}")
                return

            try:
                image_content = save_image_from_url(product_data['name'], product_data['image_link'])

                product, created = Product.objects.get_or_create(
                    product_name=product_data['name'],
                    supermarket_id=2,
                    defaults={
                        'product_weight': product_data['weight'],
                        'product_image_url': image_content,
                        'product_url': product_data['link'],
                        'groupproduct': None
                    }
                )

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

                latest_price = ProductPrice.objects.filter(product=product).order_by('-datetime_price_updated').first()

                nectar_price = product_data['nectar_price'] if product_data.get('nectar_price') is not None else None

                if latest_price:
                    latest_nectar_price = latest_price.loyalty_card_price
                else:
                    latest_nectar_price = None

                nectar_price_change = (float(latest_nectar_price) != float(nectar_price)) if latest_nectar_price is not None and nectar_price is not None else latest_nectar_price != nectar_price

                price_data_changed = (
                    not latest_price or
                    latest_price.rrp_price != float(product_data['rrp']) or
                    nectar_price_change
                )

                if price_data_changed:
                    new_price = ProductPrice(
                        product=product,
                        rrp_price=float(product_data['rrp']),
                        sale_price=None,
                        loyalty_card_price=float(nectar_price) if nectar_price is not None else None,
                        sale_deal=None,
                        loyalty_card_deal=None,
                        rrp_price_per_weight=product_data['price_per_measure'],
                        datetime_price_updated=timezone.now()
                    )
                    new_price.save()
                    print(f"Added new price for product: {product_data['name']}")
                else:
                    print("No price change, not updating price.")

                if created:
                    print(f"Saved new product: {product_data['name']}")
            except Exception as e:
                print(f"Error saving product '{product_data['name']}' to the database: {e}")

        for product in product_data:
            save_product_to_database(product)
