# ==========================================================
# BBC News Choropleth Maps for UK and England (with manual mappings)
# ==========================================================

import pandas as pd
import plotly.express as px
import json

# ==============================
# Step 1: Load CSV
# ==============================
df = pd.read_csv("bbc_uk_illegal_work_articles_with_places.csv")

# ==============================
# Step 2a: Large-region counts
# ==============================
region_counts = df['large_region'].value_counts().reset_index()
region_counts.columns = ['region', 'count']

# Drop 'UK' from large_region
region_counts = region_counts[region_counts['region'] != 'UK']

print("Articles per large_region:")
print(region_counts)

# ==============================
# Step 2b: Local-region counts
# ==============================
local_counts = df['local_region'].value_counts().reset_index()
local_counts.columns = ['local_region', 'count']

# Drop unwanted non-England entries
exclude_local = ['Scotland Politics', 'Scotland', 'Wales Politics', 'nan']
local_counts = local_counts[~local_counts['local_region'].isin(exclude_local)]
local_counts = local_counts.dropna(subset=['local_region'])

print("\nArticles per local_region (filtered):")
print(local_counts)

# ==============================
# Step 3: Load GeoJSONs
# ==============================
with open("large_area.geojson") as f:
    large_geojson = json.load(f)

with open("small_area.json") as f:
    small_geojson = json.load(f)

# ==============================
# Step 4: UK large-region choropleth
# ==============================
fig_large = px.choropleth(
    region_counts,
    geojson=large_geojson,
    locations='region',
    featureidkey='properties.CTRY21NM',
    color='count',
    color_continuous_scale='Blues',
    title='BBC News Article Counts by UK Region'
)
fig_large.update_geos(fitbounds="geojson", visible=False)
fig_large.update_traces(hovertemplate='<b>%{location}</b><br>Articles: %{z}<extra></extra>')
fig_large.show()
fig_large.write_html("bbc_news_uk_choropleth.html")

# ==============================
# Step 5: Manual mapping for local regions
# ==============================
manual_mapping = {
    'London': ['City', 'Hackney', 'Westminster', 'Camden', 'Islington', 'Kensington and Chelsea',
               'Hounslow', 'Ealing', 'Hammersmith and Fulham', 'Wandsworth', 'Merton', 'Brent',
               'Sutton', 'Croydon', 'Lewisham', 'Greenwich', 'Hackney', 'Southwark', 'Lambeth',
               'Kingston upon Thames', 'Newham', 'Haringey', 'Redbridge', 'Havering', 'Barking and Dagenham',
               'Enfield', 'Barnet', 'Waltham Forest', 'Hillingdon', 'Harrow', 'Bexley', 'Richmond upon Thames', 'City'],
    'Stoke & Staffordshire': ['Stoke-on-Trent', 'Staffordshire', 'Telford and Wrekin'],
    'South Yorkshire': ['Sheffield', 'Doncaster', 'Barnsley', 'Rotherham'],
    'West Yorkshire': ['Bradford', 'Leeds', 'Wakefield', 'Calderdale', 'Kirklees'],
    'Berkshire': ['West Berkshire', 'Wokingham', 'Bracknell Forest', 'Royal Borough of Windsor and Maidenhead', 'Slough', 'Reading'],
    'Beds, Herts & Bucks': ['Bedford', 'Central Bedfordshire', 'Luton', 'Hertfordshire', 'Milton Keynes', 'Buckinghamshire'],
    'Hereford & Worcester': ['Herefordshire', 'Worcestershire'],
    'Birmingham & Black Country': ['Birmingham', 'Walsall', 'Wolverhampton', 'Sandwell', 'Dudley'],
    'Wear': ['Sunderland', 'South Tyneside', 'Durham', 'Gateshead'],
    'Tees': ['Darlington', 'Hartlepool', 'Middlesbrough', 'Redcar and Cleveland', 'Stockton-on-Tees']
}


# Initialize new DataFrame for mapped regions
small_region_names = [f['properties']['name'] for f in small_geojson['features']]
mapped_counts = pd.DataFrame({'local_region': small_region_names})
mapped_counts['count'] = 0

# Sum counts for manual mapping
for original_name, geo_names in manual_mapping.items():
    count = local_counts.loc[local_counts['local_region'] == original_name, 'count'].sum()
    for geo_name in geo_names:
        if geo_name in mapped_counts['local_region'].values:
            mapped_counts.loc[mapped_counts['local_region'] == geo_name, 'count'] += count

# Fill remaining counts (regions that match directly)
for idx, row in local_counts.iterrows():
    if row['local_region'] not in manual_mapping.keys():
        if row['local_region'] in mapped_counts['local_region'].values:
            mapped_counts.loc[mapped_counts['local_region'] == row['local_region'], 'count'] = row['count']

# ==============================
# Step 6: England local-region choropleth
# ==============================
fig_small = px.choropleth(
    mapped_counts,
    geojson=small_geojson,
    locations='local_region',
    featureidkey='properties.name',
    color='count',
    color_continuous_scale='Oranges',
    title='BBC News Article Counts by Local Region (England)'
)
fig_small.update_geos(fitbounds="geojson", visible=False)
fig_small.update_traces(hovertemplate='<b>%{location}</b><br>Articles: %{z}<extra></extra>')
fig_small.show()
fig_small.write_html("bbc_news_england_lad_choropleth.html")

print("Maps created successfully!")
