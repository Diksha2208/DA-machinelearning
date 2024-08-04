import pandas as pd
import pandas_profiling
import streamlit as st
from streamlit_pandas_profiling import st_profile_report

option = st.sidebar.selectbox("Choose a dataset:", ("Load a dataset", "Use example dataset"))

if option == "Load a dataset":
    uploaded_file = st.sidebar.file_uploader("Upload a dataset (CSV file)", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        # perform data profiling using Pandas-Profiling
        pr = df.profile_report()
        st.header("**Dataset:**")
        st.write(df)
        if st.sidebar.button("Generate Report"):
            st.write("---")
            st.header("**Pandas Profiling Report**")
            st_profile_report(pr)

if option == "Use example dataset":
    dataset = st.sidebar.selectbox("Try a preloaded dataset:", ("Diabetes dataset", "Chronic Kidney Disease Dataset"))
    if dataset == "Youtubedataset":
        df = pd.read_csv("data/Global_YouTube_Statistics.csv")
        # perform data profiling using Pandas-Profiling
        pr = df.profile_report()
        st.header("**Dataset:**")
        st.write(df)
        if st.sidebar.button("Generate Report"):
            st.write("---")
            st.header("**Pandas Profiling Report**")
            st_profile_report(pr)


