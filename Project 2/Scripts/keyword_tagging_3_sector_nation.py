import pandas as pd
import re
from collections import Counter

# -------------------------
# 1. LOAD DATA
# -------------------------
df = pd.read_csv("bbc_london_illegal_work_articles.csv")

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Ensure text column exists
if "text" not in df.columns:
    raise ValueError("CSV must contain a 'text' column")

# Lowercase text for consistent matching
df["text"] = df["text"].astype(str).str.lower()

# -------------------------
# 2. DEFINE KEYWORDS
# -------------------------

# Sectors
sectors = [
    "construction", "restaurant", "hotel", "farm", "agriculture",
    "factory", "delivery", "cleaning", "hospitality",
    "shop", "security", "social care", "retail", 
    "private hire", "taxi", "courier"
]

# Nationalities (expandable)
nationalities = [
    "polish", "romanian", "bulgarian", "italian", "spanish", "portuguese",
    "indian", "pakistani", "bangladeshi", "chinese", "filipino",
    "nigerian", "egyptian", "syrian", "ukrainian", "irish", "british",
    "african", "other european"
]

# -------------------------
# 3. TAGGING FUNCTIONS
# -------------------------

def find_keywords(text, keyword_list, none_label="not mentioned"):
    """
    Generic function to find keywords in text.
    Returns unique matches, comma-separated, or none_label if nothing found.
    """
    found = set()
    for kw in keyword_list:
        if re.search(rf"\b{re.escape(kw)}\b", text):
            found.add(kw)
    return ", ".join(sorted(found)) if found else none_label

# Wrappers for clarity
def find_sectors(text):
    return find_keywords(text, sectors, none_label="not mentioned")

def find_nationalities(text):
    return find_keywords(text, nationalities, none_label="not mentioned")

# -------------------------
# 4. APPLY TAGGING TO DATA
# -------------------------
df["sector"] = df["text"].apply(find_sectors)
df["nationality"] = df["text"].apply(find_nationalities)

# -------------------------
# 5. COUNT FREQUENCIES
# -------------------------
def count_column_keywords(series, none_label="not mentioned"):
    counter = Counter()
    for value in series:
        if value != none_label:
            counter.update(set(value.split(", ")))
    return counter

sector_counts = count_column_keywords(df["sector"], none_label="not mentioned")
nationality_counts = count_column_keywords(df["nationality"], none_label="not mentioned")

# -------------------------
# 6. PRINT RESULTS
# -------------------------
print("\n----- SECTOR FREQUENCIES (PER ARTICLE) -----")
for sector, count in sector_counts.items():
    print(f"{sector}: {count}")

print("\n----- NATIONALITY FREQUENCIES (PER ARTICLE) -----")
for nation, count in nationality_counts.items():
    print(f"{nation}: {count}")

# -------------------------
# 7. OPTIONAL CHECKS
# -------------------------
no_sector_count = len(df[df["sector"] == "not mentioned"])
no_nationality_count = len(df[df["nationality"] == "not mentioned"])
print(f"\nArticles with no sector mentioned: {no_sector_count}")
print(f"Articles with no nationality mentioned: {no_nationality_count}")

# -------------------------
# 8. SAVE TAGGED CSV
# -------------------------
output_file = "articles_tagged_sectors_nationalities.csv"
df.to_csv(output_file, index=False, encoding="utf-8")
print(f"\nTagged dataset saved as: {output_file}")
