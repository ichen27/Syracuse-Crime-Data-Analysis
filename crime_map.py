import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import geopandas as gpd
from shapely.geometry import Point
import contextily as ctx

conn = sqlite3.connect('crime_data.db')
query = ("""
        SELECT LONG, LAT FROM crime_2024_2
        UNION ALL
        SELECT LONG, LAT FROM crime_2024_1
        UNION ALL
        SELECT LONG, LAT FROM crime_2023_2
        UNION ALL
        SELECT LONG, LAT FROM crime_2023_1;
        """)

df = pd.read_sql_query(query, conn)
conn.close()

df["LONG"] = pd.to_numeric(df["LONG"], errors="coerce")
df["LAT"] = pd.to_numeric(df["LAT"], errors="coerce")

points = gpd.points_from_xy(df["LONG"], df["LAT"], crs="EPSG:4326")
gdf = gpd.GeoDataFrame(df, geometry=points)

# Reproject to Web Mercator (EPSG:3857)
gdf = gdf.to_crs(epsg=3857)
map = gpd.GeoDataFrame (df, geometry=points)

fig, ax = plt.subplots(figsize=(20, 15))  # Adjust width and height
gdf.plot(ax=ax, aspect=1, color="red", markersize=10)
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)  # Add basemap

plt.title("Crime Data Map (2023-2024)")
plt.tight_layout()
plt.show()

