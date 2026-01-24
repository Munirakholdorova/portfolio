import pandas as pd
from collections import Counter
import plotly.express as px

# -------------------------
# 1️⃣ LOAD CSV
# -------------------------
# Update this path to the correct location of your CSV
csv_path = "/Users/munirakholdorova/Downloads/Hmml/bbc_uk_illegal_work_articles_4.csv"
df = pd.read_csv(csv_path)

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Lowercase text for consistent matching
df['text'] = df['text'].astype(str).str.lower()

# -------------------------
# 2️⃣ DEFINE SECTOR KEYWORDS
# -------------------------
sectors = [
    "construction", "restaurant", "hotel", "farm", "agriculture",
    "factory", "delivery", "cleaning", "hospitality",
    "shop", "security", "social care", "retail", 
    "private hire", "taxi", "courier"
]

# -------------------------
# 3️⃣ TAGGING FUNCTION
# -------------------------
def find_sectors(text):
    """
    Returns a list of sector keywords found in the text.
    """
    return [s for s in sectors if s in text]

# -------------------------
# 4️⃣ COUNT SECTOR FREQUENCIES
# -------------------------
sector_counts = Counter()

for text in df['text']:
    for s in find_sectors(text):
        sector_counts[s] += 1

# -------------------------
# 5️⃣ CREATE DATAFRAME FOR PLOTTING
# -------------------------
sector_df = pd.DataFrame(
    sector_counts.items(),
    columns=["Sector", "Frequency"]
).sort_values(by="Frequency", ascending=True)

# Sort from highest to lowest for plotting
sector_df = sector_df.sort_values(by="Frequency", ascending=False)

# Ensure Sector is categorical to preserve order in the plot
sector_df["Sector"] = pd.Categorical(
    sector_df["Sector"],
    categories=sector_df["Sector"],
    ordered=True
)

# -------------------------
# 6️⃣ PLOTLY LOLLIPOP CHART
# -------------------------
fig = px.scatter(
    sector_df,
    x="Sector",
    y="Frequency",
    size_max=20
)

# Add stems (lines from 0 to the dot)
for _, row in sector_df.iterrows():
    fig.add_shape(
        type="line",
        x0=row["Sector"],
        x1=row["Sector"],
        y0=0,
        y1=row["Frequency"],
        line=dict(width=2)
    )

# Customize markers
fig.update_traces(marker=dict(size=14, color='blue'))

# Layout
fig.update_layout(
    title="Sectors Mentioned in BBC Articles on Illegal Work in the UK",
    xaxis_title="Employment Sector",
    yaxis_title="Number of Articles",
    template="plotly_white"
)

fig.update_xaxes(tickangle=45)

fig.show()
