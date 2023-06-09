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

from src.utils.streamlit_utils import (
    upload_dataset,
    progress_bar,
    cfu_data_cleaning,
    remove_spaces,
    delta_time_cal,
    decay_rate,
)


# TODO: how to import the info_merge df from sample_info?
# st.write(st.session_state.info_merge)


def cast_df_columns(df):
    """
    The cast_df_columns function takes a dataframe as input and returns the same dataframe with
    the columns that are categorical variables cast to pandas.Categorical dtype. The function also adds
    categories to each column that were not present in the original dataset, but are present in other datasets.

    :param df: Pass in the dataframe to be modified
    :return: The dataframe with the columns cast as categories
    """

    mapping_category_to_col = {
        "Storage form": [
            "Pellet",
            "Unbulked powder",
            "Bulked powder, pre-dried bulking",
            "Bulked powder, w/o SiO2",
            "Bulked powder, pre-dried bulking w/o SiO2",
            "Bulked powder",
        ],
        "Container": ["Mylar"],
        "Bulking": ["PVT", "SKP", "Tryptone"],
        "Desiccant": [
            "2%CaCl2",
            "5%SIO2",
            "10%CaCl2",
            "10%SIO2",
            "25%SIO2",
            "5%TMC",
            "25%TMC",
            "10%TMC",
            "5%TMC+2%CaCl2",
        ],
    }

    for col, categories in mapping_category_to_col.items():
        if col in df.columns:
            df[col] = df[col].astype("category").cat.add_categories(categories)

    return df


# An empty df to take in user's inputs
empty_df = pd.DataFrame(
    {
        "FD sample ID": [""],
        "FD Run ID": [""],
        "Storage form": [""],
        "Container": [""],
        "Temperature (C)": [np.nan],
        "Bulking": [""],
        "Desiccant": [""],
    }
)


# ================================== DASHBOARD ==============================================
def pivot_in_pack_app():
    st.title("Pivot In-pack Data Dashboard")

    st.subheader("New In-pack Sample Information Data Entry")

    with st.expander("Instruction for entering new sample information"):
        st.write(
            """
                 Each entry requires both **FD sample ID and FD Run ID** to be valid.
                 * Numerical feaure: Temperature (4, 21, 37, etc)
                 * Dropdown features:
                     * Storage form, Container, Bulking, Desiccant

                 * Add rows: scroll to the bottom-most row and click on the “+” sign in any cell
                 * Delete rows: select one or multiple rows, then press the `delete` key on your keyboard
                 """
        )

    if "empty_ip_input" not in st.session_state:
        st.session_state["empty_ip_input"] = cast_df_columns(empty_df.copy())
    if "ip_input" not in st.session_state:
        # st.session_state["ip_input"] = cast_df_columns(empty_df.copy())
        st.session_state["ip_input"] = pd.DataFrame()

    with st.form("my_form"):
        # the session_state.emtpy_input always provides the input_df with an empty frame to take new entries
        # if I use only session_state.ip_input, the input_df takes in the last session_state.ip_input
        # BUT NOT the new entries
        # Thus I need the session_state.empty_input to allow the input_df contains the new entries

        # User enters new entries
        input_df = st.experimental_data_editor(st.session_state["empty_ip_input"], num_rows="dynamic")

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.subheader("New In-pack Samples")

            ip_info = remove_spaces(input_df)

            # TODO: the first entry with only 1 input FD sample ID or FD Run ID is still captured?
            ip_info = pd.concat([st.session_state.ip_input, ip_info], ignore_index=True)
            ip_info.dropna(subset=["FD sample ID", "FD Run ID"], how="any", inplace=True)
            ip_info = ip_info.drop_duplicates(
                subset=["FD sample ID", "FD Run ID", "Storage form", "Container"], keep="last", ignore_index=True
            )

            st.write(ip_info)
            st.session_state.ip_input = ip_info  # to database
            st.write(ip_info.shape)

    st.subheader("In-pack CFU Plating Data")

    df = upload_dataset()
    if len(df) > 0:
        progress_bar()

        df_v0, df_v1 = pivot_in_pack(df)  # raw, decay_df
        # st.session_state['pivot_df'] = df_v1.to_dict("records")
        # if len(df_v1) > 0:
        st.subheader("Raw In-pack CFU Plating Data")
        df_v0 = st.experimental_data_editor(df_v0, num_rows="dynamic")
        st.write(df_v0.shape)

        st.subheader("Processed CFU Plating Data")

        # TODO: join the 3 dataframes: info_merge, user_input_df and decay_df
        # temp1 = pd.merge(left=st.session_state.ip_input, right=df_v1.drop(['T0', 'Date'], axis=1),
        #                  on='FD Run ID', how='left')
        #
        # select necessary cols from sample_info
        # sub_df = df[["FD sample ID", "Strain", "Ferm condition", "Cryo mix"]]
        # drop duplicates
        # sub_df = sub_df.drop_duplicates(
        #
        # temp2 = pd.merge(left=temp1, right=st.session_state.info_merge, on=['FD sample ID'], how='left')
        #
        # final_df = pd.merge(temp2, st.session_state.info_merge, on='FD sample ID')

        df_v1 = st.experimental_data_editor(df_v1, num_rows="dynamic")
        st.write(df_v1.shape)
        st.download_button(
            label="Download Processed CFU Plating Data as CSV",
            data=df_v1.to_csv(),
            file_name="cfu_processed.csv",
            mime="text/csv",
        )

        # final_df = st.experimental_data_editor(final_df, num_rows="dynamic")
        # st.write(final_df.shape)
        # st.download_button(
        #     label="Download Processed CFU Plating Data as CSV",
        #     data=final_df.to_csv(),
        #     file_name='cfu_processed.csv',
        #     mime='text/csv'
        # )

        exp_period = st.slider(
            "Choose a time range of completed experiments:",
            df_v1["T0"].min().date(),
            df_v1["Date"].max().date(),
            value=(df_v1["T0"].min().date(), df_v1["Date"].max().date()),
            format="YYYY/MM/DD",
        )

        df_v1_show = df_v1[
            (df_v1["T0"] >= pd.Timestamp(exp_period[0])) & (df_v1["Date"] <= pd.Timestamp(exp_period[1]))
        ]
        st.dataframe(df_v1_show)
        st.write(df_v1_show.shape)


