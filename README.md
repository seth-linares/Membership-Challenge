# LDS Church Membership Analysis

## Getting Started

Within this repository, you can simply run `docker compose up` to leverage the `docker-compose.yaml` with your local folder synced with the container folder where the streamlit app is running. 

Additionally, you can use `docker build -t streamlit .` to use the `Dockerfile` to build the image and then use `docker run -p 8501:8501 -v "$(pwd):/app:rw" streamlit` to start the container with the appropriate port and volume settings.

We currently use `python:3.11.6-slim` in our [Dockerfile](Dockerfile).  You can change to `FROM quay.io/jupyter/minimal-notebook` to use the [minimal Jupyter notebook](https://quay.io/organization/jupyter)


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