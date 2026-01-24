import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------------
# LOAD DATA
# -----------------------------------------
csv_file = "bbc_uk_illegal_work_articles_balanced.csv"
df = pd.read_csv(csv_file)

# -----------------------------------------
# COUNT ARTICLES PER YEAR
# -----------------------------------------
year_counts = df["year"].value_counts().sort_index()

# -----------------------------------------
# PLOT TIME SERIES
# -----------------------------------------
plt.figure(figsize=(10, 5))
plt.plot(year_counts.index, year_counts.values, marker='o')
plt.xlabel("Year")
plt.ylabel("Number of Articles")
plt.title("BBC News Articles on Illegal Working in the UK (2000–2025)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.show()
