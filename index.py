'''from fastapi import FastAPI, Query
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
    return scrap_meshoo(base_url=base_url, pages=pages)'''

from fastapi import FastAPI, Query
from scraper import scrap_meshoo
from fastapi.responses import JSONResponse
from typing import Optional

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI deployed successfully!"}

@app.get("/scrape")
def scrape(
    base_url: str = Query(..., description="Base URL to scrape"),
    pages: int = Query(1, description="Number of pages to scrape"),
    limit: Optional[int] = Query(None, description="Limit the number of results")
):
    try:
        df = scrap_meshoo(base_url, pages)
        if limit:
            df = df.head(limit)

        return {
            "scraped_at": str(df['Scrap_time'][0]),
            "total_products": len(df),
            "products": df.drop(columns=['Scrap_time']).to_dict(orient="records")
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Scraping failed", "details": str(e)}
        )
