import pandas as pd
import re
from collections import Counter

# -------------------------
# 1. LOAD DATA
# -------------------------
df = pd.read_csv("bbc_uk_illegal_work_articles_4.csv")

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Ensure text column exists
if "text" not in df.columns:
    raise ValueError("CSV must contain a 'text' column")

# Lowercase text
df["text"] = df["text"].astype(str).str.lower()

# -------------------------
# 2. DEFINE KEYWORDS
# -------------------------
illegal_keywords = [
    "illegal", "undocumented", "unauthorised",
    "without permit", "no work permit", "overstayed",
    "foreign worker", "migrant worker"
]

sectors = [
    "construction", "restaurant", "hotel", "farm", "agriculture",
    "factory", "delivery", "cleaning", "hospitality",
    "shop", "security", "social care", "retail", "private hire","taxi", "courier", "delivery"
]

# -------------------------
# 3. TAGGING FUNCTIONS
# -------------------------
def find_sectors(text):
    """
    Return unique sectors mentioned in text (once per article).
    """
    found = set()
    for sector in sectors:
        if re.search(rf"\b{re.escape(sector)}\b", text):
            found.add(sector)
    return ", ".join(sorted(found)) if found else "not mentioned"


def find_illegal_keywords(text):
    """
    Return unique illegal-work keywords mentioned in text (once per article).
    """
    found = set()
    for kw in illegal_keywords:
        if re.search(rf"\b{re.escape(kw)}\b", text):
            found.add(kw)
    return ", ".join(sorted(found)) if found else "none"

# -------------------------
# 4. APPLY TAGGING
# -------------------------
df["sector"] = df["text"].apply(find_sectors)
df["illegal_status"] = df["text"].apply(find_illegal_keywords)

# -------------------------
# 5. COUNT (ONCE PER ARTICLE)
# -------------------------
sector_counts = Counter()
illegal_counts = Counter()

for sectors_in_article in df["sector"]:
    if sectors_in_article != "not mentioned":
        sector_counts.update(set(sectors_in_article.split(", ")))

for illegal_in_article in df["illegal_status"]:
    if illegal_in_article != "none":
        illegal_counts.update(set(illegal_in_article.split(", ")))

# -------------------------
# 6. PRINT RESULTS
# -------------------------
print("\n----- SECTOR FREQUENCIES (PER ARTICLE) -----")
for sector, count in sector_counts.items():
    print(f"{sector}: {count}")

print("\n----- ILLEGAL KEYWORD FREQUENCIES (PER ARTICLE) -----")
for kw, count in illegal_counts.items():
    print(f"{kw}: {count}")

# -------------------------
# 7. SAVE TAGGED CSV
# -------------------------
output_file = "articles_4_tagged.csv"
df.to_csv(output_file, index=False, encoding="utf-8")

print(f"\nTagged dataset saved as: {output_file}")

# -------------------------
# 8. OPTIONAL CHECK
# -------------------------
no_sector_count = len(df[df["sector"] == "not mentioned"])
print(f"\nArticles with no sector mentioned: {no_sector_count}")
