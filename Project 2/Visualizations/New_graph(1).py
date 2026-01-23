import pandas as pd
import matplotlib.pyplot as plt

csv_file = "bbc_uk_illegal_work_articles_balanced.csv"
df = pd.read_csv(csv_file)
df = df[df["year"] < 2025]

all_years = list(range(2000, 2025))
year_counts = df["year"].value_counts().reindex(all_years, fill_value=0)

# Normalize
year_percent = year_counts / year_counts.sum() * 100

plt.figure(figsize=(10, 5))
plt.plot(year_percent.index, year_percent.values, marker='o', color='blue')
plt.xlabel("Year")
plt.ylabel("Percentage of Articles")
plt.title("BBC News Articles on Illegal Working in the UK (2000–2024) - Normalized")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
