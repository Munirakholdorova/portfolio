import requests
import time
import re
import pandas as pd
from bs4 import BeautifulSoup

# ----- CONFIG -----
HEADERS = {"User-Agent": "Mozilla/5.0"}
BASE_URL = "https://www.bbc.co.uk/search?q=Illegal+work+in+london&d=NEWS_PS"
MAX_PAGES = 29   # limit based on manual checking
START_YEAR = 2000
END_YEAR = 2025
OUTPUT_FILE = "bbc_filtered_articles.csv"
# ------------------

def extract_urls_from_page(page):
    url = BASE_URL if page == 1 else f"{BASE_URL}&page={page}"
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    urls = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # Keep BBC News articles only
        if href.startswith("https://www.bbc.co.uk/") and "news" in href:
            urls.append(href)
    return set(urls)

def extract_year(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")

        # Method 1: Try <time datetime="YYYY-...">
        t = soup.find("time")
        if t and t.has_attr("datetime"):
            return int(t["datetime"][:4])

        # Method 2: Try JSON-LD script
        script = soup.find("script", type="application/ld+json")
        if script:
            m = re.search(r'"datePublished"\s*:\s*"(\d{4})', script.text)
            if m:
                return int(m.group(1))

        return None
    except:
        return None

def extract_text(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text(strip=True) for p in paragraphs)
        return text if text else None
    except:
        return None


# ------------ Start crawling ----------------
print("Collecting URLs...")
all_urls = set()
for page in range(1, MAX_PAGES + 1):
    urls = extract_urls_from_page(page)
    print(f"Page {page}/{MAX_PAGES}: found {len(urls)} article URLs")
    all_urls.update(urls)
    time.sleep(1)  # polite crawling

print(f"\nTotal unique URLs collected: {len(all_urls)}")

# Filter and extract content
results = []
print("\nFiltering + extracting data...")

for url in all_urls:
    year = extract_year(url)
    if year is None or not (START_YEAR <= year <= END_YEAR):
        continue

    text = extract_text(url)
    if not text:
        continue

    results.append({"url": url, "year": year, "text": text})
    print(f"Added: {url}")
    time.sleep(0.3)

print(f"\nArticles in range {START_YEAR}-{END_YEAR}: {len(results)}")

# Save CSV
df = pd.DataFrame(results)
df.to_csv(OUTPUT_FILE, index=False)

print(f"\nSaved to: {OUTPUT_FILE}")
