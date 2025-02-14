# from django.core.management.base import BaseCommand
# import bs4 as bs
# import re
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from api.models import Product, ProductPrice, Supermarket, Category
# from django.core.files.base import ContentFile
# from PIL import Image
# from io import BytesIO
# from django.utils import timezone
# import os
# import requests

# class Command(BaseCommand):
#     help = 'Scrape data from Asda website'

#     def handle(self, *args, **kwargs):
#         self.stdout.write("Starting the Asda scraper...")
#         self.scrape_asda()

#     def scrape_asda(self):
#         import bs4 as bs
#         import re
#         from selenium import webdriver
#         from selenium.webdriver.support.ui import WebDriverWait
#         from selenium.webdriver.support import expected_conditions as EC
#         from selenium.webdriver.common.by import By

#         # Setup Chrome WebDriver
#         browser = webdriver.Chrome()

#         # Navigate to the URL
#         url = "https://groceries.asda.com/aisle/fruit-veg-flowers/fruit/apples/1215686352935-910000975210-1215666691670"
#         browser.get(url)

#         # Accept cookies if needed
#         try:
#             WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
#         except Exception as e:
#             print("Cookies button not found or not clickable:", e)

#         # Wait for the product listings to load
#         try:
#             WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'co-product-list')))
#         except Exception as e:
#             print("Error waiting for product data:", e)
#             browser.quit()
#             exit()

#         # Get the HTML source
#         html_source = browser.page_source
#         browser.quit()

#         # Parse HTML with BeautifulSoup
#         soup = bs.BeautifulSoup(html_source, "html.parser")
#         product_list = soup.find('div', class_='co-product-list')
#         product_containers = product_list.find_all('div', {'class': 'co-product'}) if product_list else []

#         all_products = []
#         product_index = 1
#         noOfFailImage = 1

#         for container in product_containers:
#             try:
#                 name_element = container.find('a', {'data-auto-id': 'linkProductTitle'})
#                 name = name_element.text.strip() if name_element else None
#                 link = "https://groceries.asda.com" + name_element['href'] if name_element else None
                
#                 # Enhanced image extraction logic
#                 picture_element = container.find('picture', {'class': 'asda-image'})
#                 image_element = picture_element.find('img') if picture_element else None
#                 source_element = picture_element.find('source') if picture_element else None
                
#                 if image_element and image_element.get('src'):
#                     image_url = image_element.get('src')
#                 elif source_element and source_element.get('srcset'):
#                     image_url = source_element.get('srcset').split(",")[0].split(" ")[0]
#                 else:
#                     image_url = None
#                     noOfFailImage += 1

#                 # Extracting weight/volume
#                 volume_tag = container.find('div', {'class': 'co-item__volume-container'}).find('span', {'class': 'co-product__volume'})
#                 weight = volume_tag.text.strip() if volume_tag else None

#                 price_info = container.find('div', {'class': 'co-item__price-container'})
#                 was_price_tag = price_info.find('span', {'class': 'co-product__was-price'})
#                 sale_price_tag = price_info.find('strong', {'class': 'co-product__price'})
#                 rrp = re.search(r"\d+\.\d+", was_price_tag.text.strip()).group() if was_price_tag else \
#                     (re.search(r"\d+\.\d+", sale_price_tag.text.strip()).group() if sale_price_tag else None)
#                 sale_price = re.search(r"\d+\.\d+", sale_price_tag.text.strip()).group() if sale_price_tag and was_price_tag else None
                
#                 promo_tag = container.find('div', {'class': 'link-save-banner-large__meat-sticker'})
#                 promo_parts = promo_tag.find_all('span', class_='link-save-banner-large__config') if promo_tag else []
#                 promo_text = ''.join([part.text for part in promo_parts]).replace('�', '£') if promo_parts else None
                
#                 price_per_measure_tag = price_info.find('span', {'class': 'co-product__price-per-uom'})
#                 price_per_measure = price_per_measure_tag.text.strip() if price_per_measure_tag else None

#                 # Check if essential information is not None
#                 data_complete = all([name, link, image_url, weight, rrp])

#                 all_products.append({
#                     'name': name,
#                     'link': link,
#                     'image_url': image_url,
#                     'rrp': rrp,
#                     'sale_price': sale_price,
#                     'promo_deal': promo_text,
#                     'price_per_measure': price_per_measure,
#                     'weight': weight,
#                     'data_complete': data_complete
#                 })
#             except Exception as e:
#                 print(f"Error processing Product {product_index} ({name if 'name' in locals() else 'Unknown'}): {e}")
            
#             product_index += 1  # Increment the product index

#         # Output extracted data
#         for product in all_products:
#             print(product)
#             print(" ")

#         print("Finished processing all products.")
#         print("Number of failed image: " + str(noOfFailImage))

#         #  import Django models
#         from api.models import Product, ProductPrice, Supermarket, Category

#         from django.core.files.base import ContentFile
#         import requests
#         from PIL import Image
#         from io import BytesIO
#         from django.db.models import Q
#         from django.utils import timezone

       
#         def save_image_from_url(product_name, url):
#             try:
#                 response = requests.get(url)
#                 if response.status_code == 200:
#                     image = Image.open(BytesIO(response.content))
#                     image_io = BytesIO()
#                     image.save(image_io, format='JPEG')
#                     filename = f"{product_name.replace(' ', '_')}-Asda.jpg"
#                     filepath = os.path.join('product_image', filename)
#                     with open(filepath, 'wb') as f:
#                         f.write(image_io.getvalue())
#                     return filepath
#                 else:
#                     print(f"Failed to download image for {product_name}. Status code: {response.status_code}")
#             except Exception as e:
#                 print(f"Error saving image for {product_name}: {e}")



        
#         def save_product_to_database(self, product_data):
#             try:
#                 if product_data['data_complete']:
#                     image_content = save_image_from_url(product_data['name'], product_data['image_url'])

