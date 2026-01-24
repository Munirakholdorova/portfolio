import requests
from bs4 import BeautifulSoup
import csv
import time

# -----------------------------
# BBC ARTICLE URLS
# -----------------------------
urls = [
    'https://www.bbc.co.uk/news/articles/c04vqzp6x31o',
    'https://www.bbc.co.uk/news/articles/c709r8ekn8no',
    'https://www.bbc.co.uk/news/articles/cq50n5pd2ejo',
    'https://www.bbc.co.uk/news/articles/c740vjrp81po',
    'https://www.bbc.co.uk/news/articles/cwy8ee2w73jo',
    'https://www.bbc.co.uk/news/articles/cx2jnldejrko',
    'https://www.bbc.co.uk/news/articles/cj6xe89z92po',
    'https://www.bbc.co.uk/news/articles/cy850zn36pqo',
    'https://www.bbc.co.uk/news/articles/c5y5379djl3o',
    'https://www.bbc.co.uk/news/articles/cy404wyemd9o',
    'https://www.bbc.co.uk/news/articles/cy8j6dz2428o',
    'https://www.bbc.co.uk/news/articles/cy85zrlp81mo',
    'https://www.bbc.co.uk/news/articles/c0mpzpv3mw7o'
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

# -----------------------------
# OUTPUT CSV
# -----------------------------
with open("bbc_articles_final.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["URL", "Title", "Date", "ArticleText"])

    for url in urls:
        print("Processing:", url)

        try:
            r = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(r.text, "html.parser")

            # -----------------------------
            # ARTICLE CONTAINER
            # -----------------------------
            article = soup.find("article")
            if not article:
                print("No article found:", url)
                continue

            # -----------------------------
            # TITLE
            # -----------------------------
            title_tag = soup.find("h1")
            title = title_tag.get_text(strip=True) if title_tag else ""

            # -----------------------------
            # DATE
            # -----------------------------
            time_tag = soup.find("time")
            date = time_tag["datetime"] if time_tag and time_tag.has_attr("datetime") else ""

            # -----------------------------
            # REAL BBC ARTICLE PARAGRAPHS ONLY
            # Rule: <p> with class containing "Paragraph"
            # -----------------------------
            paragraphs = article.find_all(
                "p",
                class_=lambda c: c and "Paragraph" in c
            )

            clean_paragraphs = []
            for p in paragraphs:
                text = p.get_text(strip=True)

                # Skip very short or empty paragraphs
                if not text or len(text) < 40:
                    continue

                clean_paragraphs.append(text)

            article_text = "\n\n".join(clean_paragraphs)

            writer.writerow([url, title, date, article_text])
            time.sleep(1)

        except Exception as e:
            print("Failed:", url, e)
            writer.writerow([url, "", "", ""])

print("Done! CSV created: bbc_articles_final.csv")
