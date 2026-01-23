import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
HEADERS = {"User-Agent": "Mozilla/5.0"}
START_YEAR = 2000
END_YEAR = 2024  # exclude 2025
MAX_PAGES = 29   # pages per year
OUTPUT_FILE = "bbc_uk_illegal_work_articles_balanced.csv"

BASE_URL_TEMPLATE = (
    "https://www.bbc.co.uk/search?"
    "q=illegal+work"
    "&from={year}-01-01"
    "&to={year}-12-31"
    "&d=SEARCH_PS"
)

# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------

def is_uk_article(soup):
    """Return True if article is explicitly UK-based."""
    uk_link = soup.find("a", href=lambda h: h and h.startswith("/news/uk"))
    return uk_link is not None

def extract_article_data(url):
    """Extract title, year, and cleaned text from a BBC article."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")

        # --- UK FILTER ---
        if not is_uk_article(soup):
            return None

        # --- ARTICLE CONTAINER ---
        article = soup.find("article") or soup.find("div", {"id": "story-body"}) or soup.find("body")
        if not article:
            return None

        # --- TITLE ---
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else "No title"

        # --- YEAR ---
        year = None
        time_tag = soup.find("time")
        if time_tag and time_tag.has_attr("datetime"):
            year = int(time_tag["datetime"][:4])
        else:
            meta_date = soup.find("meta", {"property": "article:published_time"})
            if meta_date and meta_date.has_attr("content"):
                year = int(meta_date["content"][:4])
        if not year or not (START_YEAR <= year <= END_YEAR):
            return None

        # --- CLEAN TEXT EXTRACTION ---
        clean_paragraphs = []

        # Modern BBC
        text_blocks = article.find_all("div", attrs={"data-component": "text-block"})
        if text_blocks:
            for block in text_blocks:
                for p in block.find_all("p"):
                    text = p.get_text(strip=True)
                    if len(text) >= 40 and not text.lower().startswith((
                        "related topics", "more on this story", "related internet links")):
                        clean_paragraphs.append(text)
        else:
            # Fallback for older articles
            for p in article.find_all("p"):
                text = p.get_text(strip=True)
                if len(text) >= 40:
                    clean_paragraphs.append(text)

        if not clean_paragraphs:
            return None

        article_text = "\n\n".join(clean_paragraphs)

        return {
            "url": url,
            "title": title,
            "year": year,
            "text": article_text
        }

    except Exception:
        return None

# -------------------------------------------------
# 1. COLLECT ARTICLE URLS YEAR BY YEAR
# -------------------------------------------------
print("Collecting BBC article URLs by year...")
all_urls = set()

for year in range(START_YEAR, END_YEAR + 1):
    print(f"\nSearching year: {year}")
    base_url = BASE_URL_TEMPLATE.format(year=year)

    for page in range(1, MAX_PAGES + 1):
        search_url = base_url if page == 1 else f"{base_url}&page={page}"

        try:
            r = requests.get(search_url, headers=HEADERS, timeout=10)
            r.raise_for_status()
        except Exception:
            break

        soup = BeautifulSoup(r.text, "lxml")
        urls = set()

        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("https://www.bbc.co.uk/news/"):
                urls.add(href)

        if not urls:
            break

        all_urls.update(urls)
        print(f"  Page {page}: {len(urls)} URLs")
        time.sleep(1)

print(f"\nTotal unique URLs collected: {len(all_urls)}")

# -------------------------------------------------
# 2. EXTRACT & FILTER ARTICLES
# -------------------------------------------------
results = []
print("\nExtracting UK-only articles...")

for url in all_urls:
    data = extract_article_data(url)
    if data:
        results.append(data)
        print("Added:", url)
        time.sleep(0.5)

print(f"\nTotal UK articles saved: {len(results)}")

# -------------------------------------------------
# 3. SAVE OUTPUT
# -------------------------------------------------
df = pd.DataFrame(results, columns=["url", "title", "year", "text"])
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

print(f"\nCSV saved as: {OUTPUT_FILE}")
