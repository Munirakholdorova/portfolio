import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

TEST_URLS = [
    "https://www.bbc.co.uk/news/articles/cy404wyemd9o",
    "https://www.bbc.co.uk/news/articles/c865yj3wn6wo",
    "https://www.bbc.co.uk/news/articles/czr1mkml406o",
]


def extract_article_places(url):
    """
    Extracts large + local region using BBC News article navigation HTML
    """
    large_region = None
    local_region = None

    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    # This is the exact structure you showed in the screenshot
    nav = soup.find("nav", attrs={"aria-label": "BBC News"})
    if not nav:
        return None, None

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

    return large_region, local_region


print("\n=== TEST RESULTS ===\n")

for url in TEST_URLS:
    large, local = extract_article_places(url)

    print(f"URL: {url}")
    print(f"  Large region: {large}")
    print(f"  Local region: {local}")
    print("-" * 50)
