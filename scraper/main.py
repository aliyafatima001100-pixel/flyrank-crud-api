import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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
    all_book_urls = []
    
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
            all_book_urls.append(absolute_url)
        next_button = soup.select_one('li.next a')
        if next_button:
            next_href = next_button.get('href')
            current_url = urljoin(current_url, next_href)
        else:
            current_url = None 
    unique_urls = list(set(all_book_urls))
    print(f"catalogue_pages={catalogue_pages_visited}")
    print(f"discovered={len(all_book_urls)}")
    print(f"unique_urls={len(unique_urls)}")
    
    return unique_urls

if __name__ == "__main__":
    discover_books()