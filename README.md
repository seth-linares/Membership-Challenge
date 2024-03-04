# Link to GitHub Repository for Seth Linares
[Github Repository](https://github.com/sethlinares/app_challenge_membership_fa23)




# Challenge General Information

You can read the details of the challenge at [challenge.md](challenge.md)

## Key Items

- __Due Date:__ December 13, 2023
- __Work Rules:__ You cannot work with others.  You can ask any question you want in our general channel. Teacher and TA are the only one that can answer questions. If you leverage code from an internet connection, then it should be referenced.
- __Product:__ A streamlit app that runs within Docker and builds from your repo. Additionally, a fully documented `readme.md`.
- __Github Process:__ Each student will fork the challenge repository and create their app. They will submit a link to the app in Canvas.
- __Canvas Process:__ Each student will upload a `.pdf` or `.html` file with your results as described in [challenge.md](challenge.md)


## Notes & References

- [Fork a repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
- [Creating a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)

### Docker Information

Within this repository, you can simply run `docker compose up` to leverage the `docker-compose.yaml` with your local folder synced with the container folder where the streamlit app is running. 

Additionally, you can use `docker build -t streamlit .` to use the `Dockerfile` to build the image and then use `docker run -p 8501:8501 -v "$(pwd):/app:rw" streamlit` to start the container with the appropriate port and volume settings.

We currently use `python:3.11.6-slim` in our [Dockerfile](Dockerfile).  You can change to `FROM quay.io/jupyter/minimal-notebook` to use the [minimal Jupyter notebook](https://quay.io/organization/jupyter)



# Target Scripts for review

## Cmd 5: Filter and process pattern data
Cmd 5 in the given Pyspark code is involved in filtering and processing various datasets, primarily focusing on geographic and time-based data. The process begins with a subset of the "tract_table" dataset after filtering for LDS buildings and then further filtered to exclusively regions labeled as "ID". The spatial data processing segment involves joining and filtering operations based on "placekey", while making sure to use a left_semi join to retain only the rows from spatial dataframe that have a match in the poi dataframe. The same technique is also used for spatial_idaho dataframe, where the left_semi join is used between spatial and poi_idaho dataframes on the placekey field, retaining only the rows from spatial dataframe that have a match in the poi_idaho dataframe. The pattern dataset is processed similarly, with additional steps to extract year and month information from a "date_range_start" column, filter for the year 2019, and inner join with the POI dataset. The command concludes by creating a new database and saving these processed datasets as tables ready to be used for analysis.

### Suggestions
The code could be improved by dealing with some of the redundant code. For example, the same filtering operation is performed on the pattern and pattern_idaho datasets as well as the spatial datasets. This could be simplified by just creating the more general spatial and pattern datasets and then filtering them later on in the code rather than going through and processing the specific ID dataset all over again. Overall the code isn"t awful but it could be improved to make it more efficient and easier to understand.

## Cmd 22: Traffic Filter to Chapel Algorithm
Cmd 22 deals with a complex analysis of patterns related to chapel visits, using data from a table named "chapel.pattern_idaho". The code begins by defining a window partition which descends by value and is grouped by "placekey" and "date_range_start". This is then used to rank the popular days for the chapels. There are 2 percentiles that the coder tried to make, 50th and 70th. We use this to try and identify chapels based on their popularity on Sundays and Mondays. The logic here is to select places that are most popular on Sundays (ranked in the top 3) and least popular on Mondays (ranked in the bottom 4). This part concludes by joining this processed data with the poi table to add location details like street address and city, and then saving the result as a new table.

### Suggestions
One of the biggest issues that I noticed when first going over the code is the improper assignment and creation of percentiles. The same percentile value was used both for the 50th and 70th, making them both effectively look at the 70th percentile. Based on the use of these percentiles that would completely skew the results if not addressed. I feel like it is also important to note that despite some professor's beleifs that trying to squish as many operations into a single block as is possible, it does really suffer in terms of following the logic of the process. Another problem I noticed was that sometimes methods were chained when unnecessary such as 2 filters in a row when one would be sufficient. 


## Cmd 50: US Spread Active Members to tracts
Cmd 50 in the PySpark code is involved in combining and refining data from two different tables (chapel.chapel_nearest and chapel.use_pattern_chapel) to identify relevant locations for an analysis focused on chapel visits. The process begins by loading these tables into the nearest and pattern dataFrames respectively. The main thing being done here is a full join of these two dataFrames on the "placekey" field. This join renames certain columns in the nearest dataFrame for clarity ("street_address" to "nearest_address" and "initial_address" to "scrape_address"), and by selecting specific fields for the join operation. The filtering applied after the join are pretty specifi. It focuses on entries where "Sunday" = 1, or "Sunday" = 2 and "dist" is not null or where "dist" is less than or equal to 0.0003 and "city" is null. The data is then sorted by "placekey" and descending "dist", with duplicates dropped based on "placekey".

### Suggestions

I think the only improvements and/or fixes I would add would be possibly splitting up the cell. I think defining the tables within the same cell as your main join and filtering doesn"t feel right to me at least. I believe that it would make it both more readable and easier to deal with errors if/when they pop up in your code logic. I suppose the only other thing I think is a bit odd is the use of the full join. It could cause issues with null values in the resulting dataframe so I would be careful with that. I think that the code is pretty good overall though.

## Cmd 60: Sunday Visitor Estimates
Cmd 60 focuses on estimating visitor counts to chapels on Sundays. It involves joining and processing data from multiple tables: "chapel.placekey_chapel", "chapel.pattern", and "safegraph.censustract_pkmap". The process starts by joining the patterns DataFrame with pk_final on "placekey". This join filters the dataset to focus only on chapels. An important part of this process is the extraction and analysis of visit data by day by using selectExpr along with posexplode_outer. The code then joins this data with pk_tract to add "tractcode" information and calculates the exact date of the visit using date_add. The subsequent filtering to keep only records where "dayofweek" equals 1 (Sunday) shows the focus on Sunday visitors. The aggregation functions then calculate various statistics like count, sum, median, minimum, and maximum of the visit counts. An additional column "sunday_visits" is computed to estimate normalized visit counts. The final aggregation step consolidates these estimates at the "placekey" level, and the results are saved as a new table and displayed.

### Suggestions

I think a potential problem that stand out to me is with the left join, you open yourself up to the risk of nulls being present within the data. If you do this, you need to be prepared to deal with the nulls in some way. I think that the code is written decently so I don"t notice any glaring issues.


## Cmd 64
In Cmd 64, a new SQL table named membership.home_dist is created. This table is formed by selecting specific columns from the dat_distance_all table. The columns selected include "placekey", "home", "region", "value", "raw_visitor_counts", and "date_range_start". Notably, a new column point_placekey is created using the ST_Point function to generate geographical points from "longitude" and "latitude" values. Another column, "dist", is calculated using the ST_DISTANCE function to compute the distance between each "point_placekey" and a "center_home" point, with the distance being multiplied by 69.

### Suggestions
In this part of the code SQL was used which is something I haven"t used in a decent while. When trying to look for issues, I think the main thing that raises my eyebrows is the use of the ST_DISTANCE function and using 69 as a conversion factor like this. I get that the developer is trying to get the distance and that the distance between any two adjacent latitudes is approximately 69 miles, but I believe that this could be done perhaps by using a function that is more specific to the task at hand. I think that the code is pretty good overall though and my suggestion might not even be necessary.

## Cmd 66
Cmd 66 combines data from home_weight and sunday tables to estimate active chapel members per tract. The process begins by selecting specific columns from home_weight and joining it with the sunday table. The key operation here is the creation of two new columns, typical_sunday and active_members. The typical_sunday column is calculated using a conditional statement: if the "median" is less than or equal to 16, it uses the "max" value. Otherwise it uses the "median". The active_members column is calculated by multiplying this "median" by "home_weight". The resulting data is then grouped by "home" and aggregated to estimate the total number of active members, which is rounded to the nearest whole number.

### Suggestions
The code looks clean. I"ve harped on this numerous times but I think that the use of the left join could cause some issues and definitely needs to be considered closely. I don"t think that there are any other issues that I can see with the code.

## Cmd 74
Cmd 74 is trying to create a comparison at the county level, using data on active chapel members, census data, and population figures. The process involves joining the county_target DataFrame with a modified version of the rel_cens DataFrame, where the column "Church of Jesus Christ of Latter-day Saints" is renamed to "rcensus_lds". This joined data is further enhanced by calculating two ratios: ratio_census and ratio_population. These ratios are computed by dividing the estimated active members by the LDS census data and the total population, respectively. The aim is likely to assess the proportion of active chapel members in relation to the broader population and specific religious demographics. The final DataFrame is then saved as a new table and displayed.

### Suggestions
I don"t really see any issues. Maybe it's because I"m tired, but at this point the last few have seemed pretty clean to me. The left join is still something I would mention if being pedantic, but I think that the code is pretty good.


# Vocabulary

## 1. The Added Value of DataBricks in Data Science Process

DataBricks offers significant value in the data science process due to its unified platform, which seamlessly integrates various components required for data science workflows. Firstly, it provides a collaborative environment where data scientists, data engineers, and business analysts can work together efficiently. Its integration with popular languages like Python, R, and Scala, and compatibility with libraries like TensorFlow, PyTorch, and XGBoost, make it a versatile tool for diverse data science needs.

The platform excels in handling large-scale data processing with its robust cloud-based infrastructure, making it ideal for big data analytics. The interactive notebooks in DataBricks allow for easy data exploration, visualization, and sharing of insights. Furthermore, its MLflow integration streamlines the machine learning lifecycle from experimentation to deployment, enabling better tracking and management of machine learning models. DataBricks also ensures high data security standards, making it a reliable choice for sensitive data projects.

## 2. Comparison of PySpark and Pandas/Tidyverse

PySpark and Pandas (or the Tidyverse in R) are both powerful tools for data manipulation, but they cater to different needs and scales of data. 

PySpark, part of the Apache Spark ecosystem, is designed for big data processing. It excels in handling large datasets that do not fit into the memory of a single machine, offering distributed data processing capabilities. PySpark is well-suited for complex data pipelines, real-time data processing, and large-scale data analytics, thanks to its ability to parallelize tasks across multiple nodes in a cluster.

On the other hand, Pandas (or Tidyverse in R) is more user-friendly and is ideal for data analysis on a single machine. It provides an extensive set of functions for data manipulation, cleaning, and visualization. Pandas is great for small to medium-sized datasets and is more intuitive for users familiar with SQL or Excel. Its simplicity and rich functionality make it a favorite for exploratory data analysis and prototyping.

In summary, while PySpark is geared towards distributed, large-scale data processing, Pandas/Tidyverse is more suitable for single-machine, in-memory data tasks.

## 3. Explaining Docker to a Non-Tech Person

Imagine Docker as a system that allows you to package an application with all the parts it needs into a single package called a container. This container can then be easily moved and run on any computer that has Docker installed, regardless of the underlying operating system or setup. 

It's like having a portable work environment that you can take with you anywhere, ensuring that your application will work exactly the same way, regardless of where it's deployed. This eliminates the common problem of an application working on one person’s computer but not another's due to different configurations or settings.

Docker provides consistency and efficiency, simplifying the process of developing, testing, and deploying applications, making it a valuable tool in software development and deployment processes.


# Feature Challenge Explanation


## Simple Feature: Tract Population Density

#### Definition
The feature "Tract Population Density" tries to quantify the number of people per unit area within each census tract. It is calculated by dividing the total population of a tract by its land area (in square meters). This metric provides insights into how densely populated different areas are.

#### Why can this be useful?
1. **Urban Planning and Development**: High population density areas might indicate urban regions, potentially requiring more infrastructure, public services, and amenities. Conversely, lower-density areas might signify rural or less developed regions.
2. **Economic Activity**: Areas with higher population densities often correlate with increased economic activity, including retail, services, and employment opportunities.
3. **Environmental Impact**: Understanding population density helps in assessing the environmental stress in an area, including resource utilization, waste generation, and ecological footprints.
4. **Social Services**: Densely populated areas may have different social service needs, such as healthcare, education, and transportation services.

#### Interpretation of the Map
The map created using Plotly Express visually represents the population density across different tracts. Here's how to interpret it:

- **Size of Points**: Larger points indicate tracts with higher population density. Smaller points represent less densely populated tracts.
- **Color of Points**: The color gradient (usually from cool to warm colors) shows the spectrum of population density, with warmer colors typically representing higher densities.
- **Interactivity**: Hovering over a point reveals specific data about that tract, such as the exact population density value.

#### Interpretation of the Data
When analyzing the population density data:

1. **Compare Densities**: Look for variations in population density between different tracts. This can highlight regional differences in population distribution.
2. **Identify Trends**: Areas with similar densities might have common characteristics or needs. These trends can inform regional planning and policy-making.


#### Limitations and Considerations
- **Relatively Small Number**: Because of the way the feature is calculated, the population density values are relatively small. This can make it difficult for humans to interpret the data. I believe that the data is still useful for machine learning models and can provide some value to the model's predictions.
- **Temporal Dynamics**: Population density is not static; it changes over time due to factors like migration, development, and natural events.
- **Spatial Resolution**: The tract level analysis may not capture finer-grained population variations within tracts.

#### Conclusion
The "Tract Population Density" feature is a crucial metric in urban planning, economic development, and resource allocation. It can help identify regional differences in population distribution and highlight areas with similar characteristics or needs. This information can be especially useful for leaders of the church to understand the needs of the members in their area and to plan for future growth in regards to building new churches and temples.


## Complex Feature: Average Visit Duration at LDS Churches by Tract

#### Definition
This feature, "Average Visit Duration at LDS Churches by Tract," represents the average length of time visitors spend at Latter-day Saints (LDS) church buildings within each census tract. The calculation is based on the median dwell time recorded for visits to identified LDS churches.

#### Significance
1. **Community Engagement**: Longer average visit durations might indicate higher levels of community engagement or more extensive church activities.
2. **Church Activity Rate**: Understanding how long visitors stay can help church leaders identify which areas have more active churchgoers.

#### Interpretation of the Data
When analyzing the average visit duration data:

1. **Duration Analysis**: Look at the average duration times across different tracts. Longer durations might imply more engaging church activities or a more dedicated congregation.
2. **Comparative Analysis**: Comparing visit durations across different areas can reveal variations in religious practice intensity or church engagement.
3. **Correlation with Membership Estimates**: Understanding how visit durations relate to active membership estimates can offer insights into the church's role in community life.

### Visualization Interpretation

The scatter plot visualization of average visit duration versus active members estimate provides a visual correlation between these two metrics.

- **X-Axis (Average Visit Duration)**: This represents the average time spent by visitors at LDS churches in a tract.
- **Y-Axis (Active Members Estimate)**: This shows the estimated number of active church members in each tract.
- **Data Points**: Each point on the plot represents a census tract. The position of the point indicates both its average visit duration and active members estimate.
- **Trends and Outliers**: Look for patterns or outliers in the scatter plot. For example, tracts with unusually high visit durations or active member estimates might warrant further investigation.

### Limitations and Considerations
- **Temporal Factors**: The data might be influenced by temporal factors like holidays, special events, or seasonal variations in church attendance.
- **Cultural and Demographic Influences**: The church visit durations might be affected by local cultural or demographic factors, which should be considered when interpreting the data.

### Conclusion
The "Average Visit Duration at LDS Churches by Tract" feature offers valuable insights into church engagement and community participation in religious activities. By analyzing and visualizing this data, we can better understand the dynamics of which areas have higher church attendance and identify areas of strong or weak engagement within the community. This analysis can be particularly useful for predicting the next temple location.