import os
import time
import requests
import json
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone
from pydantic import BaseModel, ValidationError
from typing import Optional

HEADERS = {
    "User-Agent": "FlyRankInternshipA9/1.0 (+https://github.com/aliyafatima001100-pixel/flyrank-crud-api)"
}
TIMEOUT = 10
class BookRecord(BaseModel):
    title: str
    product_url: str
    price_text: str
    price_gbp: float
    availability_text: str
    rating_text: Optional[str] = None
    description: Optional[str] = None
    source_page: str
    fetched_at: str

def fetch_html(url, cache_filename):
    cache_path = os.path.join("cache", cache_filename)
    os.makedirs("cache", exist_ok=True)

    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as file:
            return file.read()

    time.sleep(0.5)
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if response.status_code != 200:
            return None
        html = response.text
        with open(cache_path, "w", encoding="utf-8") as file:
            file.write(html)
        return html
    except Exception:
        return None

def discover_books():
    base_url = "https://books.toscrape.com/catalogue/page-1.html"
    current_url = base_url
    catalogue_pages_visited = 0
    discovered_links = {}
    
    while current_url and catalogue_pages_visited < 3:
        catalogue_pages_visited += 1
        cache_filename = f"catalogue-page-{catalogue_pages_visited}.html"
        
        html = fetch_html(current_url, cache_filename)
        if not html: break
            
        soup = BeautifulSoup(html, "html.parser")
        for link in soup.select('article.product_pod h3 a'):
            absolute_url = urljoin(current_url, link.get('href'))
            if absolute_url not in discovered_links:
                discovered_links[absolute_url] = current_url
                
        next_button = soup.select_one('li.next a')
        current_url = urljoin(current_url, next_button.get('href')) if next_button else None

    return discovered_links

def clean_price(price_str):
    if not price_str: return 0.0
    match = re.search(r'[\d\.]+', price_str)
    return float(match.group()) if match else 0.0

def scrape_books():
    discovered_links = discover_books()
    good_records = []
    bad_records = []
    
    for book_url, source_page in discovered_links.items():
        safe_name = book_url.split('/')[-2] + ".html"
        html = fetch_html(book_url, safe_name)
        if not html: continue
            
        soup = BeautifulSoup(html, "html.parser")
        product_main = soup.select_one('article.product_page')
        if not product_main: continue
            
        title = product_main.select_one('h1').text if product_main.select_one('h1') else None
        price_text = product_main.select_one('p.price_color').text if product_main.select_one('p.price_color') else None
        
        availability_elem = product_main.select_one('p.availability')
        availability_text = availability_elem.text.strip() if availability_elem else None
        
        rating_elem = product_main.select_one('p.star-rating')
        rating_text = rating_elem['class'][1] if rating_elem and len(rating_elem['class']) > 1 else None
        
        desc_elem = soup.select_one('#product_description ~ p')
        description = desc_elem.text if desc_elem else None

        raw_dict = {
            "title": title,
            "product_url": book_url,
            "price_text": price_text,
            "price_gbp": clean_price(price_text),
            "availability_text": availability_text,
            "rating_text": rating_text,
            "description": description,
            "source_page": source_page,
            "fetched_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        }
        
        try:
            valid_record = BookRecord(**raw_dict)
            good_records.append(valid_record.model_dump())
        except ValidationError as e:
            bad_records.append({"url": book_url, "error": str(e), "raw_data": raw_dict})

    os.makedirs("output", exist_ok=True)
    with open("output/books.json", "w", encoding="utf-8") as f:
        json.dump(good_records, f, indent=2)
    with open("output/errors.json", "w", encoding="utf-8") as f:
        json.dump(bad_records, f, indent=2)
    print(f"Validated and stored {len(good_records)} books to output/books.json")
    if bad_records:
        print(f"WARNING: {len(bad_records)} records failed validation (see output/errors.json)")

if __name__ == "__main__":
    scrape_books()