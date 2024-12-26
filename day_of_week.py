import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime

conn = sqlite3.connect('crime_data.db')

query = "SELECT * FROM crime_2023_1;"
df = pd.read_sql_query(query, conn)


df['DATEEND'] = pd.to_datetime(df['DATEEND'], format='%Y/%m/%d %H:%M:%S%z')

mon = df.loc[df['DATEEND'].dt.dayofweek == 0].count().iloc[0]
tue = df.loc[df['DATEEND'].dt.dayofweek == 1].count().iloc[0]
wed = df.loc[df['DATEEND'].dt.dayofweek == 2].count().iloc[0]
thur = df.loc[df['DATEEND'].dt.dayofweek == 3].count().iloc[0]
fri = df.loc[df['DATEEND'].dt.dayofweek == 4].count().iloc[0]
sat = df.loc[df['DATEEND'].dt.dayofweek == 5].count().iloc[0]
sun = df.loc[df['DATEEND'].dt.dayofweek == 6].count().iloc[0]


x_values = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
y_values = [mon, tue, wed, thur, fri, sat, sun]

# Plot the data
plt.plot(x_values, y_values, marker='.', linestyle='-', label="2023")

plt.title("Day of the Week with the Highest Crime Rate")
plt.xlabel("Week")
plt.ylabel("Number of Crimes Commited")

plt.show()
