Ivan Chen
Syracuse Crime Analysis


Introduction:

As a Syracuse University student and a resident in upstate NY, the health of my local communities is of great importance to me. The city of Syracuse consistently ranks as one of the most dangerous cities in New York, with a violent crime rate of around 891 incidents per 100,000 people, which is currently the third highest in the state. From my own personal experiences, I've noticed many Syracuse University students feel unsafe to venture beyond the confines of the campus. This is a major issue and as a community, we need to take actionable steps towards fixing this issue. Before we can do that though, we need to understand this problem. We need to understand the ins and outs of this problem; what time of day do we see the most crime? What time of the year is crime most common? Where in the city is crime most common? And more. These are questions that need to be answered before we can take any actionable steps towards fixing this issue and building a safer tomorrow. 

Data Summary:

This report presents an exploratory data analysis of crime data spanning from 2020 to 2024. This analysis aims to identify patterns and provide key insights to improve public safety. The dataset that this analysis is based on consists of 40,151 records detailing crime incidents, categorized by type, time, and location. 

Exploratory data analysis:
![crime-type](https://github.com/user-attachments/assets/a753c6ef-bd51-4691-83c5-387f2a6637c1)
Observation: The pie chart categorizes crimes into types, with the largest proportions being Larceny (21%), Simple Assault (20%), and Other Offences (15%).
Analysis:
High Prevalence of Larceny: Theft-related crimes (Larceny) make up the largest category, indicating a need for measures like increased security for businesses and public education on theft prevention.
Assault-Related Crimes: Simple Assault (20%) is the second-most common type of crime, suggesting a need for interventions addressing interpersonal violence.
Other Offences: The 15% under "Other Offences" likely encompasses various smaller categories, requiring further breakdown to identify actionable patterns.
Smaller Crime Types:
Criminal Mischief (14%): Vandalism and property damage.
Burglary (8%): Highlights the need for better home and business security systems.
Family and Aggravated Assault (7%): Indicates issues related to domestic violence.
Motor Vehicle Theft (5%): Suggests the importance of car security systems and public awareness.
Recommendations:
Implement neighborhood watch programs and public safety campaigns to combat theft and vandalism.
Focus on community and school programs to address interpersonal violence and domestic issues.
Deploy targeted measures for vehicle theft prevention, such as parking security.











![crime-per-month](https://github.com/user-attachments/assets/26ef164a-f550-4db4-ba4e-d173f2fa15bd)




Observation: This graph compares monthly crime counts across multiple years. August shows the highest crime rates in most years, while December has the lowest.
Analysis:
The spike in August could correlate with increased outdoor activities, travel, and events during the summer.
The drop in December could reflect reduced activity due to holidays or colder weather, leading to fewer crimes.








![crime-in-week](https://github.com/user-attachments/assets/dd0d59dc-3b37-482c-93af-f90d36793382)



















Observation: This graph highlights the number of crimes committed on each day of the week. Monday has the highest number of crimes, while Thursday has the lowest.
Analysis:
Monday's spike could be related to increased reporting of weekend incidents or the resumption of regular activities that contribute to higher crime reporting.
The lower crime rates on Thursday may be associated with reduced activity mid-week, before the weekend.

![crime-per-day-2023](https://github.com/user-attachments/assets/a987ee6d-2518-4262-b98f-e20df2f75e37)


Observation: This scatter plot shows crime counts per day in 2023. A slight upward trend is visible in the number of crimes throughout the year.
Analysis:
The upward trend indicates a gradual increase in crime as the year progresses. This could be influenced by seasonal effects, with more crimes during warmer months or increased reporting as the year advances.
Outliers with high crime counts might represent specific incidents or events.
![crime-per-day](https://github.com/user-attachments/assets/279fda5a-0c05-4516-971c-21b5b26afc27)



Observation: This scatter plot aggregates crime counts over multiple years, from 2020 to 2024. The data is spread evenly, with some spikes exceeding 70 crimes on certain days.
Analysis:
There are no major deviations or trends over the years, indicating a relatively stable level of crime day-to-day.
The spikes might represent specific events, public holidays, or other factors that drive short-term increases in crime.
Observation: This graph compares monthly crime counts across multiple years. August shows the highest crime rates in most years, while December has the lowest.
Analysis:
The spike in August could correlate with increased outdoor activities, travel, and events during the summer.
The drop in December could reflect reduced activity due to holidays or colder weather, leading to fewer crimes.

![crime-in-month](https://github.com/user-attachments/assets/3598a428-5a71-4ac9-91cd-80617816f174)



Observation: This line graph represents the number of crimes committed on each day of a specific month. The crime counts fluctuate between 1,400 and 2,200, with a general downward trend toward the end of the month.
Analysis:
Fluctuations in Daily Crime: The daily crime rates show noticeable peaks and troughs, indicating no consistent pattern day-to-day within the month.
End-of-Month Drop: The sharp decline toward the end of the month may indicate reporting or administrative delays. Alternatively, this could suggest lower activity or enforcement measures.
Mid-Month Stability: The crime rates in the middle of the month appear more consistent, with smaller variations between days.
Recommendations: Investigate why crime rates drop at the end of the month, possibly by examining reporting procedures or seasonal variations.

![percentage-per-month](https://github.com/user-attachments/assets/9f73340b-0435-40d5-8f1d-9f36a561a1a3)



Observation: This line graph shows the percentage of crimes committed in each month as a fraction of the total for the year. The percentages hover between 8% and 12%, with a slight downward trend toward the later months of the year.
Analysis:
Spring and Early Summer Peaks: The months of March, April, and May show higher percentages of crimes, possibly linked to increased activities and favorable weather conditions that contribute to criminal opportunities.
Late-Year Decline: The drop in percentages during November and December could be due to colder weather, holiday-related activities, or fewer interactions in public spaces.
Consistency Mid-Year: The months of June through October maintain a relatively stable percentage, suggesting steady activity during the late spring and summer.


![crime-map](https://github.com/user-attachments/assets/30cb6cb9-6cee-4215-a144-001a7d58be30)



Hotspots Identified: Crime activity is concentrated in urban areas and high-traffic zones, particularly in downtown regions, near commercial hubs, and along major roadways.
Sparse Areas: The outskirts and suburban regions show significantly fewer crimes, suggesting a lower density of incidents in these areas.
Possible Factors:
High population density in urban areas may lead to increased opportunities for crime.
The presence of businesses and public facilities might attract criminal activity.
Public transportation routes could contribute to higher crime rates along specific corridors.
Recommendations:
Focus law enforcement efforts in the identified hotspots.
Install more surveillance cameras and street lighting in high-crime areas.
Conduct community outreach programs in these zones to raise awareness and improve safety.


Conclusion
This analysis identifies key areas for action to reduce crime and improve public safety. Geospatial data highlights urban centers and high-traffic areas as major crime hotspots, suggesting the need for targeted interventions, such as deploying additional law enforcement, installing surveillance cameras, and improving lighting in these zones. Community engagement programs, such as neighborhood watch groups, can also play a vital role in deterring crime in these areas.
Temporal trends reveal that crime rates peak during spring and summer months, particularly in March, April, and August, which indicates the importance of allocating resources seasonally. Law enforcement presence should be increased during these months, while community programs and public awareness campaigns can help address the root causes of these spikes. The end-of-month and end-of-year declines in crime suggest that administrative factors or behavioral changes may influence reporting, which can be addressed by ensuring consistent reporting mechanisms.
The breakdown of crime types emphasizes the need to combat larceny and simple assault, which together account for a significant proportion of crimes. Theft prevention programs, public education on securing personal and business property, and partnerships with local businesses can help reduce larceny. Simultaneously, addressing interpersonal violence through community education and conflict resolution programs can reduce assaults.
