from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from scraper import TrendsScraperIndonesia

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render halaman utama (dashboard chart)"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/trends")
async def get_trends():
    """API yang dipanggil chart.js untuk fetch tren"""
    scraper = TrendsScraperIndonesia()
    data = scraper.scrape_trends(hour_index=0)
    return JSONResponse(data)
