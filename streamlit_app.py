#%%
import pandas as pd
import polars as pl
import pyarrow as pa
import pyarrow.parquet as pq
import streamlit as st
import plotly.express as px
import pydeck as pdk
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static


#%%
county = pl.read_parquet('data/active_members_county.parquet')
tract = pl.read_parquet("data/active_members_tract.parquet")
chapel_scrape = pl.read_parquet("data/full_church_building_data-20.parquet")
chapel_safegraph = pl.read_parquet("data/safegraph_chapel.parquet")
temples = pl.from_arrow(pq.read_table("data/temple_details_spatial.parquet"))
tract_nearest = pl.from_arrow(pq.read_table("data/tract_distance_to_nearest_temple.parquet"))



#%%

print("County Table")
print("Shape:", county.shape)
print("Columns:", county.columns)
print("Data Types:", county.dtypes)


print("\nTract Table")
print("Shape:", tract.shape)
print("Columns:", tract.columns)
print("Data Types:", tract.dtypes)


print("\nChapel Scrape Table")
print("Shape:", chapel_scrape.shape)
print("Columns:", chapel_scrape.columns)
print("Data Types:", chapel_scrape.dtypes)


print("\nChapel Safegraph Table")
print("Shape:", chapel_safegraph.shape)
print("Columns:", chapel_safegraph.columns)
print("Data Types:", chapel_safegraph.dtypes)


print("\nTemples Table")
print("Shape:", temples.shape)
print("Columns:", temples.columns)
print("Data Types:", temples.dtypes)


print("\nTract Nearest Table")
print("Shape:", tract_nearest.shape)
print("Columns:", tract_nearest.columns)
print("Data Types:", tract_nearest.dtypes)



#%%

temples.select(pl.col("country")).describe()


#%%
chapel_scrape = chapel_scrape.with_columns(pl.col("state").map_elements(str.upper, return_dtype=str))


#%%



#%%

difference = len(chapel_scrape) - len(chapel_safegraph)
percentage_difference = (difference / len(chapel_scrape)) * 100

st.title(":blue[_Question 1_]: How does the number of chapels in Safegraph compare to the number of chapels from the church website web scrape?")


st.write(f"""The number of chapels in the Safegraph dataset is less than the number of chapels in the scraped dataset.
         When comparing the number of chapels in the scraped dataset to the number of chapels in the Safegraph dataset,
            there is a difference of {difference} chapels. There could be several reasons for the discrepancies between the two datasets.
            One potential reason is that the Safegraph dataset will not collect data if it detects too few devices in a given area. 
            Another potential reason could be that the third-party sources used to create the Safegraph dataset use unreliable collection methods. 
""")
st.write(f"Compared to the scraped data, {percentage_difference:.4f}% of chapels are missing from Safegraph")
st.write(f"This translates to {difference} chapels missing from Safegraph dataset")


#%%

def calculate_differences(state):
    state_upper = state.upper()

    chapels_scrape_state = chapel_scrape.filter(chapel_scrape['state'] == state_upper)
    chapels_safegraph_state = chapel_safegraph.filter(chapel_safegraph['region'] == state_upper)

    diff = len(chapels_scrape_state) - len(chapels_safegraph_state)
    if len(chapels_scrape_state) > 0:
        percent_diff = (diff / len(chapels_scrape_state)) * 100
    else:
        percent_diff = 0  

    return diff, percent_diff, len(chapels_scrape_state), len(chapels_safegraph_state)


st.title("Chapel Comparison by State", )


selected_state = st.selectbox("Select a State", options=sorted(set(chapel_scrape['state'])))


diff, percent_diff, count_scrape, count_safegraph = calculate_differences(selected_state)
st.write(f"Difference in chapel count for {selected_state}: {diff} (Percentage difference: {percent_diff:.2f}%)")
st.write("(Note: The difference is calculated by subtracting the number of chapels in the Safegraph dataset from the number of chapels in the scraped dataset.)")

