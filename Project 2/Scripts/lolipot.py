import pandas as pd
from collections import Counter
import plotly.express as px

# -------------------------
# Load CSV
# -------------------------
df = pd.read_csv("articles_3.csv")

# Normalize columns
df.columns = df.columns.str.strip().str.lower()
df['text'] = df['text'].astype(str).str.lower()

# -------------------------
# Keywords
# -------------------------
illegal_keywords = [
    "illegal", "undocumented", "unauthorised",
    "without permit", "no work permit", "overstayed",
    "foreign worker", "migrant worker"
]

sectors = [
    "construction", "restaurant", "hotel", "farm", "agriculture",
    "factory", "delivery", "cleaning", "hospitality", "shop", "security"
]

# -------------------------
# Tagging functions
# -------------------------
def find_sectors(text):
    return [s for s in sectors if s in text]

def has_illegal(text):
    return any(k in text for k in illegal_keywords)

# -------------------------
# Filter + count
# -------------------------
df_illegal = df[df['text'].apply(has_illegal)]

sector_counts = Counter()

for text in df_illegal['text']:
    for s in find_sectors(text):
        sector_counts[s] += 1

# -------------------------
# DataFrame creation
# -------------------------
sector_df = pd.DataFrame(
    sector_counts.items(),
    columns=["Sector", "Frequency"]
).sort_values(by="Frequency", ascending=True)

# -------------------------
# Plotly Express LOLLIPOP
# -------------------------
import plotly.express as px

# Sort from highest to lowest
sector_df = sector_df.sort_values(by="Frequency", ascending=False)

# Ensure Sector is categorical (keeps order)
sector_df["Sector"] = pd.Categorical(
    sector_df["Sector"],
    categories=sector_df["Sector"],
    ordered=True
)

# DOTS
fig = px.scatter(
    sector_df,
    x="Sector",
    y="Frequency"
)

# STEMS
for _, row in sector_df.iterrows():
    fig.add_shape(
        type="line",
        x0=row["Sector"],
        x1=row["Sector"],
        y0=0,
        y1=row["Frequency"],
        line=dict(width=2)
    )

fig.update_traces(marker=dict(size=14))

fig.update_layout(
    title="Sectors Associated with Illegal Migrant Work in BBC News",
    xaxis_title="Employment Sector",
    yaxis_title="Number of Articles",
    template="plotly_white"
)

fig.update_xaxes(tickangle=45)

fig.show()






