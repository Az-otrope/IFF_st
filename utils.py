#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 00:28:31 2023

@author: miu
"""
import pandas as pd
import numpy as np
import streamlit as st
import time


def upload_dataset() -> pd.DataFrame:
    """
    Let the user upload a dataset as CSV
    
    INPUT: a .csv file 
    
    OUTPUT: return dataframe with relevant input and calculated information
    """
    
    file = st.file_uploader("Upload .csv file", type=["csv"])
    if not file:
        st.warning("Please upload a CSV file.")
        return pd.DataFrame()
        
    data = pd.read_csv(file)
    file.close()

    return data


def progress_bar():
    """
    Display the progress bar of work in progress
    """
    progress_bar = st.progress(0)
    
    for percent_complete in range(100):
        time.sleep(0.05)
        progress_bar.progress(percent_complete+1)
    
    st.write("File uploaded successfully")
    

# =============================================================================
# def convert_time_features(i):
#     """
#     The convert_time_features function standardizes time inputs, keeps text inputs, and passes None inputs
#     """
#     if i == '':
#         return None
#     try:
#         return pd.to_datetime(i, infer_datetime_format=True, format="%m/%d/%y")
#     except ValueError:
#         return i
# =============================================================================
    
    
def remove_spaces(df):
    """
    This function removes the spaces before and after a string. 
    The function will pass columns with timestamp and numerical datatypes
    """
    
    for col in df:
        if df[col].dtype == np.dtype('object'):
            
            df[col] = df[col].apply(lambda x:x.strip() if type(x) == "str" else x)
    return df