chart_data = pd.DataFrame({
    "Source": ["Web Scrape", "Safegraph"],
    "Chapel Count": [count_scrape, count_safegraph]
})


plt.figure(figsize=(10, 6))
sns.barplot(x='Source', y='Chapel Count', data=chart_data, palette=['blue', 'green'], hue='Source', legend=False)


st.pyplot(plt.gcf())


#%%

chapel_scrape_pd = chapel_scrape.to_pandas()

#%%

chapel_scrape_pd = chapel_scrape_pd.rename(columns={
    'lat': 'lat',
    'lon': 'lon',
    'zip': 'zipCode',
    'state': 'state'
})
#%%

st.title("Scraped Chapel Locations")
st.write("The map below allows you to view the locations of chapels in the scraped dataset.")



scatterplot = pdk.Layer(
    'ScatterplotLayer',
    data=chapel_scrape_pd,
    get_position='[lon, lat]',
    get_color='[200, 30, 0, 160]',
    get_radius=200,
    radiusMinPixels=5,  
    radiusMaxPixels=20,
    pickable=True,
    auto_highlight=True,
)

r = pdk.Deck(
    map_style='mapbox://styles/mapbox/satellite-streets-v11',
    initial_view_state=pdk.ViewState(
        latitude=40.2536122,
        longitude=-74.3142982,
        zoom=11,
        pitch=0,
    ),
    layers=[scatterplot],
    tooltip={
        "html": "<b>State:</b> {state} <br/> <b>Address:</b> {full_address} <br/>",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }
)

st.pydeck_chart(r)




#%%






#%%
st.title(":blue[_Question 2_]: Does the active member estimate look reasonable as compared to the tract population?")

st.title("Tract and County Data Analysis")
st.write("""
This app analyzes and visualizes the relationship between active member estimates and population data at the tract and county levels.
Use the controls below to select a state and county, and view the corresponding data visualizations.
""")






#%%

def extract_state_county(fips_code):
    state_fp = fips_code[:2]
    county_fp = fips_code[2:5]
    return state_fp, county_fp

tract = tract.with_columns([
    pl.col('home').map_elements(lambda x: extract_state_county(x)[0]).alias('state_fp'),
    pl.col('home').map_elements(lambda x: extract_state_county(x)[1]).alias('county_fp')
])

combined_data = tract.join(county, left_on=['state_fp', 'county_fp'], right_on=['STATEFP', 'COUNTYFP'])

combined_data = combined_data.with_columns((pl.col('active_members_estimate') / pl.col('population')).alias('proportion'))

scaling_factor = st.slider('Adjust active membership estimates', min_value=0.0, max_value=1.0, value=1.0)
combined_data = combined_data.with_columns((pl.col('active_members_estimate') * scaling_factor).alias('adjusted_active_members'))

st.write(f"""Note: Streamlit has a bug with selecting one state and then selecting another state without deselecting the counties. If you wish to view another state, please refresh the page
         or deselect all counties before switching states.
         If you run into an error :red[__StreamlitAPIException: Every Multiselect default value must exist in options__], refresh the page.
""")

state_names = [name for name in combined_data['state_name'].unique().to_list() if name is not None]
state_names.sort()

if 'selected_state_name' not in st.session_state or st.session_state['selected_state_name'] not in state_names:
    st.session_state['selected_state_name'] = state_names[0]

selected_state_name = st.selectbox("Select a State", state_names, index=state_names.index(st.session_state['selected_state_name']))
st.session_state['selected_state_name'] = selected_state_name

selected_state_fp = combined_data.filter(pl.col('state_name') == selected_state_name)['state_fp'].unique()[0]
state_data = combined_data.filter(pl.col('state_fp') == selected_state_fp)

county_names = [name for name in state_data['county_name'].unique().to_list() if name is not None]
county_names.sort()

if st.session_state['selected_state_name'] != selected_state_name or 'selected_county_names' not in st.session_state:
    st.session_state['selected_county_names'] = []

