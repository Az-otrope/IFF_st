#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 00:26:40 2023

@author: miu
"""
import streamlit as st
import pandas as pd
import numpy as np

from utils import upload_dataset, progress_bar, remove_spaces


def cast_df_columns(df):
    """
    The cast_df_columns function takes a dataframe as input and returns the same dataframe with
    the columns that are categorical variables cast to pandas.Categorical dtype. The function also adds
    categories to each column that were not present in the original dataset, but are present in other datasets.

    :param df: Pass in the dataframe to be modified
    :return: The dataframe with the columns casted as categories
    """
    
    mapping_category_to_col = {
        'Storage form':['Pellet', 'Unbulked powder', 'Bulked powder, pre-dried bulking', 
                        'Bulked powder, w/o SiO2', 'Bulked powder, pre-dried bulking w/o SiO2', 'Bulked powder'],
        'Container': ['Mylar'],
        'Bulking': ['PVT', 'SKP', 'Tryptone'],
        'Desiccant': ['2%CaCl2', '5%SIO2', '10%CaCl2', '10%SIO2', '25%SIO2',
                      '5%TMC', '25%TMC', '10%TMC', '5%TMC+2%CaCl2']
    }
        
    for col, categories in mapping_category_to_col.items():
        if col in df.columns:
            df[col] = df[col].astype("category").cat.add_categories(categories)

    return df


def pivot_in_pack_app():
    st.title('Pivot In-pack Data Dashboard')
    
    st.subheader('New In-pack Sample Information Data Entry')
    
    with st.expander('Instruction for entering new sample information'):
        st.write('''
                 * Add rows: scroll to the bottom-most row and click on the “+” sign in any cell
                 * Delete rows: select one or more rows and press the `delete` key on your keyboard
                 ''')
    

    empty_df = pd.DataFrame(
        {
            'FD sample ID':[''],
            'FD Run ID':[''], 
            'Storage form':[''],
            'Container':[''],
            'Temperature (C)':[np.nan],
            'Bulking':[''],
            'Desiccant':['']
            }
        )
    
    if 'empty_df' not in st.session_state:
        st.session_state['empty_df'] = cast_df_columns(empty_df.copy())
        
    with st.form('my_form'):
        input_df = st.experimental_data_editor(st.session_state['empty_df'], num_rows='dynamic')
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.subheader('New In-pack Samples')
            
            df_v0 = st.session_state['empty_df']
            
            df_v1 = df_v0.append(input_df, ignore_index=True)
            df_v1 = df_v1.drop_duplicates(subset=['FD sample ID', 'FD Run ID', 'Storage form', 'Container'], keep='last', ignore_index=True)
            df_v1 = remove_spaces(df_v1)
            
            st.write(df_v1)
            st.session_state.empty_df = df_v1
            st.write(input_df.shape)
    
    
    st.subheader('Experimental CFU Plating Data')
    
    df = upload_dataset()    
    if len(df) > 0:
        progress_bar()
        
        df_v0, df_v1 = pivot_in_pack(df)
        st.session_state['pivot_df'] = df_v1.to_dict("records")
        if len(df_v1) > 0:
            st.subheader('Raw CFU Plating Data')
            df_v0 = st.experimental_data_editor(df_v0, num_rows="dynamic")
            st.write(df_v0.shape)

            st.subheader('Processed CFU Plating Data')
            # Join with input_df HERE
            
            df_v1 = st.experimental_data_editor(df_v1, num_rows="dynamic")
            st.write(df_v1.shape)
            st.download_button(
                label="Download Processed CFU Plating Data as CSV",
                data=df_v1.to_csv(),
                file_name='cfu_processed.csv',
                mime='text/csv'
            )

        exp_period = st.slider(
            'Choose a time range of completed experiments:',
            df_v1['T0'].min().date(),
            df_v1['Date'].max().date(),
            value=(df_v1['T0'].min().date(), df_v1['Date'].max().date()),
            format='YYYY/MM/DD'
        )
        df_v1_show = df_v1[(df_v1['T0'] >= pd.Timestamp(exp_period[0])) & (df_v1['Date'] <= pd.Timestamp(exp_period[1]))]
        st.dataframe(df_v1_show)
        st.write(df_v1_show.shape)


def feature_eng(df):
    """
    The feature_eng function creates 2 new timedelta features in days and weeks. 
    """
    
    df[['T0', 'Date']] = df[['T0', 'Date']].apply(pd.to_datetime, format="%m/%d/%y")
    df['Time point (day)'] = (df['Date'] - df['T0']).apply(lambda x: x.days)
    
    def num_weeks(row):
        year1, week1, day1 = row['T0'].isocalendar()
        year2, week2, day2 = row['Date'].isocalendar()
        return (year2 - year1) * 52 + (week2 - week1)
    df['Time point (week)'] = df.apply(num_weeks, axis=1)

    return df


def data_cleaning(df):
    df.columns = df.iloc[1]
    df = df.iloc[2:].reset_index()
    df.dropna(subset=['Batch'], inplace=True)
    df.drop(df[df['Remark/AW'] == 'Redo'].index, inplace=True)
    df = df[
        ['Batch','Sample Description','Storage form','Temperature-Celsius',
         'T0','Date','CFU/mL','CFU/g','CV','Water Activity'
        ]
    ]
    
    df = remove_spaces(df)
    
    for idx, row in df.iterrows():
        try:
            df.loc[idx, "CV"] = float(row['CV'].split("%")[0])
        except Exception as e:
            pass

    for col in ['CFU/mL', 'CFU/g', 'CV', 'Water Activity']:
        df[col] = df[col].replace('#DIV/0!', np.NaN)
        df[col] = df[col].astype(float)

    df = df.rename(columns={'Batch': 'FD Run ID', 'CV': 'CV (%)'})

    return df


def pivot_in_pack(df):
    df = data_cleaning(df)
    raw_cfu = feature_eng(df)

    pivot_rawcfu = df.pivot(index='FD Run ID', columns='Time point (week)', values=['CFU/mL', 'CFU/g', 'Water Activity'])
    pivot_rawcfu.columns = [f"W{week}_{scale}" for scale, week in pivot_rawcfu.columns.to_list()]
    
    # remove cols that cause duplicated samples
    cfu = df.drop(['Sample Description','Storage form','Temperature-Celsius',
                   'CFU/mL','CFU/g','CV (%)','Water Activity','Time point (day)','Time point (week)'], axis=1)
    cfu = cfu.drop_duplicates(subset='FD Run ID').reset_index(drop=True)
    
    # join the pivot df with the original info
    clean_cfu = pd.merge(cfu, pivot_rawcfu, on='FD Run ID')

    return raw_cfu, clean_cfu
