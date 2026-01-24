import json

# For large area
with open("large_area.geojson") as f:
    geo = json.load(f)
print(geo['features'][0]['properties'].keys())  # Shows all property names

# For small area
with open("uk_lad.json") as f:
    geo = json.load(f)
print(geo['features'][0]['properties'].keys())  # Shows all property names