# =============================== END DASHBOARD ==============================================


# def decay_rate(df):
#     """
#     The decay_rate function calculates the rate at which the material's concentration (in Log10_CFU) decay over time.
#     The function takes in time (day) as the independent variable (X) and Log10(CFU) as the dependent variable (y).
#     A linear regression model calculates the slope, r-squared, and the 95% confidence interval (CI) of the slope.
#     The model will skip entries having fewer than 2 datapoints due to avoid overfitting and bias.
#
#     INPUT: a dataframe containing raw plating CFU data (wide format)
#         - X (independent variable): time (day) - int64 or float64
#         - y (dependent variable): Log10(CFU) - float64
#
#     OUTPUT: a dataframe containing the samples information, the CFU values at each timepoint, the decay rate over time,
#         the R-squared of the linear fit equation, the lower and upper values of the 95% CI of the decay rate.
#         - decay_rate: slope of the linear fit equation (m)
#         - r-squared: coefficient of determination
#         - ci_slope: [lower,upper] values of the slope's 95% CI
#     """
#     df["LogCFU"] = np.log10(df["CFU/g"])
#
#     # No calculation if there are only 1 or 2 observant (day-LogCFU)
#     if len(df) < 3:
#         decay_df = pd.Series({"Decay Rate": None, "R-squared": None, "CI95_lower": None, "CI95_upper": None})
#         return decay_df
#
#     # Extract the input feature and target variable
#     x = df[["Day", "const"]]  # require to be float/int
#     y = df["LogCFU"]
#
#     # Fit the linear regression model
#     model = sm.OLS(y, x)
#     results = model.fit()
#
#     # Extract the coefficient and R-squared
#     slope = results.params[1]
#     r_squared = results.rsquared
#
#     # Extract the 95% confidence interval
#     ci = results.conf_int(alpha=0.05)
#     ci_slope = ci.loc["Day"]
#
#     decay_df = pd.Series(
#         {"Decay Rate": slope, "R-squared": r_squared, "CI95_lower": ci_slope[0], "CI95_upper": ci_slope[1]}
#     )
#
#     return decay_df


def pivot_in_pack(df):
    # clean and organize experimental cfu plating file
    df = cfu_data_cleaning(df)

    # select in-pack df
    onseed_chars = ["Ext", "treat", "bio", "Rep"]
    ip_df = df[~df["On-seed Description"].str.contains("|".join(onseed_chars), na=False)]
    ip_df = ip_df[["FD Run ID", "Date", "T0", "CFU/mL", "CFU/g", "CV (%)", "Water Activity"]]

    raw_ip = delta_time_cal(ip_df)

    # create pivot df to arrange CFU values into wide format
    pivot_ip = raw_ip.pivot(index="FD Run ID", columns="Week", values=["CFU/mL", "CFU/g", "Water Activity"])
    pivot_ip.columns = [f"W{week}_{scale}" for scale, week in pivot_ip.columns.to_list()]

    # remove cols that cause duplicated samples
    ip_cfu = raw_ip.drop(["CFU/mL", "CFU/g", "CV (%)", "Water Activity", "Day", "Week"], axis=1)
    ip_cfu.drop_duplicates(subset="FD Run ID", inplace=True)

    # join the pivot df with the original info -> wide format df
    wide_ip = pd.merge(ip_cfu, pivot_ip, on="FD Run ID")

    # calculate the decay rate, r-squared and 95% CI
    raw = raw_ip.copy()
    raw["LogCFU"] = np.log10(raw["CFU/g"])
    raw = sm.add_constant(raw)

    decay = raw.groupby("FD Run ID").apply(decay_rate).reset_index()
    decay_ip = pd.merge(left=wide_ip, right=decay, on="FD Run ID")

    decay_ip = decay_ip.drop_duplicates()

    return raw_ip, decay_ip
