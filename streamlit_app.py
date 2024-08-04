import streamlit as st
import pandas as pd

# Function to load the preloaded dataset
@st.cache
def load_preloaded_data():
    data_path = 'data/Global_YouTube_Statistics.csv'
    df = pd.read_csv(data_path)
    df.columns = df.columns.str.strip()
    df['Country'] = df['Country'].str.title()
    numeric_columns = ['subscribers', 'video views', 'uploads', 'video_views_rank', 
                       'country_rank', 'channel_type_rank', 'video_views_for_the_last_30_days', 
                       'lowest_monthly_earnings', 'highest_monthly_earnings', 
                       'lowest_yearly_earnings', 'highest_yearly_earnings', 'created_year']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')
    df = df.dropna(subset=['subscribers', 'video views', 'uploads'])
    df = df.drop_duplicates()
    return df

# Title of the Streamlit app
st.title('Global YouTube Statistics Dashboard')

# Main screen options
st.header("Choose a dataset")
option = st.selectbox("Select an option:", ("Upload a CSV file", "Use YouTube Statistics"))

# Initialize an empty DataFrame
df = pd.DataFrame()

if option == "Upload a CSV file":
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")

elif option == "Use YouTube Statistics":
    df = load_preloaded_data()
    st.success("Loaded YouTube Statistics dataset!")

# If DataFrame is not empty, display the data and visualizations
if not df.empty:
    st.header('Dataset')
    st.write(df)

    # Display basic statistics
    st.header('Basic Statistics')
    st.write(df.describe())

      # Option to use existing rank column or create a new rank
    use_existing_rank = st.sidebar.checkbox('My dataset has Rank colunm', value=True)
    
    # Rank column selection and ranking logic
    if not use_existing_rank:
        rank_column = st.sidebar.selectbox('Select column to grenerate rank by', df.columns)
        df['rank'] = df[rank_column].rank(method='min', ascending=False)

        # Slider to filter by rank
    min_rank = int(df['rank'].min())
    max_rank = int(df['rank'].max())
    rank_range = st.sidebar.slider('Select rank range', min_rank, max_rank, (min_rank, max_rank))

    if use_existing_rank:
        rank_chart_df = df[['Youtuber', 'rank']].set_index('Youtuber')
        st.bar_chart(rank_chart_df)
    else:
        rank_chart_df = df[[rank_column, 'rank']].set_index('rank_column')
        st.bar_chart(rank_chart_df)
   


    # Display a bar chart of top YouTubers by subscribers
    st.header('Top YouTubers by Subscribers')
    top_youtubers = df.nlargest(10, 'subscribers')
    st.bar_chart(top_youtubers.set_index('Youtuber')['subscribers'])

    # Display a bar chart of top countries by total video views
    st.header('Top Countries by Total Video Views')
    country_views = df.groupby('Country')['video views'].sum().nlargest(10)
    st.bar_chart(country_views)

    # Display a scatter plot of subscribers vs. video views
    st.header('Subscribers vs. Video Views')
    st.scatter_chart(df[['subscribers', 'video views']])

    # Group by category and calculate the mean of video views
    st.header('Mean of Video Views by Category')
    mean_video_views_by_category = df.groupby('category')['video views'].mean().reset_index()
    st.write(mean_video_views_by_category)
    st.bar_chart(mean_video_views_by_category.set_index('category'))
