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


def pivot_in_pack(df):
    
    df.columns = df.iloc[1]
    df = df.iloc[2:]
    df = df.reset_index()
    # remove rows with NaN in 'Batch" col
    df.dropna(subset=['Batch'],inplace=True)
    # keep relevant cols
    df = df[['Batch','Sample Description','Storage form','Temperature-Celsius',
                           'T0','Date','CFU/mL','CFU/g','CV','Water Activity']]
    
    # convert to datetime for T0 and Date
    df[['T0','Date']] = df[['T0','Date']].apply(pd.to_datetime, format="%m/%d/%y")
    
    # time point by days and weeks of plating
    ## by days
    df['Time point (day)'] = (df['Date']-df['T0']).apply(lambda x: x.days)
    ## by weeks
    to_week = df[['T0','Date']]
    for i in to_week.columns:
        to_week[i] = to_week[i].apply(lambda x:x.week)
    df['Time point (week)'] = to_week['Date'] - to_week['T0']    
    
    # remove % sign for CV values while ignoring invalid values
    for idx, row in df.iterrows():
        try:
            df.loc[idx, "CV"] = float(row['CV'].split("%")[0])
        except Exception as e:
            pass
    
    # handle invalid values and change to float
    to_float = df[['CFU/mL','CFU/g','CV','Water Activity']]
    for col in to_float.columns:
        df[col] = df[col].replace('#DIV/0!', np.NaN)
        df[col] = df[col].astype(float)      
        
    # change col names
    df.rename(columns={'Batch':'FD Run ID', 'Temperature-Celsius':'Temperature (C)', 'CV':'CV (%)'}, inplace=True)
    
    # Record the CFUs by week for each ID
    pivot_rawcfu = df.pivot(index='FD Run ID', columns='Time point (week)', values=['CFU/mL','CFU/g'])
    # rename the cols by the counting week
    pivot_rawcfu.columns = [f"W{week}_{scale}" for scale, week in pivot_rawcfu.columns.to_list()]
    
    # remove cols that cause duplicated samples
    cfu = df.drop(['T0','Date','CFU/mL','CFU/g','CV (%)','Time point (day)','Time point (week)'],axis=1)
    # drop duplicated IDs
    cfu.drop_duplicates(subset='FD Run ID', inplace=True)
    
    # join the pivot df with the original info
    cleaned_cfu = pd.merge(cfu, pivot_rawcfu, on='FD Run ID')
    
    # to keep: df - original data with minimal cleaning
    # to keep: cleaned_cfu - processed data for further analysis
    return df, cleaned_cfu
    
    
   
    
    
    #features engineering
