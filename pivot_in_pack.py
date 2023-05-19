#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 00:26:40 2023

@author: miu
"""
import streamlit as st
import pandas as pd
import numpy as np

from utils import upload_dataset, progress_bar


def pivot_in_pack_app():
    st.title('Pivot In-pack Data Dashboard')
    
    st.subheader('New Sample Information Data Entry')
    
    with st.expander('Instruction for entering new sample information'):
        st.write('''
                 * Add rows: scroll to the bottom-most row and click on the “+” sign in any cell
                 * Delete rows: select one or more rows and press the `delete` key on your keyboard
                 ''')
    
    empty_df = pd.DataFrame(
        {
            'FD Run ID':pd.Series(dtype='str'), 
            'Storage form':pd.Series(dtype='str'), 
            'Temperature (C)':pd.Series(dtype='int'), 
            'Desiccant':pd.Series(dtype='str')
            }
        )
    
    input_df = st.experimental_data_editor(empty_df, num_rows='dynamic')
    
    if st.button('Submit'):
        pass
    
    
    st.subheader('Experimental Data')
    
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
    df = feature_eng(df)

    pivot_rawcfu = df.pivot(index='FD Run ID', columns='Time point (week)', values=['CFU/mL', 'CFU/g', 'Water Activity'])
    pivot_rawcfu.columns = [f"W{week}_{scale}" for scale, week in pivot_rawcfu.columns.to_list()]
    
    # remove cols that cause duplicated samples
    cfu = df.drop(['Sample Description','Storage form','Temperature-Celsius',
                   'CFU/mL','CFU/g','CV (%)','Water Activity','Time point (day)','Time point (week)'], axis=1)
    cfu = cfu.drop_duplicates(subset='FD Run ID').reset_index(drop=True)
    
    # join the pivot df with the original info
    cleaned_cfu = pd.merge(cfu, pivot_rawcfu, on='FD Run ID')

    return df, cleaned_cfu
