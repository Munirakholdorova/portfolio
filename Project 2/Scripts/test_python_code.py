from newspaper import Article
import requests
from bs4 import BeautifulSoup
import csv
import time

# List of your URLs
urls = [
    'https://www.bbc.co.uk/news/articles/c04vqzp6x31o',
    'https://www.bbc.co.uk/news/articles/c709r8ekn8no',
    'https://www.bbc.co.uk/news/uk-23535938'
]

with open("articles.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["URL", "Title", "Date", "Text"])

    for url in urls:
        print("Processing:", url)

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        # ✅ TITLE (BBC uses h1 reliably)
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else ""

        # ✅ DATE (BBC uses <time datetime="">)
        time_tag = soup.find("time")
        date = time_tag["datetime"] if time_tag and time_tag.has_attr("datetime") else ""

       # ✅ CLEAN ARTICLE TEXT (BBC ONLY)
        article_tag = soup.find("article")

        text = ""
        if article_tag:
            paragraphs = article_tag.find_all("p")
            clean_paragraphs = []
            for p in paragraphs:
                # Exclude captions, side content, and navigation text
                if p.find_parent(["figure", "aside", "nav"]):
                    continue

                p_text = p.get_text(strip=True)

                # Skip short junk lines

                if len(p_text) < 30:
                    continue

                clean_paragraphs.append(p_text)

            text = " ".join(clean_paragraphs)


        writer.writerow([url, title, date, text])
        time.sleep(1)

print("Done! Articles saved to articles3.csv")
