import streamlit as st
import pandas as pd

st.title('Machine Learning App')

st.write('This app builds a machine learning model')
df = pd.read_csv('data/Global_YouTube_Statistics.csv')



# Title of the Streamlit app
st.title('Global YouTube Statistics Dashboard')

min_rank, max_rank = int(df['rank'].min()), int(df['rank'].max())
rank_range = st.sidebar.slider('Select rank range', min_rank, max_rank, (min_rank, max_rank))

rank_df = df[(df['rank'] >= rank_range[0]) & 
                 (df['rank'] <= rank_range[1])]

# Sidebar for user input
st.sidebar.header('Filter Options')

# Filter by country
countries = df['Country'].unique()
selected_countries = st.sidebar.multiselect('Select countries', countries, countries)

# Filter by category
categories = df['category'].unique()
selected_categories = st.sidebar.multiselect('Select categories', categories, categories)

# Apply filters
filtered_df = df[(df['Country'].isin(selected_countries)) & (df['category'].isin(selected_categories))]

# Display the filtered DataFrame
st.header('Filtered Data')
st.write(filtered_df)

# Display basic statistics
st.header('Basic Statistics')
st.write(filtered_df.describe())

# Display a bar chart of top YouTubers by subscribers
st.header('Top YouTubers by Subscribers')
top_youtubers = filtered_df.nlargest(10, 'subscribers')
st.bar_chart(top_youtubers.set_index('Youtuber')['subscribers'])

# Display a bar chart of top countries by total video views
st.header('Top Countries by Total Video Views')
country_views = filtered_df.groupby('Country')['video views'].sum().nlargest(10)
st.bar_chart(country_views)

# Display a scatter plot of subscribers vs. video views
st.header('Subscribers vs. Video Views')
st.scatter_chart(filtered_df[['subscribers', 'video views']])


