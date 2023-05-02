#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 00:26:40 2023

@author: miu
"""
import streamlit as st
from utils import upload_dataset
import pandas as pd
from datetime import time, date, datetime
import numpy as np


def pivot_in_pack():
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
        rawcfu_df = rawcfu_df[['Batch','Sample Description','Storage form','Temperature-Celsius',
                               'T0','Date','CFU/mL','CFU/g','CV','Water Activity']]
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
        rawcfu_df.rename(columns={'Batch':'FD Run ID', 'Temperature-Celsius':'Temperature (C)', 'CV':'CV (%)'}, inplace=True)
        # display the df
        st.dataframe(rawcfu_df)
    
    st.write('Time Range')
    exp_period = st.slider('Choose a time range of completed experiments:',
                           date(2019,1,1), date.today(),
                           value=(date(2020,1,1),date(2021,1,1)),
                           format='YYYY/MM/DD')
   
    
    
    #features engineering
