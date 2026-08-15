# Polite Scraper - Books to Scrape

## Target Classification
* **Target Site:** books.toscrape.com
* **Scope:** The first 3 catalogue pages and their associated 60 book detail pages.
* **Data Collected:** Book title, URL, price, availability, rating, and description.
* **Why it is appropriate:** Books to Scrape is explicitly designed as a public practice sandbox for scraping.
* **Robots.txt check:** Checked `https://books.toscrape.com/robots.txt` - no robots file found (404).
* I will not reuse this code on another site without checking its rules and terms first.

## Installation & Running (Python Lane)
1. Install dependencies: `pip install requests beautifulsoup4 pydantic`
2. Run the scraper: `python main.py` or `py main.py`

## Record Schema
* `title` (string)
* `product_url` (string)
* `price_text` (string)
* `price_gbp` (float)
* `availability_text` (string)
* `rating_text` (string, optional)
* `description` (string, optional)
* `source_page` (string)
* `fetched_at` (string, ISO datetime)

## Politeness Rules
* **User-Agent:** Honest identification linking to my GitHub repo.
* **Delay:** 0.5-second wait between live requests.
* **Timeout:** 10-second limit on all requests.
* **Cache:** All HTML is cached locally to prevent duplicate network requests on reruns.

## Limitations & Ethics
* **Limitation:** The script relies on specific CSS classes (`article.product_pod`, `p.price_color`). If the site redesigns its HTML layout, the scraper will break.
* **Ethics Note:** Always use an official API if available. Never bypass logins, paywalls, or blocks. Collect only what you need.
* **Browser Cost:** A plain HTTP request takes ~100ms and minimal memory. Loading a headless browser like Playwright would take seconds and 100MB+ RAM per page. We didn't need a browser here because the target data is already present in the raw HTML sent by the server.

## Sample Run Report
```json
{
  "start_time": "2026-08-15T10:30:00Z",
  "duration_seconds": 1.25,
  "pages_fetched": 0,
  "cache_hits": 64,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 1
}