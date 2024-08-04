import streamlit as st
import pandas as pd
import plotly.express as px
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
    rank_df = df[ (df['rank'] >= rank_range[0]) & 
                 (df['rank'] <= rank_range[1])]

    if use_existing_rank:
        rank_chart_df = rank_df[['Youtuber', 'rank']].set_index('Youtuber')
        st.bar_chart(rank_chart_df)
    else:
        rank_chart_df =  rank_df[['Youtuber', 'rank']].set_index('Youtuber')
        st.bar_chart(rank_chart_df)
   
    st.header('Dataset')
    st.write(df)

    # Display basic statistics
    st.header('Basic Statistics')
    st.write(df.describe())

    
    create_Line_Bar = st.selectbox('Would you like to Create line chart to display analysis over time?', ['Yes', 'No'])
    if create_Line_Bar == 'Yes':
        time_column = st.selectbox('Select Time colunm', df.columns)
        data_column = st.selectbox('Select colunm you want to display over time', df.columns)
      
        # Ensure the time column is numeric
        df[time_column] = pd.to_numeric(df[time_column], errors='coerce')
        df = df.dropna(subset=[time_column])
        df = df.sort_values(by=time_column)
        st.sidebar.header('Line Chart')
  
        # Sidebar selection for year range
        min_year = int(df[time_column].min())
        max_year = int(df[time_column].max())
        year_range = st.sidebar.slider('Select year range', min_year, max_year, (min_year, max_year))

        # Filter the dataframe by the selected year range
        line_df = df[(df[time_column] >= year_range[0]) & (df[time_column] <= year_range[1])]

        # Check if the data column is numeric or not
        if pd.api.types.is_numeric_dtype(line_df[data_column]):
            # Sum the values if the data column is numeric
            time_series = line_df.groupby(time_column)[data_column].sum().reset_index()
        else:
            # Count the occurrences if the data column is not numeric
            time_series = line_df.groupby(time_column)[data_column].count().reset_index()

        # Create the line chart
        st.line_chart(time_series.set_index(time_column)[data_column])


    
    create_pie_chart = st.selectbox('Would you like to create a pie chart?', ['Yes', 'No'])
    if create_pie_chart == 'Yes':
        category_column = st.selectbox('Select category column for pie chart', df.columns)
        value_column = st.selectbox('Select value column for pie chart', df.columns)
        # Sidebar selection for categories to include in the pie chart
        st.sidebar.header('Pie Chart')
        unique_categories = df[category_column].unique()
        selected_categories_for_pie = st.sidebar.multiselect('Select categories to include in pie chart', unique_categories, unique_categories)
        
        # Filter the dataframe by the selected categories
        pie_data = df[df[category_column].isin(selected_categories_for_pie)]
        
        # Aggregate the data for the pie chart
        pie_data = pie_data.groupby(category_column)[value_column].sum().reset_index()

        # Create the pie chart
        fig = px.pie(pie_data, names=category_column, values=value_column, title=f'Pie chart of {value_column} by {category_column}')
        st.plotly_chart(fig)
    create_bar_chart = st.selectbox('Would you like to create a bar chart?', ['Yes', 'No'])
    if create_bar_chart == 'Yes':
        category_column = st.selectbox('Select category column for bar chart', df.columns)
        value_column = st.selectbox('Select value column for bar chart', df.columns)

        # Sidebar selection for categories to include in the bar chart
        unique_categories = df[category_column].unique()
        selected_categories_for_bar = st.sidebar.multiselect('Select categories to include in bar chart', unique_categories, unique_categories)
        
        # Filter the dataframe by the selected categories
        bar_data = df[df[category_column].isin(selected_categories_for_bar)]
        
        # Aggregate the data for the bar chart
        bar_data = bar_data.groupby(category_column)[value_column].sum().reset_index()

        # Create the bar chart
        fig = px.bar(bar_data, x=category_column, y=value_column, title=f'Bar chart of {value_column} by {category_column}')
        st.plotly_chart(fig)
    st.header('Top YouTubers by Subscribers')
    top_youtubers = df.nlargest(10, 'subscribers')
    st.bar_chart(top_youtubers.set_index('Youtuber')['subscribers'])

    # Display a bar chart of top countries by total video views
    st.header('Top Countries by Total Video Views')
    country_views = df.groupby('Country')['video views'].count().nlargest(10)
    st.bar_chart(country_views)

    # Display a scatter plot of subscribers vs. video views
    st.header('Subscribers vs. Video Views')
    st.scatter_chart(df[['subscribers', 'video views']])

 
