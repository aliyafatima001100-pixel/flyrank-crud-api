import os
import requests

HEADERS = {
    "User-Agent": "FlyRankInternshipA9/1.0 (+https://github.com/aliyafatima001100-pixel/flyrank-crud-api)"
}
TIMEOUT = 10  

def fetch_page_1():
    url = "https://books.toscrape.com/catalogue/page-1.html"
    cache_path = "cache/catalogue-page-1.html"
    os.makedirs("cache", exist_ok=True)

    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as file:
            html = file.read()
        print("CACHE HIT")
        print(f"Response size: {len(html)} characters")
        return html
    print("FETCH")
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        if response.status_code != 200:
            print(f"Failed to fetch! Status code: {response.status_code}")
            return None
            
        html = response.text
        with open(cache_path, "w", encoding="utf-8") as file:
            file.write(html)
            
        print(f"Response size: {len(html)} characters")
        return html
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    fetch_page_1()