import streamlit as st

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import altair as alt
from datetime import time, date, datetime
from pivot_in_pack import pivot_in_pack

import warnings
warnings.filterwarnings("ignore")

# FUNCTIONS
def upload_dataset(caption: str) -> pd.DataFrame:
    """
    Let the user upload a dataset as CSV
    
    INPUT: a .csv file 
    
    OUTPUT: return dataframe with relevant input and calculated information
    """
    
    file = st.file_uploader(caption, type=["csv"])
    if not file:
        st.warning("Please upload a CSV file.")
        return pd.DataFrame()
        
    data = pd.read_csv(file)
    file.close()

    return data


# DASHBOARD
st.header('Sparkle Too Data Analysis')
add_sidebar = st.sidebar.selectbox('Project', ('Boost','Pivot In-pack', 'Pivot On-seed'))

                                  
                                  
# PROJECT: Pivot In-pack   
if add_sidebar == 'Pivot In-pack':
    pivot_in_pack()
    
#pivot On-seed
if add_sidebar == 'Pivot On-seed':
    st.subheader('Pivot On-seed Data Dashboard')
    
    data=upload_dataset('Upload Raw CFU .csv file')
        
    st.write('Time Range')
    exp_period = st.slider('Choose a time range of completed experiments:',
                           date(2019,1,1), date.today(),
                           value=(date(2020,1,1),date(2021,1,1)),
                           format='YYYY/MM/DD')
   
    #data preprocessing
    
    #features engineering
                                               
                                               

#boost
if add_sidebar == 'Boost':
    st.subheader('Boost Data Dashboard')
    
    data=upload_dataset('Upload Raw CFU .csv file')
    
    st.write('Time Range')
    exp_period = st.slider('Choose a time range of completed experiments:',
                           date(2019,1,1), date.today(),
                           value=(date(2020,1,1),date(2021,1,1)),
                           format='YYYY/MM/DD')
                                  
    #data preprocessing
    
    #features engineering
    
    #e.g. data visualization time series
    chart_data = pd.DataFrame(np.random.randn(20, 3),
                              columns=['a', 'b', 'c'])

    c = alt.Chart(chart_data).mark_circle().encode(
    x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

    st.altair_chart(c, use_container_width=True)