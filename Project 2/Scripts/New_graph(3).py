import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------------
# LOAD DATA
# -----------------------------------------
csv_file = "bbc_uk_illegal_work_articles_balanced.csv"
df = pd.read_csv(csv_file)

# -----------------------------------------
# EXCLUDE YEARS WITHOUT DATA (before 2010) AND PARTIAL YEAR 2025
# -----------------------------------------
df = df[(df["year"] >= 2010) & (df["year"] <= 2024)]

# -----------------------------------------
# COUNT ARTICLES PER YEAR
# -----------------------------------------
year_counts = df["year"].value_counts().sort_index()

# -----------------------------------------
# PLOT TIME SERIES
# -----------------------------------------
plt.figure(figsize=(12, 6))

# Bar chart to clearly show differences year by year
plt.bar(year_counts.index, year_counts.values, color='skyblue', edgecolor='black')

# Add line on top to highlight trend
plt.plot(year_counts.index, year_counts.values, color='red', marker='o', linewidth=2)

# Labels and title
plt.xlabel("Year", fontsize=12)
plt.ylabel("Number of Articles", fontsize=12)
plt.title("BBC News Articles on Illegal Working in the UK (2010–2024)", fontsize=14)

# Show exact numbers on top of bars
for i, value in enumerate(year_counts.values):
    plt.text(year_counts.index[i], value + 0.5, str(value), ha='center', fontsize=10)

plt.xticks(year_counts.index, rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
