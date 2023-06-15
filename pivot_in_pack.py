#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 00:26:40 2023

@author: miu
"""
import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm

from utils import upload_dataset, progress_bar, remove_spaces
# TODO: how to import the info_merge df from sample_info?
#import sample_info

#info_df = sample_info.info_merge

def cast_df_columns(df):
    """
    The cast_df_columns function takes a dataframe as input and returns the same dataframe with
    the columns that are categorical variables cast to pandas.Categorical dtype. The function also adds
    categories to each column that were not present in the original dataset, but are present in other datasets.

    :param df: Pass in the dataframe to be modified
    :return: The dataframe with the columns casted as categories
    """
    
    mapping_category_to_col = {
        'Storage form': ['Pellet', 'Unbulked powder', 'Bulked powder, pre-dried bulking', 'Bulked powder, w/o SiO2',
                         'Bulked powder, pre-dried bulking w/o SiO2', 'Bulked powder'],
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
                 Each entry requires both **FD sample ID and FD Run ID** to be valid. 
                 * Numerical feaure: Temperature (4, 21, 37, etc)
                 * Dropdown features: 
                     * Storage form, Container, Bulking, Desiccant
                     
                 * Add rows: scroll to the bottom-most row and click on the “+” sign in any cell
                 * Delete rows: select one or more rows and press the `delete` key on your keyboard
                 ''')
    

    empty_df = pd.DataFrame(
        {
            'FD sample ID': [''],
            'FD Run ID': [''],
            'Storage form': [''],
            'Container': [''],
            'Temperature (C)': [np.nan],
            'Bulking': [''],
            'Desiccant': ['']
            }
        )
    
    if 'df' not in st.session_state:
        st.session_state['df'] = cast_df_columns(empty_df.copy())
        #st.session_state['df'] = cast_df_columns(empty_df)

    with st.form('my_form'):
        input_df = st.experimental_data_editor(st.session_state['df'], num_rows='dynamic')
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.subheader('New In-pack Samples')
            
            df_v = st.session_state['df']
            df_v0 = remove_spaces(input_df)

            user_input_df = pd.concat([df_v, df_v0], ignore_index=True)
            user_input_df = user_input_df.drop_duplicates(subset=['FD sample ID', 'FD Run ID', 'Storage form', 'Container'], keep='last', ignore_index=True)
            user_input_df.dropna(subset=['FD sample ID', 'FD Run ID'], inplace=True, ignore_index=True)

            st.write(user_input_df)
            st.session_state.df = user_input_df
            st.write(user_input_df.shape)


    st.subheader('Experimental CFU Plating Data')
    
    df = upload_dataset()    
    if len(df) > 0:
        progress_bar()
        
        df_v0, df_v1 = pivot_in_pack(df) # raw, decay_df
        st.session_state['pivot_df'] = df_v1.to_dict("records")
        if len(df_v1) > 0:
            st.subheader('Raw CFU Plating Data')
            df_v0 = st.experimental_data_editor(df_v0, num_rows="dynamic")
            st.write(df_v0.shape)

            st.subheader('Processed CFU Plating Data')

            # TODO: Join with input_df HERE
            # temp1 = pd.merge(left=real_input_df, right=decay_df.drop(['T0', 'Date'], axis=1),
            #                  on='FD Run ID', how='left')
            #
            # temp2 = pd.merge(left=temp1, right=info_df, on=['FD sample ID'], how='left')
            #
            # final_df = pd.merge(temp2, info_df, on='FD sample ID')

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


def data_cleaning(df):
    df.columns = df.iloc[1]
    df = df.iloc[2:].reset_index()
    df.dropna(subset=['Batch'], inplace=True)
    df.drop(df[df['Remark/AW'] == 'Redo'].index, inplace=True)
    df = df[
        ['Batch', 'Sample Description', 'Storage form', 'Temperature-Celsius',
         'T0', 'Date', 'CFU/mL', 'CFU/g', 'CV', 'Water Activity']
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


def feature_eng(df):
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


def decay_rate(df):
    """
    The decay_rate function calculates the rate at which the material's concentration (in Log10_CFU) decay over time.
    The function takes in time (day) as the independent variable (X) and Log10(CFU) as the dependent variable (y).
    A linear regression model calculates the slope, r-squared, and the 95% confidence interval (CI) of the slope.
    The model will skip entries having fewer than 2 datapoints due to avoid overfitting and bias.

    INPUT: a dataframe containing raw plating CFU data (wide format)
        - X (independent variable): time (day) - int64 or float64
        - y (dependent variable): Log10(CFU) - float64

    OUTPUT: a dataframe containing the samples information, the CFU values at each timepoint, the decay rate over time,
        the R-squared of the linear fit equation, the lower and upper values of the 95% CI of the decay rate.
        - decay_rate: slope of the linear fit equation (m)
        - r-squared: coefficient of determination
        - ci_slope: [lower,upper] values of the slope's 95% CI
    """
    df['LogCFU'] = np.log10(df['CFU/g'])

    # No calculation if there are only 1 or 2 observant (day-LogCFU)
    if len(df) < 3:
        decay_df = pd.Series({'Decay Rate': None, 'R-squared': None,
                              'CI95_lower': None, 'CI95_upper': None})
        return decay_df

    # Extract the input feature and target variable
    X = df[['Day', "const"]]  # require to be float/int
    y = df['LogCFU']

    # Fit the linear regression model
    model = sm.OLS(y, X)
    results = model.fit()

    # Extract the coefficient and R-squared
    decay_rate = results.params[1]
    r_squared = results.rsquared

    # Extract the 95% confidence interval
    ci = results.conf_int(alpha=0.05)
    ci_slope = ci.loc['Day']

    decay_df = pd.Series({'Decay Rate': decay_rate, 'R-squared': r_squared,
                          'CI95_lower': ci_slope[0], 'CI95_upper': ci_slope[1]})

    return decay_df


def pivot_in_pack(df):
    # clean and organize experimental cfu plating file
    df = data_cleaning(df)
    raw_cfu = feature_eng(df)

    # create pivot df to arrange CFU values into wide format
    pivot_rawcfu = df.pivot(index='FD Run ID', columns='Week', values=['CFU/mL', 'CFU/g', 'Water Activity'])
    pivot_rawcfu.columns = [f"W{week}_{scale}" for scale, week in pivot_rawcfu.columns.to_list()]
    
    # remove cols that cause duplicated samples
    cfu = df.drop(['Sample Description', 'Storage form', 'Temperature-Celsius',
                   'CFU/mL', 'CFU/g', 'CV (%)', 'Water Activity', 'Day', 'Week'], axis=1)
    cfu = cfu.drop_duplicates(subset='FD Run ID').reset_index(drop=True)
    
    # join the pivot df with the original info -> wide format df
    clean_cfu = pd.merge(cfu, pivot_rawcfu, on='FD Run ID')

    # calculate the decay rate, r-squared and 95% CI
    raw = raw_cfu.copy()
    raw = sm.add_constant(raw)

    decay = raw.groupby('FD Run ID').apply(decay_rate).reset_index()
    decay_df = pd.merge(left=clean_cfu, right=decay, on='FD Run ID')

    decay_df = decay_df.drop_duplicates()

    return raw_cfu, decay_df

# TODO: join the 3 dataframes: info_merge, user_input_df and decay_df