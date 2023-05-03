#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 00:26:40 2023

@author: miu
"""
import streamlit as st
import pandas as pd
from datetime import time, date, datetime
import numpy as np

from utils import upload_dataset


def pivot_in_pack():
    
    # Upload raw CFU data
    st.write('Experimental CFU data')
    rawcfu_df=upload_dataset('Upload Raw CFU .csv file')
    
    # data cleaning and processing
    if len(rawcfu_df) >0:
        rawcfu_df.columns = rawcfu_df.iloc[1]
        rawcfu_df = rawcfu_df.iloc[2:]
        rawcfu_df = rawcfu_df.reset_index()
        # remove rows with NaN in 'Batch" col
        rawcfu_df.dropna(subset=['Batch'],inplace=True)
        # keep relevant cols
        rawcfu_df = rawcfu_df[['Batch','Sample Description','Storage form','Temperature-Celsius',
                               'T0','Date','CFU/mL','CFU/g','CV','Water Activity']]
        
        # convert to datetime for T0 and Date
        rawcfu_df[['T0','Date']] = rawcfu_df[['T0','Date']].apply(pd.to_datetime, format="%m/%d/%y")
        
        # calculate the time point by days and weeks of plating
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
        
        # Record the CFUs by week for each ID
        pivot_rawcfu = rawcfu_df.pivot(index='FD Run ID', columns='Time point (week)', values=['CFU/mL','CFU/g'])
        # rename the column by the counting week
        pivot_rawcfu.columns = [f"W{week}_{scale}" for scale, week in pivot_rawcfu.columns.to_list()]
        
        # remove cols that cause repeated samples
        cfu = rawcfu_df.drop(['T0','Date','CFU/mL','CFU/g','CV (%)','Time point (day)','Time point (week)'],axis=1)
        # drop duplicated IDs
        cfu.drop_duplicates(subset='FD Run ID', inplace=True)
        
        # join the pivot df with the original info
        cleaned_cfu = pd.merge(cfu, pivot_rawcfu, on='FD Run ID')

        # display the df
        st.write('CFU Plating Data')
        st.dataframe(rawcfu_df.head())
        st.write(f"DataFrame size: {len(rawcfu_df)}")
        
        st.write('Processed CFU Plating Data')
        st.dataframe(cleaned_cfu)
        st.write(f"DataFrame size: {len(cleaned_cfu)}")
        
        return rawcfu_df, cleaned_cfu
    
    
   
    
    
    #features engineering
