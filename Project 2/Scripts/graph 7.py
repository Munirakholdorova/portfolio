import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------------
# LOAD DATA
# -----------------------------------------
csv_file = "/Users/munirakholdorova/Documents/bbc_uk_illegal_work_articles_balanced.csv"
df = pd.read_csv(csv_file)

# -----------------------------------------
# EXCLUDE PARTIAL YEAR (2025)
# -----------------------------------------
df = df[df["year"] < 2025]

# -----------------------------------------
# COUNT ARTICLES PER YEAR
# -----------------------------------------
all_years = list(range(2000, 2025))
year_counts = df["year"].value_counts().reindex(all_years, fill_value=0)

# -----------------------------------------
# CALCULATE YEAR-TO-YEAR DIFFERENCE
# -----------------------------------------
year_diff = year_counts.diff().fillna(0)  # difference from previous year

# -----------------------------------------
# PLOT TIME SERIES AND DIFFERENCE
# -----------------------------------------
plt.figure(figsize=(12, 6))

# Plot original counts
plt.plot(year_counts.index, year_counts.values, marker='o', label="Articles per Year", color="blue")

# Plot year-to-year differences as a bar chart
plt.bar(year_diff.index, year_diff.values, alpha=0.3, color="orange", label="Year-to-Year Difference")

plt.xlabel("Year")
plt.ylabel("Number of Articles")
plt.title("BBC News Articles on Illegal Working in the UK (2000–2024) \nwith Year-to-Year Changes")
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()
