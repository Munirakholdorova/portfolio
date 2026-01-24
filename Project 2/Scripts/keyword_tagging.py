import pandas as pd

from collections import Counter


# load csv
df = pd.read_csv("articles_3.csv")

# normalize column names: strip spaces and lowercase
df.columns = df.columns.str.strip().str.lower()

# now the 'Text' column becomes 'text'
df['text'] = df['text'].str.lower()  # convert text to lowercase


# -------------------------
# 2. Define keywords
# -------------------------
illegal_keywords = [
    "illegal", "undocumented", "unauthorised", 
    "without permit", "no work permit", "overstayed", 
    "foreign worker", "migrant worker"
]

sectors = [
    "construction", "restaurant", "hotel", "farm", "agriculture",
    "factory", "delivery", "cleaning", "hospitality", "shop", "security"
]

# -------------------------
# 3. Functions to tag
# -------------------------
def find_sectors(text):
    """Return all sectors mentioned in the text, comma-separated."""
    found = [sector for sector in sectors if sector in text]
    if found:
        return ", ".join(found)
    return "not mentioned"

def find_illegal_keywords(text):
    """Return all illegal keywords found in the text, comma-separated."""
    found = [kw for kw in illegal_keywords if kw in text]
    if found:
        return ", ".join(found)
    return "none"

# -------------------------
# 4. Apply tagging
# -------------------------
df['sector'] = df['text'].apply(find_sectors)
df['illegal_status'] = df['text'].apply(find_illegal_keywords)

# -------------------------
# 5. Count sector frequencies
# -------------------------
all_sectors = df['sector'].str.split(", ").sum()  # split multiple sectors per text
sector_counts = Counter(all_sectors)

print("----- Sector Frequencies -----")
for sector, count in sector_counts.items():
    print(f"{sector}: {count}")

# -------------------------
# 6. Count illegal keyword frequencies
# -------------------------
all_illegal = df['illegal_status'].str.split(", ").sum()
illegal_counts = Counter(all_illegal)

print("\n----- Illegal Keyword Frequencies -----")
for kw, count in illegal_counts.items():
    print(f"{kw}: {count}")

# -------------------------
# 7. Optional: View texts with no sector
# -------------------------
no_sector_texts = df[df['sector'] == "not mentioned"]
print(f"\nNumber of texts with no sector mentioned: {len(no_sector_texts)}")
