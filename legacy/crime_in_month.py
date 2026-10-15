import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime

conn = sqlite3.connect('crime_data.db')
query = ("""
        SELECT DATEEND FROM crime_2024_2
        UNION ALL
        SELECT DATEEND FROM crime_2024_1
        UNION ALL
        SELECT DATEEND FROM crime_2023_2
        UNION ALL
        SELECT DATEEND FROM crime_2023_1
        UNION ALL
        SELECT DATEEND FROM crime_2022_2
        UNION ALL
        SELECT DATEEND FROM crime_2022_1
        UNION ALL
        SELECT DATEEND FROM crime_2021_2
        UNION ALL
        SELECT DATEEND FROM crime_2021_1
        UNION ALL
        SELECT DATEEND FROM crime_2020_2
        UNION ALL
        SELECT DATEEND FROM crime_2020_1;
        """)

df = pd.read_sql_query(query, conn)
conn.close()

def toDate(date):
    date = date[:-12]
    try:
        date_object = datetime.strptime(date, "%Y/%m/%d")
        return date_object
    except(ValueError, TypeError):
        return None




df['DATEEND'] = df['DATEEND'].apply(toDate)

date_counts = df['DATEEND'].dt.day.value_counts().sort_index()
date_counts = date_counts[date_counts.index <= 30]


print(date_counts)

plt.figure(figsize=(15,10))
plt.plot(date_counts.index, date_counts.values, marker='.')
plt.ylim(1000, max(date_counts.values) + 500)
plt.xticks(range(1,31))
plt.title("Crime in a Month")
plt.xlabel("Day of Month")
plt.ylabel("Number of crimes")

plt.show()




