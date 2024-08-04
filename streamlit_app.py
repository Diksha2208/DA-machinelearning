import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    data_path = 'data/Global_YouTube_Statistics.csv'
    df = pd.read_csv(data_path)
    
    return df
df = load_data()

# Title of the Streamlit app
st.title('Global YouTube Statistics Dashboard')

min_rank= int(df['rank'].min())
rank_range = st.sidebar.slider('Select rank range', min_rank, 50, (min_rank, 50))

rank_df = df[(df['rank'] >= rank_range[0]) & 
                 (df['rank'] <= rank_range[1])]

rank_df
# Display a bar chart of top YouTube channels by rank
st.header('Top YouTube Channels by World Rank')
rank_chart_df = rank_df[['Youtuber', 'rank']].set_index('Youtuber')
st.bar_chart(rank_chart_df)

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


