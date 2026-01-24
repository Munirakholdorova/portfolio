import requests
from bs4 import BeautifulSoup
import nltk
import ssl
import csv
import os
from nltk.tokenize import sent_tokenize

# -----------------------------
# SSL fix for Mac NLTK downloads
# -----------------------------
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download sentence tokenizer
nltk.download('punkt')

# -----------------------------
# Paths
# -----------------------------
# Put your urls.txt file in the same folder as this script, or adjust the path
urls_file = "urls.txt"  # e.g., "/Users/munirakholdorova/Documents/urls.txt"
output_csv = "london_articles.csv"

# -----------------------------
# Create output folder if needed
# -----------------------------
output_folder = "london_sentences_output"
os.makedirs(output_folder, exist_ok=True)

# -----------------------------
# Open CSV to save results
# -----------------------------
with open(os.path.join(output_folder, output_csv), "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    # Header row
    writer.writerow(["URL", "Date", "Section", "Sentence"])

    # -----------------------------
    # Read URLs from urls.txt
    # -----------------------------
    if not os.path.exists(urls_file):
        print(f"Error: {urls_file} not found. Make sure the file exists and path is correct.")
        exit()

    with open(urls_file, "r") as f:
        urls = f.read().splitlines()

    # -----------------------------
    # Loop through all URLs
    # -----------------------------
    for url in urls:
        print(f"Processing: {url}")
        try:
            res = requests.get(url)
            if res.status_code != 200:
                print(f"Failed to fetch: {url} (status {res.status_code})")
                continue
        except Exception as e:
            print(f"Request error for {url}: {e}")
            continue

        soup = BeautifulSoup(res.text, "html.parser")

        # -----------------------------
        # Extract all paragraph text
        # -----------------------------
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs)

        # -----------------------------
        # Split into sentences and keep London only
        # -----------------------------
        sentences = sent_tokenize(text)
        london_sentences = [s for s in sentences if "london" in s.lower()]
        if not london_sentences:
            continue  # skip if no London sentence

        # -----------------------------
        # Extract publication date
        # -----------------------------
        date_tag = soup.find("time")
        if date_tag and date_tag.has_attr("datetime"):
            date = date_tag["datetime"]
        else:
            date = "Unknown"

        # -----------------------------
        # Extract section (e.g., Business, UK)
        # -----------------------------
        section_tag = soup.find("a", {"data-testid": "metadata-section-link"})
        section = section_tag.get_text(strip=True) if section_tag else "Unknown"

        # -----------------------------
        # Write each London sentence with metadata
        # -----------------------------
        for sentence in london_sentences:
            writer.writerow([url, date, section, sentence])

print(f"Done! Check the folder '{output_folder}' for the CSV: {output_csv}")
