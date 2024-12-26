import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime

conn = sqlite3.connect('crime_data.db')
query = ("""
        SELECT DATEEND FROM crime_2023_1
        UNION ALL
        SELECT DATEEND FROM crime_2023_2;
        """)
df_2023 = pd.read_sql_query(query, conn)
query = ("""
        SELECT DATEEND FROM crime_2022_1
        UNION ALL
        SELECT DATEEND FROM crime_2022_2;
        """)
df_2022 = pd.read_sql_query(query, conn)
query = "SELECT DATEEND FROM crime_2022_2"
df_test = pd.read_sql_query(query, conn)

query = ("""
        SELECT DATEEND FROM crime_2021_1
        UNION ALL
        SELECT DATEEND FROM crime_2021_2;
        """)
df_2021 = pd.read_sql_query(query, conn)
query = ("""
        SELECT DATEEND FROM crime_2020_1
        UNION ALL
        SELECT DATEEND FROM crime_2020_2;
        """)
df_2020 = pd.read_sql_query(query, conn)

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


df_2023['DATEEND'] = df_2023['DATEEND'].apply(toDate)
df_2022['DATEEND'] = df_2022['DATEEND'].apply(toDate)
df_2021['DATEEND'] = df_2021['DATEEND'].apply(toDate)
df_2020['DATEEND'] = df_2020['DATEEND'].apply(toDate)


y_values_2023 = []
y_values_2022 = []
y_values_2021 = []
y_values_2020 = []
for month in range(1,13):
    y_values_2023.append(df_2023.loc[df_2023['DATEEND'].dt.month == month].count().iloc[0])
    y_values_2022.append(df_2022.loc[df_2022['DATEEND'].dt.month == month].count().iloc[0])
    y_values_2021.append(df_2021.loc[df_2021['DATEEND'].dt.month == month].count().iloc[0])
    y_values_2020.append(df_2020.loc[df_2020['DATEEND'].dt.month == month].count().iloc[0])


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

plt.plot(x_values, y_values_2023, marker='.', linestyle='-', label="2023")
plt.plot(x_values, y_values_2022, marker='.', linestyle='-', label="2022")
plt.plot(x_values, y_values_2021, marker='.', linestyle='-', label="2021")
plt.plot(x_values, y_values_2020, marker='.', linestyle='-', label="2020")

plt.title("Number of Crimes Committed Per Month")
plt.xlabel("Month")
plt.ylabel("Number of Crimes Commited")
plt.legend()

plt.show()
