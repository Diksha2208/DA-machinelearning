import pandas as pd
import pandas_profiling
import streamlit as st
from streamlit_pandas_profiling import st_profile_report

# Function to load the dataset
@st.cache
def load_example_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Sidebar options
st.sidebar.header("Options")
option = st.sidebar.selectbox("Choose a dataset:", ("Load a dataset", "Use example dataset"))

# Upload a dataset
if option == "Load a dataset":
    uploaded_file = st.sidebar.file_uploader("Upload a dataset (CSV file)", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        pr = df.profile_report()
        st.header("**Dataset:**")
        st.write(df)
        if st.sidebar.button("Generate Report"):
            st.write("---")
            st.header("**Pandas Profiling Report**")
            st_profile_report(pr)

# Use an example dataset
elif option == "Use example dataset":
    dataset = st.sidebar.selectbox("Select an example dataset:", ("Diabetes dataset", "Chronic Kidney Disease Dataset", "YouTube dataset"))
    
    if dataset == "Diabetes dataset":
        df = load_example_data("data/diabetes.csv")  # Replace with actual path to your dataset
    elif dataset == "Chronic Kidney Disease Dataset":
        df = load_example_data("data/chronic_kidney_disease.csv")  # Replace with actual path to your dataset
    elif dataset == "YouTube dataset":
        df = load_example_data("data/Global_YouTube_Statistics.csv")  # Replace with actual path to your dataset
    
    pr = df.profile_report()
    st.header("**Dataset:**")
    st.write(df)
    if st.sidebar.button("Generate Report"):
        st.write("---")
        st.header("**Pandas Profiling Report**")
        st_profile_report(pr)
