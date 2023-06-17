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
        progress_bar.progress(percent_complete + 1)

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

def time_feature_eng(df):
    """
    The feature_eng function creates 2 new timedelta features in days and weeks.
    """

    df[['T0', 'Date']] = df[['T0', 'Date']].apply(pd.to_datetime, format="%m/%d/%y")
    df['Day'] = (df['Date'] - df['T0']).apply(lambda x: x.days)

    def num_weeks(row):
        year1, week1, day1 = row['T0'].isocalendar()
        year2, week2, day2 = row['Date'].isocalendar()
        return (year2 - year1) * 52 + (week2 - week1)

    df['Week'] = df.apply(num_weeks, axis=1)

    return df


def remove_spaces(df):
    """
    This function removes the spaces before and after a string. 
    The function will skip columns with timestamp, numerical datatype and NaN
    """

    for col in df:
        if df[col].dtype == np.dtype('object'):
            df[col] = df[col].apply(lambda x: x.strip() if type(x) == "str" else x)
    return df
