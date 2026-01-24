import pandas as pd
import json

# ==========================================================
# Step 1: Load CSV
# ==========================================================
df = pd.read_csv("bbc_uk_illegal_work_articles_with_places.csv")

large_csv = df['large_region'].str.strip().unique()
local_csv = df['local_region'].str.strip().unique()

print("CSV large_region values:")
print(large_csv)
print("\nCSV local_region values:")
print(local_csv)

# ==========================================================
# Step 2: Load GeoJSONs
# ==========================================================
with open("large_area.geojson") as f:
    large_geojson = json.load(f)

with open("small_area.json") as f:
    small_geojson = json.load(f)

# ==========================================================
# Step 3: Extract region names from GeoJSON
# ==========================================================
large_geo_names = [feature['properties']['CTRY21NM'] for feature in large_geojson['features']]
small_geo_names = [feature['properties']['name'] for feature in small_geojson['features']]

print("\nGeoJSON large-area region names:")
print(large_geo_names)

print("\nGeoJSON small-area region names:")
print(small_geo_names)

# ==========================================================
# Step 4: Check for mismatches
# ==========================================================
# Large regions not in GeoJSON
missing_large = [name for name in large_csv if name not in large_geo_names]
print("\nCSV large_region names NOT in GeoJSON:")
print(missing_large if missing_large else "All matched!")

# Local regions not in GeoJSON
missing_local = [name for name in local_csv if name not in small_geo_names]
print("\nCSV local_region names NOT in GeoJSON:")
print(missing_local if missing_local else "All matched!")
