import pandas as pd
import numpy as np
import sqlite3
import folium
from folium.plugins import HeatMap

# Database connection and query
conn = sqlite3.connect('crime_data.db')
query = ("""
        SELECT LONG, LAT FROM crime_2024_2
        UNION ALL
        SELECT LONG, LAT FROM crime_2024_1
        UNION ALL
        SELECT LONG, LAT FROM crime_2023_2
        UNION ALL
        SELECT LONG, LAT FROM crime_2023_1
        """)
df = pd.read_sql_query(query, conn)
conn.close()

# Convert LONG and LAT to numeric
df["LONG"] = pd.to_numeric(df["LONG"], errors="coerce")
df["LAT"] = pd.to_numeric(df["LAT"], errors="coerce")

# Drop rows with missing values
df = df.dropna(subset=["LONG", "LAT"])

# Initialize a folium map centered around the average coordinates
m = folium.Map(location=[df["LAT"].mean(), df["LONG"].mean()], zoom_start=12)

# Prepare heatmap data
heat_data = [[row['LAT'], row['LONG']] for _, row in df.iterrows()]

# Add HeatMap layer
HeatMap(heat_data, radius=10).add_to(m)

# Save and display the map
m.save("heatmap.html")
m
