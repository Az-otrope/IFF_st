#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 00:28:31 2023

@author: miu
"""
import pandas as pd
import streamlit as st
import openpyxl
from openpyxl import Workbook
from pivot_in_pack import pivot_in_pack


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

def get_report(caption: str):
    """
    Let the user query the report as an Excel file
    
    INPUT: activate the button
    
    OUTPUT: return a report in .xlsx format
    """
    raw, clean = pivot_in_pack(data)
    st.download_button(
        label="Download report as CSV",
        data=csv,
        file_name='large_df.csv',
        mime='text/csv')
            
            
        
