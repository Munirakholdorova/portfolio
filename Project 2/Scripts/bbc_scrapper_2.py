import requests
import time
import re
import pandas as pd
from bs4 import BeautifulSoup

# ----- CONFIG -----
HEADERS = {"User-Agent": "Mozilla/5.0"}
BASE_URL = "https://www.bbc.co.uk/search?q=Illegal+work+in+london&d=NEWS_PS"
MAX_PAGES = 29
START_YEAR = 2000
END_YEAR = 2025
OUTPUT_FILE = "bbc_filtered_articles_clean.csv"
# ------------------

# -----------------------------
# SEARCH RESULT URL EXTRACTION
# -----------------------------
def extract_urls_from_page(page):
    url = BASE_URL if page == 1 else f"{BASE_URL}&page={page}"
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    urls = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("https://www.bbc.co.uk/news/"):
            urls.add(href)

    return urls


# -----------------------------
# ARTICLE EXTRACTION (CLEAN)
# -----------------------------
def extract_article_data(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")

        # ---- ARTICLE CONTAINER ----
        article = soup.find("article")
        if not article:
            return None

        # ---- TITLE ----
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else None

        # ---- DATE / YEAR ----
        time_tag = soup.find("time")
        if not time_tag or not time_tag.has_attr("datetime"):
            return None

        year = int(time_tag["datetime"][:4])
        if not (START_YEAR <= year <= END_YEAR):
            return None

        # ---- BBC ARTICLE PARAGRAPHS ONLY ----
        paragraphs = article.find_all(
            "p",
            class_=lambda c: c and "Paragraph" in c
        )

        clean_paragraphs = []
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text and len(text) >= 40:
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


# -----------------------------
# START CRAWLING
# -----------------------------
print("Collecting URLs...")
all_urls = set()

for page in range(1, MAX_PAGES + 1):
    urls = extract_urls_from_page(page)
    all_urls.update(urls)
    print(f"Page {page}/{MAX_PAGES}: {len(urls)} URLs")
    time.sleep(1)

print(f"\nTotal unique article URLs: {len(all_urls)}")

# -----------------------------
# EXTRACT ARTICLES
# -----------------------------
results = []
print("\nExtracting clean article data...")

for url in all_urls:
    data = extract_article_data(url)
    if data:
        results.append(data)
        print("Added:", url)
        time.sleep(0.5)

print(f"\nTotal clean articles saved: {len(results)}")

# -----------------------------
# SAVE CSV
# -----------------------------
df = pd.DataFrame(results, columns=["url", "title", "year", "text"])
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

print(f"\nCSV saved as: {OUTPUT_FILE}")
