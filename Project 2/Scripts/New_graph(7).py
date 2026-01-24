import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------------
# LOAD DATA
# -----------------------------------------
csv_file = "bbc_uk_illegal_work_articles_balanced.csv"
df = pd.read_csv(csv_file)

# -----------------------------------------
# FILTER DATA (2010–2024)
# -----------------------------------------
df = df[(df["year"] >= 2010) & (df["year"] <= 2024)]

# -----------------------------------------
# COUNT ARTICLES PER YEAR
# -----------------------------------------
year_counts = df["year"].value_counts().sort_index()

# Ensure all years are included
all_years = pd.Series(0, index=range(2010, 2025))
year_counts = all_years.add(year_counts, fill_value=0)

# -----------------------------------------
# STYLE SETTINGS
# -----------------------------------------
sns.set(style="whitegrid")  # Clean, professional style
plt.figure(figsize=(12, 6))

# Line with markers and a subtle shadow for emphasis
plt.plot(year_counts.index, year_counts.values, marker='o', markersize=8, 
         color="#1f77b4", linewidth=3, alpha=0.9)

# Fill under the line for visual emphasis
plt.fill_between(year_counts.index, year_counts.values, color="#1f77b4", alpha=0.2)

# Labels and title
plt.xlabel("Year", fontsize=14)
plt.ylabel("Number of Articles", fontsize=14)
plt.title("BBC News Articles on Illegal Working in the UK (2010–2024)", fontsize=16)

# Y-axis ticks
plt.yticks(fontsize=12)

# X-axis ticks
plt.xticks(year_counts.index, rotation=45, fontsize=12)

# Add data labels above each marker
for x, y in zip(year_counts.index, year_counts.values):
    plt.text(x, y + 0.5, int(y), ha='center', fontsize=10)

# Remove top and right spines for a cleaner look
sns.despine()

plt.tight_layout()
plt.show()
