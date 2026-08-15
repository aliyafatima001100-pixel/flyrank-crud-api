import os
import time
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone

HEADERS = {
    "User-Agent": "FlyRankInternshipA9/1.0 (+https://github.com/aliyafatima001100-pixel/flyrank-crud-api)"
}
TIMEOUT = 10

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
            print(f"Failed to fetch {url}! Status: {response.status_code}")
            return None
        
        html = response.text
        with open(cache_path, "w", encoding="utf-8") as file:
            file.write(html)
        return html
    except Exception as e:
        print(f"Error fetching {url}: {e}")
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
        if not html:
            break
            
        soup = BeautifulSoup(html, "html.parser")
        book_links = soup.select('article.product_pod h3 a')
        for link in book_links:
            href = link.get('href')
            absolute_url = urljoin(current_url, href)
            if absolute_url not in discovered_links:
                discovered_links[absolute_url] = current_url
            
        next_button = soup.select_one('li.next a')
        if next_button:
            next_href = next_button.get('href')
            current_url = urljoin(current_url, next_href)
        else:
            current_url = None

    return discovered_links

def scrape_books():
    discovered_links = discover_books()
    raw_records = []
    
    print(f"Extracting {len(discovered_links)} books... (might take ~30 seconds on first run)")
    
    for book_url, source_page in discovered_links.items():
        safe_name = book_url.split('/')[-2] + ".html"
        
        html = fetch_html(book_url, safe_name)
        if not html:
            continue
            
        soup = BeautifulSoup(html, "html.parser")
        product_main = soup.select_one('article.product_page')
        
        # Safely extract all fields (in case a page is missing something)
        title = product_main.select_one('h1').text if product_main.select_one('h1') else None
        price_text = product_main.select_one('p.price_color').text if product_main.select_one('p.price_color') else None
        
        availability_elem = product_main.select_one('p.availability')
        availability_text = availability_elem.text.strip() if availability_elem else None
        
        rating_elem = product_main.select_one('p.star-rating')
        rating_text = rating_elem['class'][1] if rating_elem and len(rating_elem['class']) > 1 else None
        
        desc_elem = soup.select_one('#product_description ~ p')
        description = desc_elem.text if desc_elem else None
        record = {
            "title": title,
            "product_url": book_url,
            "price_text": price_text,
            "availability_text": availability_text,
            "rating_text": rating_text,
            "description": description,
            "source_page": source_page,
            "fetched_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        }
        raw_records.append(record)
    if raw_records:
        print(json.dumps(raw_records[0], indent=2))
    print(f"detail_pages={len(raw_records)}")
    
    return raw_records

if __name__ == "__main__":
    scrape_books()