import requests
from bs4 import BeautifulSoup
from scraper.base_scraper import BaseScraper
from scraper.utils import retry
import os
import shutil

class DentalScraper(BaseScraper):
    BASE_URL = "https://dentalstall.com/shop/"

    def __init__(self, db_handler, proxy=None):
        super().__init__(db_handler, proxy)
        self.headers = {"User-Agent": "Mozilla/5.0"}

    @retry(max_retries=3, delay=5)
    def fetch_page(self, url):
        """Fetch a single page with retry logic."""
        proxies = {"http": self.proxy, "https": self.proxy} if self.proxy else None
        response = requests.get(url, headers=self.headers, proxies=proxies)
        response.raise_for_status()
        return response.text

    def save_image(self, image_url, product_name):
        """Download and save the product image."""
        response = requests.get(image_url, stream=True)
        filename = f"images/{product_name.replace(' ', '_')}.jpg"
        with open(filename, "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)
        return filename

    def scrape_catalogue(self, page_limit: int):
        """Scrape the product catalogue."""
        total_scraped = 0
        os.makedirs("images", exist_ok=True)

        for page in range(1, page_limit + 1):
            url = f"{self.BASE_URL}/page/{page}"
            page_content = self.fetch_page(url)
            soup = BeautifulSoup(page_content, "html.parser")
            products = soup.select(".product")

            for product in products:
                name = product.select_one(".product-title").text.strip()
                price = float(product.select_one(".product-price").text.strip().replace("₹", ""))
                image_url = product.select_one(".product-image img")["src"]

                # Save the product image
                image_path = self.save_image(image_url, name)

                # Check if data has changed
                product_data = {"product_title": name, "product_price": price, "path_to_image": image_path}
                if not self.db_handler.is_data_updated(product_data):
                    continue

                # Save product to DB
                self.db_handler.save_product(product_data)
                total_scraped += 1

        self.db_handler.notify(total_scraped)
        return total_scraped
