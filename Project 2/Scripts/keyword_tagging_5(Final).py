import pandas as pd
import re
from collections import Counter

# -------------------------
# 1. LOAD DATA
# -------------------------
df = pd.read_csv("bbc_uk_illegal_work_articles_4.csv")

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Ensure required columns exist
required_cols = ["url", "title", "year", "text"]
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"CSV must contain a '{col}' column")

# Lowercase text
df["text"] = df["text"].astype(str).str.lower()

# -------------------------
# 2. DEFINE SECTORS
# -------------------------
sectors = [
    "construction", "restaurant", "hotel", "farm", "agriculture",
    "factory", "delivery", "cleaning", "hospitality",
    "shop", "security", "social care", "retail", "private hire",
    "taxi", "courier"
]

# -------------------------
# 3. TAGGING FUNCTION
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

# -------------------------
# 4. APPLY TAGGING
# -------------------------
df["sector"] = df["text"].apply(find_sectors)

# -------------------------
# 5. COUNT (ONCE PER ARTICLE)
# -------------------------
sector_counts = Counter()

for sectors_in_article in df["sector"]:
    if sectors_in_article != "not mentioned":
        sector_counts.update(set(sectors_in_article.split(", ")))

# -------------------------
# 6. PRINT RESULTS
# -------------------------
print("\n----- SECTOR FREQUENCIES (PER ARTICLE) -----")
for sector, count in sector_counts.items():
    print(f"{sector}: {count}")

# -------------------------
# 7. KEEP ONLY REQUIRED COLUMNS AND SAVE
# -------------------------
output_cols = ["url", "title", "year", "sector"]
df_final = df[output_cols]

output_file = "articles_4_tagged_sectors_only.csv"
df_final.to_csv(output_file, index=False, encoding="utf-8")

print(f"\nTagged dataset saved as: {output_file}")

# -------------------------
# 8. OPTIONAL CHECK
# -------------------------
no_sector_count = len(df_final[df_final["sector"] == "not mentioned"])
print(f"\nArticles with no sector mentioned: {no_sector_count}")
