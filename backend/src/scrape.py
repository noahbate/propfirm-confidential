import asyncio
import json
import os
from pathlib import Path
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

CACHE_PATH = Path(__file__).resolve().parents[1] / "scrape-cache" / "prop_firms_scraped.json"

# Define default target Prop Firms directories to scrape
# e.g. Prop Firm list aggregates/blogs
SOURCE_URLS = [
    "https://tempus.dpdns.org/prop-firms-directory-mock",  # Replace with actual live targets as required
]

async def scrape_one_crawl4ai(url: str) -> dict:
    """Uses Crawl4AI to asynchronously scrape any website, producing clean markdown."""
    browser_cfg = BrowserConfig(
        headless=True,
        verbose=False,
    )
    # CacheMode.ENABLED forces quick, bandwidth-friendly loading of identical pages
    run_cfg = CrawlerRunConfig(
        cache_mode=CacheMode.ENABLED, 
        bypass_cache=False
    )
    
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(
            url=url,
            config=run_cfg,
        )
        if not result.success:
            return {
                "url": url,
                "error": result.error_message or "Scraping failed",
                "markdown": ""
            }
        
        return {
            "url": url,
            "success": True,
            "markdown": result.markdown_v2.raw_markdown if result.markdown_v2 else result.markdown
        }

async def async_main() -> int:
    if not SOURCE_URLS:
        print("No SOURCE_URLS configured in scrape.py")
        return 2

    print(f"Initializing Crawl4AI loop for {len(SOURCE_URLS)} targets...")
    firms_data = []
    
    for url in SOURCE_URLS:
        print(f"Scraping: {url}")
        res = await scrape_one_crawl4ai(url)
        firms_data.append(res)

    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(firms_data, indent=2), encoding="utf-8")
    print(f"Successfully processed crawls! Output -> {CACHE_PATH}")
    return 0

def main() -> int:
    try:
        return asyncio.run(async_main())
    except Exception as e:
        print(f"Execution Error during Crawl4AI loop: {e}")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
