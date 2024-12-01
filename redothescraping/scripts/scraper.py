from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from config import BASE_URL, WEBDRIVER_PATH, PAGE_LOAD_TIMEOUT, MAX_PAGES
from utils import save_to_csv
import time

# Initialize WebDriver
def initialize_driver():
    service = Service(WEBDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver

# Scrape listings
def scrape_listings(driver, max_pages):
    listings = []
    page_number = 1

    while True:
        print(f"Scraping page {page_number}...")
        driver.get(f"{BASE_URL}?page={page_number}")
        time.sleep(3)  # Let the page load

        # Find all listing elements using XPath
        items = driver.find_elements(By.XPATH, "//div[contains(@class, 'listing-item-class')]")  # Replace with actual XPath

        for item in items:
            try:
                # Use XPath to locate and extract the required fields
                title = item.find_element(By.XPATH, ".//h2[contains(@class, 'title-class')]").text  # Replace with actual XPath
                price = item.find_element(By.XPATH, ".//span[contains(@class, 'price-class')]").text  # Replace with actual XPath
                rooms = item.find_element(By.XPATH, ".//span[contains(@class, 'rooms-class')]").text  # Replace with actual XPath
                baths = item.find_element(By.XPATH, ".//span[contains(@class, 'baths-class')]").text  # Replace with actual XPath
                area = item.find_element(By.XPATH, ".//span[contains(@class, 'area-class')]").text  # Replace with actual XPath
                link = item.find_element(By.XPATH, ".//a").get_attribute("href")

                # Clean and append the data
                listings.append({
                    "title": title,
                    "price": price,
                    "nb_rooms": int(rooms),
                    "nb_baths": int(baths),
                    "surface_area": float(area.replace("m²", "").strip()),
                    "link": link,
                })
            except Exception as e:
                print(f"Error scraping a listing: {e}")

        # Break if we've reached the max pages
        if max_pages and page_number >= max_pages:
            break

        # Check if there's a "next" page
        try:
            next_button = driver.find_element(By.XPATH, "//a[contains(@class, 'next-button-class')]")  # Replace with actual XPath
            next_button.click()
            page_number += 1
        except:
            print("No more pages to scrape.")
            break

    return listings

# Main function
def main():
    driver = initialize_driver()

    try:
        listings = scrape_listings(driver, MAX_PAGES)
        save_to_csv(listings, "data/extracted/avito_listings.csv")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()