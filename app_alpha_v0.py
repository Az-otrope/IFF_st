import streamlit as st

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import altair as alt
from datetime import time, date, datetime

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
    st.write("File uploaded successfully")

    return data


# DASHBOARD
st.header('Sparkle Too Data Analysis')
add_sidebar = st.sidebar.selectbox('Project', ('Boost','Pivot In-pack', 'Pivot On-seed'))

                                  
                                  
# PROJECT: Pivot In-pack   
if add_sidebar == 'Pivot In-pack':
    st.subheader('Pivot In-pack Data Dashboard')
    
    # Refresh the Samples master list
    #st.write('New Sample Information (if applicable)')
    #master_lst=upload_dataset('Upload Master list .csv file')
    
    
    # Upload raw CFU data
    st.write('Experimental CFU data')
    rawcfu_df=upload_dataset('Upload Raw CFU .csv file')
    
    # data preprocessing
    if len(rawcfu_df) >0:
        # replace the columns with the values of the second row
        rawcfu_df.columns = rawcfu_df.iloc[1]
        # remove the first and second rows
        rawcfu_df = rawcfu_df.iloc[2:]
        # reset index
        rawcfu_df = rawcfu_df.reset_index()
        # keep relevant cols
        rawcfu_df = rawcfu_df[['Batch','T0','Date','CFU/mL','CFU/g','CV','Water Activity']]
        # remove rows with NaN in 'Batch" col
        rawcfu_df.dropna(subset=['Batch'],inplace=True)
        
        
        # convert to datetime for T0 and Date
        rawcfu_df[['T0','Date']] = rawcfu_df[['T0','Date']].apply(pd.to_datetime, format="%m/%d/%y")
        
        # calculate the time point of plating
        ## by days
        rawcfu_df['Time point (day)'] = (rawcfu_df['Date']-rawcfu_df['T0']).apply(lambda x: x.days)
        ## by weeks
        to_week = rawcfu_df[['T0','Date']]
        for i in to_week.columns:
            to_week[i] = to_week[i].apply(lambda x:x.week)
        rawcfu_df['Time point (week)'] = to_week['Date'] - to_week['T0']    
        
        # remove percentage sign for CV values while ignoring invalid values
        for idx, row in rawcfu_df.iterrows():
            try:
                rawcfu_df.loc[idx, "CV"] = float(row['CV'].split("%")[0])
            except Exception as e:
                pass
        
        # handle invalid values and change to float
        to_float = rawcfu_df[['CFU/mL','CFU/g','CV','Water Activity']]
        for col in to_float.columns:
            rawcfu_df[col] = rawcfu_df[col].replace('#DIV/0!', np.NaN)
            rawcfu_df[col] = rawcfu_df[col].astype(float)      
            
        # change col names
        rawcfu_df.rename(columns={'Batch':'FD Run ID', 'CV':'CV (%)'}, inplace=True)
        # display the df
        st.dataframe(rawcfu_df)
    
    st.write('Time Range')
    exp_period = st.slider('Choose a time range of completed experiments:',
                           date(2019,1,1), date.today(),
                           value=(date(2020,1,1),date(2021,1,1)),
                           format='YYYY/MM/DD')
   
    
    
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