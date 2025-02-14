from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bs4 as bs
import time
import re

# Initialize webdriver
driver = webdriver.Chrome()

# Function to navigate pages and extract data
def scrape_data(url):
    driver.get(url)
    product_data = []
    
    # Wait for initial elements to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-list')))
    
    # Click on "Show 48 per page" if available
    try:
        show_more_link = driver.find_element_by_partial_link_text("Show 48 per page")
        show_more_link.click()
        # Wait for the page to refresh and show more products per page
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-list')))
    except Exception as e:
        print("Could not click 'Show 48 per page':", e)

    while True:
        # Refresh page source and use BeautifulSoup if needed
        soup = bs.BeautifulSoup(driver.page_source, 'html.parser')

        # Regular expression to extract decimal numbers followed by units
        decimal_pattern = re.compile(r"\d+\.\d+(/\w+)?")

   
        for product in soup.select('ul.product-list > li'):
            try:
                # Extract the title located within <div class="product-details--wrapper"> <h3><a><span>
                title_tag = product.select_one("div.product-details--wrapper h3 a span")
                title = title_tag.get_text(strip=True) if title_tag else "Title not found"

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
        
        # Find the 'Next' button, check if it is not disabled and contains the specified icon
        try:
            next_button = driver.find_element_by_xpath("//a[contains(@class, 'next') and not(contains(@class, 'disabled')) and .//span[contains(@class, 'icon-icon_whitechevronright')]]")
            next_button.click()
            time.sleep(2)  # Wait for page to load
        except Exception as e:
            print("No more pages to load or specific 'Next' button not found:", e)
            break

    return product_data

# URL setup
url = "https://www.tesco.com/groceries/en-GB/shop/fresh-food/fresh-fruit/dried-fruit-nuts-and-seeds"
result = scrape_data(url)
print(result)

# Cleanup
driver.quit()