selected_county_names = st.multiselect("Select Counties", options=county_names, default=st.session_state['selected_county_names'])
st.session_state['selected_county_names'] = selected_county_names

selected_county_fps = state_data.filter(pl.col('county_name').is_in(selected_county_names))['county_fp'].unique().to_list()
county_data = state_data.filter(pl.col('county_fp').is_in(selected_county_fps))



#%%

if not county_data.is_empty():
    fig, axes = plt.subplots(1, 2, figsize=(20, 6))


    selected_counties_str = ', '.join(selected_county_names)


    sns.violinplot(data=county_data.to_pandas(), x='adjusted_active_members', ax=axes[0])
    axes[0].set_title(f'Violin Plot of Tract-Level Adjusted Active Members Estimate in {selected_state_name} (Counties: {selected_counties_str})')
    axes[0].set_xlabel("Adjusted Active Members Estimate")
    axes[0].set_ylabel("Density")
    

    st.write(f"""
    **Violin Plot Explanation**: 
    This violin plot shows the distribution of adjusted active members estimates at the tract level within the selected counties of {selected_state_name}. 
    The width of the plot at different values indicates the density of data points, providing insights into where the majority of estimates lie. 
    This visualization helps in understanding the variability and concentration of active members estimates across tracts.""")


    sns.histplot(data=county_data.to_pandas(), x='proportion', ax=axes[1])
    axes[1].set_title(f'Histogram of Tract-Level Proportion (Active Members Estimate / Population) in {selected_state_name} (Counties: {selected_counties_str})')
    axes[1].set_xlabel("Proportion (Active Members Estimate / Population)")
    axes[1].set_ylabel("Frequency of Tracts")
    

    st.write(f"""
    **Histogram Explanation**: 
    The histogram displays the distribution of the proportion of active members estimates to the population in each tract of {selected_state_name}. 
    It shows how frequently certain proportion values occur, allowing for an assessment of how the active member estimates compare to the tract populations. 
    A balanced distribution without extreme values suggests a reasonable alignment between the estimates and population sizes.""")

    plt.tight_layout()
    st.pyplot(fig)
else:
    st.write("No data available for the selected state and counties.")


st.write("""
**Assessment of Active Member Estimate**: 
Upon examining the data from New Jersey, the active member estimates compared to the tract population appear to be reasonable. 
The distributions in the visualizations align with expectations, passing an initial 'sniff test'. 
This suggests that, at least at a high level, the active member estimates are within a plausible range when compared to the population figures of the tracts in New Jersey.
""")

#%%








#%%



st.title(":blue[_Question 3_]: Does the active member estimate look reasonable as compared to the religious census estimates by county?")


#%%


scaling_factor = st.slider('Adjust active membership estimates', 
                           min_value=0.0, max_value=1.0, value=1.0, 
                           key='active_membership_estimates_slider')

st.write(f"""Note: Streamlit has a bug with selecting one state and then selecting another state without deselecting the counties. If you wish to view another state, please refresh the page
         or deselect all counties before switching states.
         If you run into an error :red[__StreamlitAPIException: Every Multiselect default value must exist in options__], refresh the page.
""")

county = county.with_columns(
    (pl.col('active_members_estimate') * scaling_factor).alias('scaled_active_members_estimate')
)


state_names = [name for name in county['state_name'].unique().to_list() if name is not None]
state_names.sort()

if 'selected_state_name' not in st.session_state or st.session_state['selected_state_name'] not in state_names:
    st.session_state['selected_state_name'] = state_names[0]

selected_state_name = st.selectbox("Select a State:", state_names, index=state_names.index(st.session_state['selected_state_name']))
st.session_state['selected_state_name'] = selected_state_name


state_data = county.filter(pl.col('state_name') == selected_state_name)


county_names = [name for name in state_data['county_name'].unique().to_list() if name is not None]
county_names.sort()

