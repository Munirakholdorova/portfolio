import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
HEADERS = {"User-Agent": "Mozilla/5.0"}
START_YEAR = 2000
END_YEAR = 2024   # Exclude 2025
MAX_PAGES = 29
OUTPUT_FILE = "/Users/munirakholdorova/Documents/bbc_uk_illegal_work_articles_balanced.csv"

BASE_URL_TEMPLATE = (
    "https://www.bbc.co.uk/search?"
    "q=illegal+work"
    "&from={year}-01-01"
    "&to={year}-12-31"
    "&d=SEARCH_PS"
)

# -------------------------------------------------
# 1. EXTRACT CLEAN ARTICLE DATA
# -------------------------------------------------
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
        if not title:
            return None

        # ---- DATE / YEAR ----
        time_tag = soup.find("time")
        if not time_tag or not time_tag.has_attr("datetime"):
            return None

        year = int(time_tag["datetime"][:4])
        if not (START_YEAR <= year <= END_YEAR):
            return None

        # ---- CLEAN TEXT EXTRACTION (MODERN BBC TEMPLATE) ----
        text_blocks = article.find_all("div", attrs={"data-component": "text-block"})
        clean_paragraphs = []

        for block in text_blocks:
            for p in block.find_all("p"):
                text = p.get_text(strip=True)
                if not text or len(text) < 40:
                    continue
                if text.lower().startswith(("related topics", "more on this story", "related internet links")):
                    continue
                clean_paragraphs.append(text)

        # ---- FALLBACK FOR OLDER BBC ARTICLES ----
        if not clean_paragraphs:
            paragraphs = article.find_all("p")
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

# -------------------------------------------------
# 2. COLLECT ARTICLE URLS YEAR BY YEAR
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
        urls = set(a["href"] for a in soup.find_all("a", href=True) if a["href"].startswith("https://www.bbc.co.uk/news/"))

        if not urls:
            break

        all_urls.update(urls)
        print(f"  Page {page}: {len(urls)} URLs")
        time.sleep(1)

print(f"\nTotal unique URLs collected: {len(all_urls)}")

# -------------------------------------------------
# 3. EXTRACT & FILTER ARTICLES
# -------------------------------------------------
results = []
print("\nExtracting articles...")

for url in all_urls:
    data = extract_article_data(url)
    if data:
        results.append(data)
        print("Added:", url)
        time.sleep(0.5)

print(f"\nTotal articles saved: {len(results)}")

# -------------------------------------------------
# 4. SAVE CSV
# -------------------------------------------------
df = pd.DataFrame(results, columns=["url", "title", "year", "text"])
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
print(f"\nCSV saved as: {OUTPUT_FILE}")

# -------------------------------------------------
# 5. PLOT TIME-SERIES GRAPH
# -------------------------------------------------
# Fill missing years with zero
all_years = list(range(START_YEAR, END_YEAR + 1))
year_counts = df["year"].value_counts().reindex(all_years, fill_value=0)

plt.figure(figsize=(10,5))
plt.plot(year_counts.index, year_counts.values, marker='o')
plt.xlabel("Year")
plt.ylabel("Number of Articles")
plt.title(f"BBC News Articles on Illegal Working in the UK ({START_YEAR}-{END_YEAR})")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
