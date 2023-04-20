import streamlit as st

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import altair as alt
from datetime import time, date, datetime

def upload_dataset(caption: str) -> pd.DataFrame:
    """
    Let the user upload a dataset as CSV then cleans up the file contents.
    
    INPUT: a .csv file set in a template
    
    OUTPUT: a clean dataframe with relevant info
    """

    file = st.file_uploader(caption, type=["csv"])
    if not file:
        st.warning("Please upload a CSV file.")
        return pd.DataFrame()
    
    # read in the template and select relevant information
    data = pd.read_csv(file, skiprows=2)
    data = data[['Batch','Date','CFU/mL','CFU/g']]
    data.dropna(subset=['Batch'],inplace=True)

    st.write(f"DataFrame size: {len(data)}")
    file.close()
    st.dataframe(data.head())

    return data

#build dashboard
st.header('Sparkle Too Data Analysis')
add_sidebar = st.sidebar.selectbox('Project', ('Boost','Pivot In-pack', 'Pivot On-seed'))


                                  
                                  
#pivot In-pack   
if add_sidebar == 'Pivot In-pack':
    st.subheader('Pivot In-pack Data Dashboard')
    
    data=upload_dataset('Upload CSV file')
        
    st.write('Time Range')
    exp_period = st.slider('Choose a time range of completed experiments:',
                           date(2019,1,1), date.today(),
                           value=(date(2020,1,1),date(2021,1,1)),
                           format='YYYY/MM/DD')
   
    #data preprocessing
    
    #features engineering

#pivot On-seed
if add_sidebar == 'Pivot On-seed':
    st.subheader('Pivot On-seed Data Dashboard')
    
    data=upload_dataset('Upload CSV file')
        
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
    
    data=upload_dataset('Upload CSV file')
    
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