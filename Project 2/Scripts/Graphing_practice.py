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
    path=["city", "collection", "shelfMark"],          # Column that defines the grouping
    values="bindingWidth",         # Controls the size of each rectangle
    color="folios",        # Controls the colour shading
    
)

fig.show()
