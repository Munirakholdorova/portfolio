import pandas as pd
import matplotlib.pyplot as plt

# ---- Load your corpus from a CSV file ----
file_name = "/Users/munirakholdorova/Downloads/Hmml/bbc_uk_illegal_work_articles_4.csv"
df = pd.read_csv(file_name)


# Make sure 'year' is numeric
df['year'] = pd.to_numeric(df['year'], errors='coerce')

# ---- 1. Number of texts per year ----
texts_per_year = df.groupby('year').size()
plt.figure(figsize=(10,6))
plt.plot(texts_per_year.index, texts_per_year.values, marker='o')
plt.title("Number of Texts per Year")
plt.xlabel("Year")
plt.ylabel("Number of Texts")
plt.grid(True)
plt.show()

# ---- 2. Frequency of a word over time ----
word_to_track = "text"  # <-- change to any word you want to track
df['word_count'] = df['text'].str.lower().str.count(word_to_track.lower())
word_per_year = df.groupby('year')['word_count'].sum()

plt.figure(figsize=(10,6))
plt.plot(word_per_year.index, word_per_year.values, marker='o', color='orange')
plt.title(f"Frequency of '{word_to_track}' Over Time")
plt.xlabel("Year")
plt.ylabel(f"Count of '{word_to_track}'")
plt.grid(True)
plt.show()



