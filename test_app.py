import streamlit as st

import numpy as np
import pandas as pd
#import plotly.graph_objects as go
#import plotly.express as px
from datetime import time, date, datetime

def upload_dataset(caption: str) -> pd.DataFrame:
    """Let the user upload a dataset as CSV"""

    file = st.file_uploader(caption, type=["csv"])
    if not file:
        st.warning("Please upload a CSV file.")
        return pd.DataFrame()
    data = pd.read_csv(file)
    st.write(f"DataFrame size: {len(data)}")
    file.close()
    st.dataframe(data.head())

    return data

st.header('Sparkle Too Data Analysis')

#build dashboard
add_sidebar = st.sidebar.selectbox('Project', ('Boost','Pivot'))

#boost
if add_sidebar == 'Boost':
    st.write('Boost Data Dashboard')
    
    st.subheader('Time Range')
    exp_period = st.slider('Choose a time range of completed experiments:',
                                  value=(date(2019,1,1), date.today()))
    
    data=upload_dataset('Upload the file')
                                  
    #data preprocessing
    
    #features engineering
                                  
                                  
#pivot    
if add_sidebar == 'Pivot':
    st.write('Pivot Data Dashboard')
    
    #data preprocessing
    
    #features engineering

