import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
INPUT_FILE = "bbc_uk_illegal_work_articles_4.csv"
OUTPUT_FILE = "tagging_sector_with_places.csv"
HEADERS = {"User-Agent": "Mozilla/5.0"}
REQUEST_DELAY = 0.5
# -------------------------------------------------


# -------------------------------------------------
# EXTRACT REGIONS FROM ARTICLE HTML
# -------------------------------------------------
def extract_article_places(url):
    """
    Extracts large and small regions from BBC article navigation.
    Example output:
      large_region = England
      local_region = Bristol
    """
    large_region = None
    local_region = None

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")

        nav = soup.find("nav", attrs={"aria-label": "BBC News"})
        if not nav:
            return large_region, local_region

        region_links = nav.find_all(
            "a",
            href=lambda h: h and (
                h.startswith("/news/england") or
                h.startswith("/news/scotland") or
                h.startswith("/news/wales") or
                h.startswith("/news/northern-ireland")
            )
        )

        if region_links:
            large_region = region_links[0].get_text(strip=True)

        if len(region_links) > 1:
            local_region = region_links[1].get_text(strip=True)

    except Exception:
        pass

    return large_region, local_region


# -------------------------------------------------
# LOAD CSV
# -------------------------------------------------
df = pd.read_csv(INPUT_FILE)
df["large_region"] = ""
df["local_region"] = ""

# -------------------------------------------------
# PROCESS ARTICLES
# -------------------------------------------------
print("Extracting article regions from HTML...")

for idx, row in df.iterrows():
    url = row["url"]

    large, local = extract_article_places(url)

    df.at[idx, "large_region"] = large if large else "UK"
    df.at[idx, "local_region"] = local if local else ""

    print(
        f"{idx+1}/{len(df)} -> "
        f"large={df.at[idx,'large_region']}, "
        f"local={df.at[idx,'local_region']}"
    )

    time.sleep(REQUEST_DELAY)

# -------------------------------------------------
# SAVE OUTPUT
# -------------------------------------------------
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

print(f"\nSaved CSV with regions: {OUTPUT_FILE}")

