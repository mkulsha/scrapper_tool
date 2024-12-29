from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from scraper.dental_scraper import DentalScraper
from scraper.db_handler import JSONDatabaseHandler
import os

# Create FastAPI app
app = FastAPI()

# Static token for authentication
STATIC_TOKEN = "secure-static-token"

# Authentication dependency
security = HTTPBearer()

def authenticate(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != STATIC_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")

@app.post("/scrape")
def scrape_catalogue(
    page_limit: int = 5,
    proxy: str = None,
    auth: HTTPAuthorizationCredentials = Depends(authenticate),
):
    """Endpoint to trigger scraping."""
    db_handler = JSONDatabaseHandler("products.json")
    scraper = DentalScraper(db_handler=db_handler, proxy=proxy)
    total_scraped = scraper.scrape_catalogue(page_limit=page_limit)
    return {"message": f"Scraped {total_scraped} products successfully!"}