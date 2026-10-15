import requests
import sqlite3
from datetime import datetime



url = 'https://services6.arcgis.com/bdPqSfflsdgFRVVM/arcgis/rest/services/Crime_Data_2019_Part_1_Offenses/FeatureServer/3/query?outFields=*&where=1%3D1&f=geojson'

try:
    response = requests.get(url)
    data = response.json()
except Exception as e:
    print("Error" + str(e))

conn = sqlite3.connect('crime_data.db')
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS crime_2019_1 (
    DATEEND TEXT,
    TIMESTART INTEGER,
    TIMEEND INTEGER,
    ADDRESS TEXT,
    Arrest TEXT,
    LarcenyCode TEXT,
    CODE_DEFINED TEXT,
    LAT REAL,
    LONG REAL
)
""")

try:
    for item in data.get("features", []):
        attributes = item.get("properties")

        date = attributes.get('DATEEND')
        date = date / 1000

        dt_object = datetime.utcfromtimestamp(date)
        formatted_date = dt_object.strftime('%m/%d/%Y')


        c.execute('INSERT INTO crime_2019_1 (DATEEND, TIMESTART, TIMEEND, ADDRESS, Arrest, LarcenyCode, CODE_DEFINED, LAT, LONG) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
     (formatted_date,
                 attributes.get('TIMESTART'),
                 attributes.get('TIMEEND'),
                 attributes.get('ADDRESS'),
                 attributes.get('Arrest'),
                 attributes.get('LarcenyCode'),
                 attributes.get('CODE_DEFINED'),
                 attributes.get('LAT'),
                 attributes.get('LONG')))
    conn.commit()
except Exception as e:
    print("Database error: " + str(e))
    raise



conn.close()

