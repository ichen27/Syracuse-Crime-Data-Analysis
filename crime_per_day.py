import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime

conn = sqlite3.connect("crime_data.db")
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
        if(date_object.year >= 2020):
            return date_object
        else:
            return None
    except(ValueError, TypeError):
        try:
            date_object = datetime.strptime(date, "%m/%d/%Y")
            if (date_object.year >= 2020):
                return date_object
            else:
                return None
        except(ValueError, TypeError):
            return None



df['DATEEND'] = df['DATEEND'].apply(toDate)

date_counts = df['DATEEND'].value_counts().sort_index()
dates = mdates.date2num(date_counts.index)

slope, intercept = np.polyfit(dates, date_counts.values, 1)
best_fit_line = slope * dates + intercept


# Plot
plt.figure(figsize=(15, 10))
plt.scatter(date_counts.index, date_counts.values, color='#abcdef', edgecolors='blue', s=100, marker='o')
plt.plot(date_counts.index, best_fit_line, label='Best Fit Line', color='Green', linestyle='--')




plt.ylabel("Number of Crimes Committed Per Day")
plt.xlabel("Date")
plt.title("Crime Counts by Date")

plt.savefig("crime_per_day1.png", dpi=300)
plt.show()