#                     product, created = Product.objects.get_or_create(
#                         product_name=product_data['name'],
#                         supermarket_id=3,
#                         defaults={
#                             'product_weight': product_data['weight'],
#                             'product_image_url': image_content,
#                             'product_url': product_data['link'],
#                             'groupproduct': None
#                         }
#                     )

#                     if not created:
#                         update_fields = []
#                         if product.product_weight != product_data['weight']:
#                             product.product_weight = product_data['weight']
#                             update_fields.append('product_weight')
#                         if product.product_url != product_data['link']:
#                             product.product_url = product_data['link']
#                             update_fields.append('product_url')
#                         if image_content and product.product_image_url != image_content:
#                             product.product_image_url = image_content
#                             update_fields.append('product_image_url')
#                         if update_fields:
#                             product.save(update_fields=update_fields)
#                             print(f"Updated product: {product_data['name']}")

#                     latest_price = ProductPrice.objects.filter(product=product).order_by('-datetime_price_updated').first()

#                     sale_price = product_data['sale_price'] if product_data.get('sale_price') is not None else None

#                     if latest_price:
#                         latest_sale_price = latest_price.sale_price
#                     else:
#                         latest_sale_price = None

#                     if latest_sale_price is not None and sale_price is not None:
#                         sale_price_change = float(latest_sale_price) != float(sale_price)
#                     else:
#                         sale_price_change = latest_sale_price != sale_price

#                     price_data_changed = (
#                         not latest_price or
#                         latest_price.rrp_price != float(product_data['regular_price']) or
#                         sale_price_change or
#                         latest_price.sale_deal != (product_data['promo_deal'] or None)
#                     )

#                     if price_data_changed:
#                         new_price = ProductPrice(
#                             product=product,
#                             rrp_price=float(product_data['regular_price']),
#                             sale_price=float(product_data['sale_price']) if product_data.get('sale_price') is not None else None,
#                             loyalty_card_price=None,
#                             sale_deal=product_data['promo_deal'] or None,
#                             loyalty_card_deal=None,
#                             rrp_price_per_weight = product_data[price_per_measure],
#                             datetime_price_updated=timezone.now()
#                         )
#                         new_price.save()
#                         print(f"Added new price for product: {product_data['name']}")
#                     else:
#                         print("No price change, not updating price.")

#                     if created:
#                         print(f"Saved new product: {product_data['name']}")
#                 else:
#                     print("Incomplete product data, skipping.")
#             except Exception as e:
#                 print(f"Error saving product '{product_data['name']}' to the database: {e}")

#         for product in all_products:
#             save_product_to_database(product)


from django.core.management.base import BaseCommand
from api.models import Product, ProductPrice, Supermarket
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import bs4 as bs
import requests
from PIL import Image
from io import BytesIO
import os

class Command(BaseCommand):
    help = 'Scrape data from Asda website'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting the Asda scraper...")
        self.scrape_asda()

    def scrape_asda(self):
        browser = webdriver.Chrome()
        url = "https://groceries.asda.com/aisle/fruit-veg-flowers/fruit/apples/1215686352935-910000975210-1215666691670"
        browser.get(url)

        try:
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
        except Exception as e:
            self.stdout.write("Cookies button not found or not clickable: {}".format(e))

        try:
            WebDriverWait(browser, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'co-product-list')))
            html_source = browser.page_source
            browser.quit()
            self.process_products(html_source)
        except Exception as e:
            browser.quit()
            self.stdout.write("Error waiting for product data: {}".format(e))

    def process_products(self, html_source):
        soup = bs.BeautifulSoup(html_source, "html.parser")
        product_containers = soup.find_all('div', class_='co-product')
        for container in product_containers:
            product_data = self.extract_product_data(container)
            if product_data['data_complete']:
                self.save_product_to_database(product_data)

    def extract_product_data(self, container):
        name = container.find('a', {'data-auto-id': 'linkProductTitle'}).text.strip()
        link = "https://groceries.asda.com" + container.find('a', {'data-auto-id': 'linkProductTitle'})['href']
        image_element = container.find('img', {'class': 'co-product__image'})
        image_url = image_element['src'] if image_element else None
        price = container.find('strong', {'class': 'co-product__price'}).text.strip()

        return {
            'name': name,
            'link': link,
            'image_url': image_url,
            'price': price,
            'data_complete': all([name, link, image_url, price])
        }

    def save_product_to_database(self, product_data):
        image_path = self.save_image_from_url(product_data['name'], product_data['image_url'])
        supermarket, _ = Supermarket.objects.get_or_create(name='Asda')
        product, created = Product.objects.update_or_create(
            name=product_data['name'],
            defaults={
                'supermarket': supermarket,
                'link': product_data['link'],
                'product_image': image_path,
                'price': product_data['price']
            }
        )
        self.stdout.write('{} product: {}'.format('Created' if created else 'Updated', product['name']))

    def save_image_from_url(self, product_name, url):      
        try:
            response = requests.get(url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                filename = f"{product_name.replace(' ', '_')}-Asda.jpg"  
                filepath = os.path.join('product_images', filename) 
                image.save(filepath, 'JPEG')
                return os.path.join('product_images', filename) 
            else:
                self.stdout.write(f"Failed to download image for {product_name}. Status code: {response.status_code}")
        except Exception as e:
            self.stdout.write(f"Error saving image for {product_name}: {e}")
