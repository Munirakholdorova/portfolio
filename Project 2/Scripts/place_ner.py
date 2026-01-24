import pandas as pd
import spacy
from collections import Counter

# Load your CSV
df = pd.read_csv("corpus_2.csv")
df.columns = df.columns.str.strip().str.lower()
df['text'] = df['text'].fillna("").astype(str)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to extract place names using NER
def extract_places(text):
    doc = nlp(text)
    places = [ent.text for ent in doc.ents if ent.label_ == "GPE"]  # GPE = Geo-political entity
    if places:
        return ", ".join(places)
    return "not mentioned"

# Apply to your dataframe
df['place'] = df['text'].apply(extract_places)

# Count place frequencies
all_places = df['place'].str.split(", ").sum()
place_counts = Counter(all_places)

print("----- Place Frequencies -----")
for place, count in place_counts.items():
    print(f"{place}: {count}")
