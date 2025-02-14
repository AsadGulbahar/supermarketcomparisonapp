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
    help = 'Scrape data from Tesco website'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting the Tesco's scraper...")
        self.scrape_tesco()

    def scrape_tesco(self):
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
                title = title_tag.get_text(strip=True) if title_tag else None

                weight_match = first_number_pattern.search(title)
                weight = weight_match.group(0) if weight_match else None

                # Extract the product link
                link_tag = product.select_one("div.product-details--wrapper h3 a")
                link = "https://www.tesco.com" + link_tag['href'] if link_tag else None

                # Extracting image URL from srcset
                image_tag = product.select_one("div.product-image__container img")
                image_url = image_tag['srcset'].split(",")[0].strip().split(" ")[0] if image_tag and image_tag['srcset'] else None

                # Extract regular price (RRP)
                rrp_tag = product.select_one("p.styled__StyledHeading-sc-119w3hf-2")
                rrp = decimal_pattern.search(rrp_tag.get_text(strip=True)).group() if rrp_tag and decimal_pattern.search(rrp_tag.get_text(strip=True)) else None
                
                # Extract price per measure
                ppm_tag = product.select_one("p.styled__StyledFootnote-sc-119w3hf-7")
                price_per_measure = decimal_pattern.search(ppm_tag.get_text(strip=True)).group() if ppm_tag and decimal_pattern.search(ppm_tag.get_text(strip=True)) else None

                # Extract clubcard price, if available
                cc_price_tag = product.select_one("span.offer-text")
                clubcard_price = decimal_pattern.search(cc_price_tag.get_text(strip=True)).group() if cc_price_tag and decimal_pattern.search(cc_price_tag.get_text(strip=True)) else None
                
                # Extract clubcard price per measure, if available
                cc_ppm_tag = product.select_one("span.offer-secondary-text")
                clubcard_price_per_measure = decimal_pattern.search(cc_ppm_tag.get_text(strip=True)).group() if cc_ppm_tag and decimal_pattern.search(cc_ppm_tag.get_text(strip=True)) else None

                # Extract clubcard promo deal, if available
                promo_tag = product.select_one("span.offer-text")
                promo_deal = promo_tag.get_text(strip=True) if promo_tag else None

                data_complete = all([title, weight, link, image_url, rrp, price_per_measure])


                # Append all data to the list
                product_data.append({
                    'title': title,
                    'weight': weight,
                    'link': link,
                    'image_url': image_url,
                    'rrp': rrp,
                    'price_per_measure': price_per_measure,
                    'clubcard_price': clubcard_price,
                    'clubcard_price_per_measure': clubcard_price_per_measure,
                    'promo_deal': promo_deal ,
                    'data_complete' : data_complete
                })

            except Exception as e:
                print(f"Error processing product: {e}")

        # Output the extracted data
        for item in product_data:
            print(item)
            print("")



        def save_image_from_url(product_name, url):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    image_io = BytesIO()
                    image.save(image_io, format='JPEG')
                    filename = f"{product_name.replace(' ', '_')}-Tesco.jpg"
                    filepath = os.path.join('product_image', filename)
                    with open(filepath, 'wb') as f:
                        f.write(image_io.getvalue())
                    return filepath
                else:
                    print(f"Failed to download image for {product_name}. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error saving image for {product_name}: {e}")


        def save_product_to_database(product_data):
            if product_data['data_complete']:
                image_content = save_image_from_url(product_data['title'], product_data['image_url']) if product_data['image_url'] else None

                # Retrieve or create the Product instance
                product, created = Product.objects.get_or_create(
                    product_name=product_data['title'],
                    supermarket_id=4, 
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
                        print(f"Updated product: {product_data['title']}")

                # Check and update/create ProductPrice
                latest_price = ProductPrice.objects.filter(product=product).order_by('-datetime_price_updated').first()

                clubcard_price = product_data['clubcard_price'] if product_data.get('clubcard_price') is not None else None

                if latest_price:
                    latest_clubcard_price = latest_price.loyalty_card_price
                else:
                    latest_clubcard_price = None

                clubcard_price_change = (float(latest_clubcard_price) != float(clubcard_price)) if latest_clubcard_price is not None and clubcard_price is not None else latest_clubcard_price != clubcard_price

                price_data_changed = (
                    not latest_price or
                    latest_price.rrp_price != float(product_data['rrp']) or
                    clubcard_price_change
                )

                if price_data_changed:
                    new_price = ProductPrice(
                        product=product,
                        rrp_price=float(product_data['rrp']),
                        sale_price = None,
                        loyalty_card_price = clubcard_price_change or None,
                        sale_deal = None,
                        loyalty_card_deal = promo_deal or None,
                        rrp_price_per_weight = price_per_measure,
                        datetime_price_updated=timezone.now()
                    )
                    new_price.save()
                    print(f"Added new price for product: {product_data['title']}")
                else:
                    print("No price change, not updating price.")

                if created:
                    print(f"Saved new product: {product_data['title']}")
            else:
                print("Incomplete product data, skipping.")

        # Assuming 'all_products' is populated as before
        for product in product_data:
            save_product_to_database(product)

