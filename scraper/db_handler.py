import json
import redis

class JSONDatabaseHandler:
    def __init__(self, db_file):
        self.db_file = db_file
        self.cache = redis.Redis(host="localhost", port=6379, decode_responses=True)

    def load_data(self):
        try:
            with open(self.db_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_data(self, data):
        with open(self.db_file, "w") as f:
            json.dump(data, f, indent=4)

    def save_product(self, product):
        """Save or update the product in the DB."""
        data = self.load_data()
        data.append(product)
        self.save_data(data)

    def is_data_updated(self, product):
        """Check if product price has changed using caching."""
        cached_price = self.cache.get(product["product_title"])
        if cached_price and float(cached_price) == product["product_price"]:
            return False  # No change
        self.cache.set(product["product_title"], product["product_price"])
        return True

    def notify(self, count):
        """Notify about scraping status."""
        print(f"Scraped and updated {count} products in the database.")