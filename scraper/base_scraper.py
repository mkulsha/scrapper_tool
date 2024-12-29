from abc import ABC, abstractmethod

class BaseScraper(ABC):
    def __init__(self, db_handler, proxy=None):
        self.db_handler = db_handler
        self.proxy = proxy

    @abstractmethod
    def scrape_catalogue(self, page_limit: int):
        """Scrape the catalogue based on the page limit."""
        pass