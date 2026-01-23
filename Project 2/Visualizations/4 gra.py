import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load CSV
df = pd.read_csv("articles_3.csv")

# Normalize columns
df.columns = df.columns.str.strip().str.lower()
df['text'] = df['text'].astype(str).str.lower()

# Keywords
illegal_keywords = [
    "illegal", "undocumented", "unauthorised",
    "without permit", "no work permit", "overstayed",
    "foreign worker", "migrant worker"
]

sectors = [
    "construction", "restaurant", "hotel", "farm", "agriculture",
    "factory", "delivery", "cleaning", "hospitality", "shop", "security"
]

# Tagging functions
def find_sectors(text):
    return [s for s in sectors if s in text]

def has_illegal(text):
    return any(k in text for k in illegal_keywords)

# Filter only articles mentioning illegal migrants
df_illegal = df[df['text'].apply(has_illegal)]

# Count sectors
sector_counts = Counter()

for text in df_illegal['text']:
    for s in find_sectors(text):
        sector_counts[s] += 1

# Convert to DataFrame
sector_df = pd.DataFrame(
    sector_counts.items(),
    columns=["Sector", "Frequency"]
).sort_values(by="Frequency", ascending=False)

# Plot
plt.figure(figsize=(10, 6))
plt.bar(sector_df["Sector"], sector_df["Frequency"])
plt.xticks(rotation=45, ha="right")
plt.ylabel("Number of BBC News Articles")
plt.xlabel("Employment Sector")
plt.title("Sectors Associated with Illegal Migrant Work in BBC News")

plt.tight_layout()
plt.show()

