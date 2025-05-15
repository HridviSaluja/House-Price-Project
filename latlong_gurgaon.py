import requests
import pandas as pd
import time

def get_coordinates_osm(sector):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": f"Sector {sector}, Gurgaon, India",
        "format": "json",
        "limit": 1
    }
    response = requests.get(url, params=params, headers={"User-Agent": "Mozilla"})
    
    if response.status_code == 200:
        data = response.json()
        if data:
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            return f"{lat}, {lon}"
    return None

# Use a list to store sector-coordinate pairs
data = []

# Iterate over sectors and collect data
for sector in range(1, 116):
    coordinates = get_coordinates_osm(sector)
    print(f"Sector {sector}: {coordinates}")
    data.append({"Sector": f"Sector {sector}", "Coordinates": coordinates})
    time.sleep(1)  # be polite with API usage (1 request/second)

# Create DataFrame and save
df = pd.DataFrame(data)
df.to_csv("gurgaon_sectors_coordinates.csv", index=False)
