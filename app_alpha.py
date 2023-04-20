import streamlit as st

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import altair as alt
from datetime import time, date, datetime

import warnings
warnings.filterwarnings("ignore")

def upload_dataset(caption: str) -> pd.DataFrame:
    """
    Let the user upload a dataset as CSV then cleans up the file contents.
    
    INPUT: a .csv file set in a template
    OUTPUT: return dataframe with relevant info
    """
    
    file = st.file_uploader(caption, type=["csv"])
    if not file:
        st.warning("Please upload a CSV file.")
        return pd.DataFrame()
        
    data = pd.read_csv(file)
    file.close()
    st.write("File uploaded successfully")

    return data

#build dashboard
st.header('Sparkle Too Data Analysis')
add_sidebar = st.sidebar.selectbox('Project', ('Boost','Pivot In-pack', 'Pivot On-seed'))


                                  
                                  
# Pivot In-pack   
if add_sidebar == 'Pivot In-pack':
    st.subheader('Pivot In-pack Data Dashboard')
    
    # Refresh the Samples master list
    st.write('Update Sample Master List (if applicable)')
    master_lst=upload_dataset('Upload Master list .csv file')
    
    
    # Upload raw CFU data
    st.write('Experimental CFU data')
    
    # ??? without try-except: the website will display an error message for index out of bounds line 61
    try:
        rawcfu_df=upload_dataset('Upload Raw CFU .csv file')
        # replace the colmns with the values of the second row
        rawcfu_df.columns = rawcfu_df.iloc[1]
        # remove the first and second rows
        rawcfu_df = rawcfu_df.iloc[2:]
        rawcfu_df = rawcfu_df.reset_index()
        # keep relevant cols
        rawcfu_df = rawcfu_df[['Batch','Date','CFU/mL','CFU/g']]
        rawcfu_df.dropna(subset=['Batch'],inplace=True)
        # display the df
        st.dataframe(rawcfu_df.head())
    except:
        st.write(' ')
    

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