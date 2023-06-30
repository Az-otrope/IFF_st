import pandas as pd
import numpy as np
import streamlit as st
import time
import openpyxl
import statsmodels.api as sm


def upload_dataset() -> pd.DataFrame:
    file = st.file_uploader("Upload a CSV file", type=["csv"])
    if not file:
        st.warning("Please upload a file.")
        return pd.DataFrame()

    data = pd.read_csv(file)
    file.close()

    return data


# def upload_dataset() -> pd.DataFrame:
#     file = st.file_uploader("Upload file", type=["csv"])
#     if not file:
#         st.warning("Please upload a file.")
#         return pd.DataFrame()
#
#     # data = pd.read_csv(file)
#     data = pd.concat(pd.read_excel(file[0], sheet_name=None), ignore_index=True)
#     file[0].close()
#
#     return data


def progress_bar():
    progress_bar = st.progress(0)

    for percent_complete in range(100):
        time.sleep(0.05)
        progress_bar.progress(percent_complete + 1)

    st.write("File uploaded successfully")


def cfu_data_cleaning(df):
    """
    This function takes in a CSV file, removes empty and invalid entries
    """
    df.columns = df.iloc[1]
    df = df.iloc[2:]
    df = df.reset_index(drop=True)  # drop the original index

    # remove rows with NaN in 'Batch' col
    df.dropna(subset=["Batch"], inplace=True)

    # remove rows with 'Redo' in 'Redo' col
    try:
        df = df[~(df["Redo"] == "Y")]
    except Exception as e:
        pass

    # keep necessary features
    df = df[
        [
            "Batch",
            "Sample Description",
            "On-seed Description",
            "Date",
            "T0 (date)",
            "CFU/mL",
            "CFU/g",
            "CV",
            "Water Activity",
        ]
    ]

    df = remove_spaces(df)

    # remove percentage sign for CV values while ignoring invalid values
    for idx, row in df.iterrows():
        try:
            df.loc[idx, "CV"] = float(row["CV"].split("%")[0])
        except Exception as e:
            pass

    # handle invalid values and change to float
    to_float = df[["CFU/mL", "CFU/g", "CV", "Water Activity"]]
    for col in to_float.columns:
        df[col] = df[col].replace(["#DIV/0!", "#VALUE!", "#REF!"], np.NaN)
        df[col] = df[col].astype(float)

    # change col names
    df.rename(columns={"Batch": "FD Run ID", "T0 (date)": "T0", "CV": "CV (%)"}, inplace=True)

    return df


def convert_time_features(i):
    """
    The convert_time_features function standardizes time inputs, keeps text inputs, and passes None inputs
    """
    if i == "":
        return None
    try:
        return pd.to_datetime(i, infer_datetime_format=True, format="%m/%d/%y")
    except ValueError:
        return i


def delta_time_cal(df):
    df[["T0", "Date"]] = df[["T0", "Date"]].apply(pd.to_datetime, format="%m/%d/%y")
    df["Day"] = (df["Date"] - df["T0"]).apply(lambda x: x.days)

    def num_weeks(row):
        year1, week1, day1 = row["T0"].isocalendar()
        year2, week2, day2 = row["Date"].isocalendar()
        return (year2 - year1) * 52 + (week2 - week1)

    df["Week"] = df.apply(num_weeks, axis=1)

    return df


def remove_spaces(df):
    for col in df:
        if df[col].dtype == np.dtype("object"):
            df[col] = df[col].apply(lambda x: x.strip() if type(x) == "str" else x)
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
    # df["LogCFU"] = np.log10(df["CFU/g"])

    # No calculation if there are only 1 or 2 observant (day-LogCFU)
    if len(df) < 3:
        decay_df = pd.Series({"Decay Rate": None, "R-squared": None, "CI95_lower": None, "CI95_upper": None})
        return decay_df

    # Extract the input feature and target variable
    x = df[["Day", "const"]]  # require to be float/int
    y = df["LogCFU"]

    # Fit the linear regression model
    model = sm.OLS(y, x)
    results = model.fit()

    # Extract the coefficient and R-squared
    slope = results.params[1]
    r_squared = results.rsquared

    # Extract the 95% confidence interval
    ci = results.conf_int(alpha=0.05)
    ci_slope = ci.loc["Day"]

    decay_df = pd.Series(
        {"Decay Rate": slope, "R-squared": r_squared, "CI95_lower": ci_slope[0], "CI95_upper": ci_slope[1]}
    )

    return decay_df
