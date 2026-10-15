import pandas as pd
import numpy as np
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



y_values = []
for month in range(1,13):
    y_values.append(df.loc[df['DATEEND'].dt.month == month].count().iloc[0])


x_values = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


'''
jan = df.loc[df['DATEEND'].dt.month == 1].count().iloc[0]
feb = df.loc[df['DATEEND'].dt.month == 2].count().iloc[0]
mar = df.loc[df['DATEEND'].dt.month == 3].count().iloc[0]
apr = df.loc[df['DATEEND'].dt.month == 4].count().iloc[0]
may = df.loc[df['DATEEND'].dt.month == 5].count().iloc[0]
jun = df.loc[df['DATEEND'].dt.month == 6].count().iloc[0]
jul = df.loc[df['DATEEND'].dt.month == 7].count().iloc[0]
aug = df.loc[df['DATEEND'].dt.month == 8].count().iloc[0]
sep = df.loc[df['DATEEND'].dt.month == 9].count().iloc[0]
oct = df.loc[df['DATEEND'].dt.month == 10].count().iloc[0]
nov = df.loc[df['DATEEND'].dt.month == 11].count().iloc[0]
dec = df.loc[df['DATEEND'].dt.month == 12].count().iloc[0]


y_values = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
'''
total_crimes = 0
for x in y_values:
    total_crimes = total_crimes + x
y_percentages = []
for x in y_values:
    x = x / total_crimes
    y_percentages.append(x)
for x,y in zip(y_percentages, x_values):
    print(f"{x}: {y}")

plt.plot(x_values, y_percentages, marker='.', linestyle='-')
plt.ylim(0, 0.15)
plt.title("Percentage of Crimes Committed Per Month")
plt.xlabel("Month")
plt.ylabel("Percentage of Crimes Commited")

plt.show()
