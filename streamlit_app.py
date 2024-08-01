import streamlit as st
import pandas as pd

st.title('Machine Learning App')

st.write('This app builds a machine learning model')

df = pd.read_csv('data/Global_YouTube_Statistics.csv')
df
                 
                 
