from fastapi import FastAPI, Query
from scraper import scrap_meshoo

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI deployed successfully!"}

@app.get("/scrape")
def scrape(
    base_url: str = Query(..., description="Base URL to scrape"),
    pages: int = Query(1, description="Number of pages to scrape")
) -> dict:
    return scrap_meshoo(base_url=base_url, pages=pages)