import pandas as pd
import plotly.express as px

csv_path = "hmml_subset.csv"
df = pd.read_csv(csv_path)

print(df.info())
print(df.columns)
print(df.head(5).transpose())


# CREATE THE TREEMAP
fig = px.treemap(
    df,
    path=["Category"],          # Column that defines the grouping
    values="SizeValue",         # Controls the size of each rectangle
    color="ColourValue",        # Controls the colour shading
    color_continuous_scale="Viridis"   # Or "Plasma", "Blues", etc.
)

fig.show()
