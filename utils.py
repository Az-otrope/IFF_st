#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 00:28:31 2023

@author: miu
"""
import pandas as pd
import streamlit as st


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
    st.write("File uploaded successfully")

    return data
            
            
        
