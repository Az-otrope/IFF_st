import streamlit as st

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import altair as alt
from datetime import time, date, datetime
from pivot_in_pack import pivot_in_pack
from utils import upload_dataset, get_report

import warnings
warnings.filterwarnings("ignore")


# DASHBOARD
add_sidebar = st.sidebar.selectbox('Project', ('Boost','Pivot In-pack','Pivot On-seed'))
                                  
                                  
# PROJECT: Pivot In-pack   
if add_sidebar == 'Pivot In-pack':
    st.title('Pivot In-pack Data Dashboard')
    st.subheader('New Sample Information Data Entry')
   
    with st.form('sample_form'):
        # input:
        sample_id = st.text_input('FD Sample ID')
        run_id = st.text_input('FD Run ID')
        strain = st.selectbox('Strain', ['','Klebsiella variicola','Kosakonia sacchari'])
        
        eft_date = st.date_input('EFT date')
        broth_id = st.text_input('Broth ID')
        scale = st.selectbox('Fermentation Scale', ['','14L','150K'])
        ferm_cond = st.text_input('Ferm condition')
        eft = st.number_input('EFT (hr)')
        titer = st.number_input('Broth titer (CFU/mL)')
        age = st.number_input('Broth age (day)')
        
        pellet_date = st.date_input('Pelletization date')
        cryo = st.selectbox('Cryo mix', ['','DSR','PVT70%','SKP'])
        igd_1 = st.selectbox('Ingredient 1', ['','40% Sucrose','45.5% Sucrose'])
        igd_2 = st.selectbox('Ingredient 2', ['','8% KH2PO4','10% Maltodextrin','22.75% Inulin'])
        igd_3 = st.selectbox('Ingredient 3', ['','10.2% K2HPO4','0.5% MgSO4'])
        igd_4 = st.selectbox('Ingredient 4', [''])
        cryo_rate = st.number_input('Cryo mix addition rate')
        
        fd_start = st.date_input('FD start date')
        fd_recipe = st.text_input('FD cycle recipe')
        fd_p = st.text_input('FD pressure (mTorr)')
        fd_time = st.number_input('FD run time (hr)')
        rate = st.number_input('Primary ramp rate (C/min)')
        
        receive_date = st.date_input('PA receive date')
        look = st.text_input('Dried appearance')
        container = st.selectbox('Container', ['', 'Foil pouch'])
        water_act = st.number_input('Water activity')
        viability = st.number_input('Viability (CFU/g)')
        
        #yield
        #log loss
        storage = st.checkbox('Storage tracking')
        seed = st.checkbox('Seed treatment')
        note = st.text_input('Note')
        
        submitted = st.form_submit_button('Submit')
       
    
    st.subheader('CFU Plating Data')
    
    # upload data
    data=upload_dataset()
    
    if len(data) > 0:
        raw, clean = pivot_in_pack(data)
        
        # display the df
        st.write('CFU Plating data')
        st.dataframe(raw.head())
        st.write(f"DataFrame size: {len(raw)}")
        
        st.write('Processed CFU Plating Data')
        st.dataframe(clean)
        st.write(f"DataFrame size: {len(clean)}")
    
        # export data
        st.download_button(
            label="Download report as CSV",
            data=clean.to_csv(),
            file_name='large_df.csv',
            mime='text/csv')
    
        


#pivot On-seed
if add_sidebar == 'Pivot On-seed':
    st.title('Pivot On-seed Data Dashboard')
    
    data=upload_dataset()
        
    st.write('Time Range')
    exp_period = st.slider('Choose a time range of completed experiments:',
                           date(2019,1,1), date.today(),
                           value=(date(2020,1,1),date(2021,1,1)),
                           format='YYYY/MM/DD')
   
    #data preprocessing
    
    #features engineering
                                               
                                               

#boost
if add_sidebar == 'Boost':
    st.title('Boost Data Dashboard')
    
    data=upload_dataset()
    
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