if st.session_state['selected_state_name'] != selected_state_name or 'selected_county_names' not in st.session_state:
    st.session_state['selected_county_names'] = []

selected_county_names = st.multiselect("Select Counties:", options=county_names, default=st.session_state['selected_county_names'])
st.session_state['selected_county_names'] = selected_county_names

selected_county_data = state_data.filter(pl.col('county_name').is_in(selected_county_names))



if not selected_county_data.is_empty():
    fig, ax = plt.subplots(figsize=(12, 6))


    selected_county_data_df = selected_county_data.to_pandas()
    selected_county_data_df.set_index('county_name')[['scaled_active_members_estimate', 'rcensus_lds']].plot(kind='bar', ax=ax)
    ax.set_title(f'Comparison of Scaled Active Members Estimate and Religious Census in {selected_state_name} (Counties: {selected_county_names})')
    ax.set_xlabel('County')
    ax.set_ylabel('Estimates')
    ax.legend(["Scaled Active Members Estimate", "Religious Census LDS"])


    plt.tight_layout()
    st.pyplot(fig)


    st.write("""
    **Bar Plot Explanation**: 
    This bar plot compares the scaled active members estimate to the religious census figures for the Mormon church in each selected county of {}. 
    The 'Scaled Active Members Estimate' represents our adjusted estimate of active Mormon members in the county, while 'Religious Census LDS' represents the reported number of members according to the religious census.
    The comparison is crucial in understanding how our estimates relate to the official figures.""".format(selected_state_name))


    st.write("Comparison Ratios (Scaled Active Members Estimate / Religious Census LDS):")
    st.table(selected_county_data_df.set_index('county_name')['ratio_census'])


    st.write("""
    **Comparison Analysis**: 
    Upon comparing the active member estimates with the religious census figures by county, it's observed that generally, the active member estimates are lower than the census figures. 
    This difference is likely because the census numbers may be inflated due to inactive members still being on the records. 
    It's not unusual or unexpected for the active members estimate to be less than the religious census figure, as our estimates attempt to reflect the number of actively participating members, rather than just registered members.
    """)
else:
    st.write("No data available for the selected state and counties.")
#%%







#%%





#%%

st.title(":blue[_Question 4_]: How does the current temple placement look by state as compared to the county active membership estimates?")

temples_us = temples.filter(pl.col("country") == "United States")




temples_county_joined = temples_us.join(county, left_on=['STATEFP', 'COUNTYFP'], right_on=['STATEFP', 'COUNTYFP'])


def create_map(show_temples):
    m = folium.Map(location=[37.0902, -95.7129], zoom_start=5)


    for _, row in temples_county_joined.to_pandas().iterrows():
        folium.Circle(
            location=[row['lat_general'], row['long_general']],
            radius=row['active_members_estimate'] / 5, 
            color='blue',
            fill=True,
            fill_color='blue',
            tooltip=f"{row['county_name']}: {row['active_members_estimate']} active members"
        ).add_to(m)


    if show_temples:
        temples_cluster = MarkerCluster().add_to(m)
        for _, temple in temples_county_joined.to_pandas().iterrows():
            folium.Marker(
                location=[temple['lat_general'], temple['long_general']],
                popup=temple['temple'],
                icon=folium.Icon(color='red', icon='glyphicon glyphicon-tower')
            ).add_to(temples_cluster)

    return m


show_temples = st.checkbox('Show Temples on Map', value=True)


st_map = create_map(show_temples)
folium_static(st_map)

st.write("""
### Analysis of Temple Placement vs. Active Membership Estimates

Upon analyzing the spatial distribution of temples in relation to the active membership estimates by county, several observations stand out:

- **In densely populated areas like New York City and Philadelphia:** The number of temples appears to be low compared to the what I would expect.

- **In areas like Utah and Idaho:** The placement of temples seems to be more closely aligned with the active membership estimates. 

It seems like the data we have is not portraying the full picture in non-LDS dense areas.
""")

