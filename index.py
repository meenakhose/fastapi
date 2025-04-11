'''from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from typing import Annotated, Optional, Dict
from scraper import scrap_meshoo

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI deployed successfully!"}

@app.get("/scrape")
def scrape(
    base_url: Annotated[str, Query(description="Base URL to scrape")],
    pages: Annotated[int, Query(1, description="Number of pages to scrape")],
) -> Dict:
    return scrap_meshoo(base_url=base_url, pages=pages)'''
from typing import Annotated
from fastapi import FastAPI, Query
from scraper import scrap_meshoo

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI deployed successfully!"}

@app.get("/scrape")
def scrape(
    base_url: Annotated[str, Query(description="Base URL to scrape")],
    pages: Annotated[int, Query(default=1, description="Number of pages to scrape")]
) -> dict:
    return scrap_meshoo(base_url=base_url, pages=pages)
