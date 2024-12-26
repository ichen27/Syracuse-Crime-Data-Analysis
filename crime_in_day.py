import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime



conn = sqlite3.connect('crime_data.db')
query = ("""
        SELECT TIMESTART FROM crime_2024_2
        UNION ALL
        SELECT TIMESTART FROM crime_2024_1
        UNION ALL
        SELECT TIMESTART FROM crime_2023_2
        UNION ALL
        SELECT TIMESTART FROM crime_2023_1
        UNION ALL
        SELECT TIMESTART FROM crime_2022_2
        UNION ALL
        SELECT TIMESTART FROM crime_2022_1
        UNION ALL
        SELECT TIMESTART FROM crime_2021_2
        UNION ALL
        SELECT TIMESTART FROM crime_2021_1
        UNION ALL
        SELECT TIMESTART FROM crime_2020_2
        UNION ALL
        SELECT TIMESTART FROM crime_2020_1;
        """)

df = pd.read_sql_query(query, conn)
conn.close()

def toTime(military_time):
    try:
        military_time = int(military_time)
        military_time_str = f"{military_time:04d}"
        # Step 2: Convert it to a datetime object using strptime
        time_obj = datetime.strptime(military_time_str, "%H%M")

        # Step 3: Format it to regular time (12-hour format with AM/PM)
        regular_time = time_obj.strftime("%I:%M %p")
        return regular_time
    except(ValueError, TypeError):
        return None


df["TIMESTART"] = df["TIMESTART"].apply(toTime)

df['TIMESTART'] = pd.to_datetime(df['TIMESTART'], format='%I:%M %p')

df['HOUR'] = df['TIMESTART'].dt.hour



plt.figure(figsize=(15, 8))
plt.hist(df['HOUR'], bins=range(0, 25), edgecolor='black', align='left', color='skyblue')

# Customize the plot
plt.title('Crimes Committed in a Day (Over the past 4 Years)', fontsize=16)
plt.xlabel('Time', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.xticks(range(0, 24), ['12AM', '1AM', '2AM', '3AM', '4AM', '5AM', '6AM', '7AM', '8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM', '8PM', '9PM', '10PM', '11PM'])  # Ensure all hours (0-23) are labeled
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.show()