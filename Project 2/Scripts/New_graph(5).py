import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
# COLOR SCHEME
# -----------------------------------------
# Use shades of blue and red (light to medium)
colors = [
    "#1f77b4",  # blue
    "#aec7e8",  # light blue
    "#ff7f0e",  # muted red (not too dark)
    "#ff9896",  # light red
    "#2ca02c"   # mild greenish-blue (safe)
]

# Map colors cyclically if years exceed color count
bar_colors = [colors[i % len(colors)] for i in range(len(year_counts))]

# -----------------------------------------
# PLOT TIME SERIES
# -----------------------------------------
plt.figure(figsize=(14, 7))

# Bars
bars = plt.bar(year_counts.index, year_counts.values, color=bar_colors, edgecolor='gray', alpha=0.9)

# Trend line (smooth quadratic)
z = np.polyfit(year_counts.index, year_counts.values, 2)
p = np.poly1d(z)
plt.plot(year_counts.index, p(year_counts.index), color='#d62728', linestyle='--', linewidth=2, label='Trend')

# Add data labels
for bar in bars:
    height = bar.get_height()
    if height > 0:
        plt.text(bar.get_x() + bar.get_width()/2, height + 0.5, int(height), ha='center', fontsize=10, color='#333333')

# Labels and title
plt.xlabel("Year", fontsize=12)
plt.ylabel("Number of Articles", fontsize=12)
plt.title("BBC News Articles on Illegal Working in the UK (2010–2024)", fontsize=16)
plt.xticks(year_counts.index, rotation=45)
plt.yticks()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()
