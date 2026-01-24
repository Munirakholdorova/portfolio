import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------------
# LOAD DATA
# -----------------------------------------
csv_file = "bbc_uk_illegal_work_articles_balanced.csv"
df = pd.read_csv(csv_file)

# -----------------------------------------
# EXCLUDE ANY FUTURE YEAR (if accidentally included)
# -----------------------------------------
df = df[df["year"] <= 2024]

# -----------------------------------------
# ENSURE ALL YEARS 2000–2024 ARE PRESENT
# -----------------------------------------
all_years = pd.Series(range(2000, 2025))
year_counts = df["year"].value_counts().sort_index()
year_counts = year_counts.reindex(all_years, fill_value=0)

# -----------------------------------------
# OPTIONAL: SMOOTH THE TREND
# -----------------------------------------
# Simple moving average (window=3) to reduce noise
smoothed_counts = year_counts.rolling(window=3, center=True, min_periods=1).mean()

# -----------------------------------------
# PLOT TIME SERIES
# -----------------------------------------
plt.figure(figsize=(12, 6))

# Plot original counts as bars
plt.bar(year_counts.index, year_counts.values, color='lightblue', label='Articles per Year')

# Plot smoothed line
plt.plot(smoothed_counts.index, smoothed_counts.values, color='red', marker='o', label='Smoothed Trend')

plt.xlabel("Year")
plt.ylabel("Number of Articles")
plt.title("BBC News Articles on Illegal Working in the UK (2000–2024)")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()
