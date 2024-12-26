import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sqlite3
import matplotlib.dates as md


conn = sqlite3.connect("crime_data.db")

query = ("""
        SELECT CODE_DEFINED FROM crime_2024_2
        UNION ALL
        SELECT CODE_DEFINED FROM crime_2024_1
        UNION ALL
        SELECT CODE_DEFINED FROM crime_2023_2
        UNION ALL
        SELECT CODE_DEFINED FROM crime_2023_1
        UNION ALL
        SELECT "CODE DEFINED" FROM crime_2022_2
        UNION ALL
        SELECT CODE_DEFINED FROM crime_2022_1
        UNION ALL
        SELECT CODE_DEFINED FROM crime_2021_2
        UNION ALL
        SELECT CODE_DEFINED FROM crime_2021_1
        UNION ALL
        SELECT CODE_DEFINED FROM crime_2020_2
        UNION ALL
        SELECT CODE_DEFINED FROM crime_2020_1;
        """)

df = pd.read_sql_query(query, conn)
conn.close()

# Creates pandas series with crime and their count
'''
CODE_DEFINED
LARCENY                12135
SIMPLE ASSAULT         11477
CRIMINAL MISCHIEF       8269
BURGLARY                4494
OFFN AGAINST FAMILY     3946
'''
def toPercent(count, total):
    count = count / total
    count = count * 100
    return count


count = df['CODE_DEFINED'].value_counts()
column_total = count.sum()
count = count.apply(lambda x : toPercent(x,column_total))
print(count)
misc_total = 0
for n in count:
    if n < 5:
        misc_total = misc_total + n

new_row = pd.Series([misc_total], index=["OTHER OFFENCES"])
count = pd.concat([count, new_row])
filtered_count = count[count > 5]
filtered_count = filtered_count.fillna(0).astype(int)


custom_labels = [f"{index} ({size}%)" for index, size in filtered_count.items()]

for n in custom_labels:
    print(n)

plt.figure(figsize=(15,10))
plt.title("Crime Type Breakdown")
plt.pie(filtered_count.values, labels=custom_labels)
plt.show()