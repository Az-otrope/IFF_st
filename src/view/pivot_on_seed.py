import streamlit as st
import pandas as pd
import numpy as np

from src.utils.streamlit_utils import upload_dataset, progress_bar, remove_spaces, delta_time_cal


def cast_df_columns(df):
    """
    The cast_df_columns function takes a dataframe as input and returns the same dataframe with
    the columns that are categorical variables cast to pandas.Categorical dtype. The function also adds
    categories to each column that were not present in the original dataset, but are present in other datasets.

    :param df: Pass in the dataframe to be modified
    :return: The dataframe with the columns cast as categories
    """
    mapping_category_to_col = {"Age": ["Yes", "No"], "Aged_Temp": ["4", "21"]}

    for col, categories in mapping_category_to_col.items():
        if col in df.columns:
            df[col] = df[col].astype("category").cat.add_categories(categories)

    return df


# An empty df to take in user's inputs
empty_df = pd.DataFrame(
    {
        "FD sample ID": [""],
        "FD Run ID": [""],
        "Aged": [""],
        "Aged_Temp": [""],
        "Aged_Week": [""],
    }
)


# ================================== DASHBOARD ==============================================
def pivot_on_seed_app():
    st.title("Pivot On-seed Data Dashboard")

    st.subheader("New On-seed Sample Information Data Entry")

    with st.expander("Instruction for entering new sample information"):
        st.write(
            """
                     Each entry requires both **FD sample ID and FD Run ID** to be valid.

                     * Add rows: scroll to the bottom-most row and click on the “+” sign in any cell
                     * Delete rows: select one or multiple rows, then press the `delete` key on your keyboard
                     """
        )

    if "empty_os_input" not in st.session_state:
        st.session_state["empty_os_input"] = cast_df_columns(empty_df.copy())
    if "os_input" not in st.session_state:
        st.session_state["os_input"] = pd.DataFrame()

    with st.form("my_form"):
        # User enters new entries
        input_df = st.experimental_data_editor(st.session_state["empty_os_input"], num_rows="dynamic")

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.subheader("New In-pack Samples")

            os_info = remove_spaces(input_df)

            # TODO: the first entry with only 1 input FD sample ID or FD Run ID is still captured?
            os_info = pd.concat([st.session_state.os_input, os_info], ignore_index=True)
            os_info.dropna(subset=["FD sample ID", "FD Run ID"], how="any", inplace=True)
            os_info = os_info.drop_duplicates(subset=["FD sample ID", "FD Run ID"], keep="last", ignore_index=True)

            st.write(os_info)
            st.session_state.ip_input = os_info  # to database
            st.write(os_info.shape)

    st.subheader("On-seed CFU Plating Data")

    df = upload_dataset()
    # st.write(st.session_state)
    if len(df) > 0:
        progress_bar()

        df_v0, df_v1 = pivot_on_seed(df)
        # st.session_state['pivot_df'] = df_v1.to_dict("records")
        if len(df_v1) > 0:
            st.subheader("Raw On-seed CFU Plating Data")
            df_v0 = st.experimental_data_editor(df_v0, num_rows="dynamic")
            st.write(df_v0.shape)

            st.subheader("Processed CFU Plating Data")
            df_v1 = st.experimental_data_editor(df_v1, num_rows="dynamic")
            st.write(df_v1.shape)
            st.download_button(
                label="Download Processed CFU Plating Data as CSV",
                data=df_v1.to_csv(),
                file_name="cfu_processed.csv",
                mime="text/csv",
            )

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


def data_cleaning(df):
    df.columns = df.iloc[1]
    df = df.iloc[2:].reset_index()
    df.dropna(subset=["Batch"], inplace=True)
    df.drop(df[df["Remark"] == "Redo"].index, inplace=True)
    df = df[
        [
            "Batch",
            "Sample Description",
            "Code No.",
            "T0",
            "Date",
            "CFU/mL",
            "SD CFU/mL",
            "Extender CFU/mL",
            "SD Extender CFU/mL",
            "CV",
            "Water Activity",
        ]
    ]
    for idx, row in df.iterrows():
        try:
            df.loc[idx, "CV"] = float(row["CV"].split("%")[0])
        except Exception as e:
            pass

    for col in ["CFU/mL", "SD CFU/mL", "Extender CFU/mL", "SD Extender CFU/mL", "CV", "Water Activity"]:
        df[col] = df[col].replace("#DIV/0!", np.NaN)
        df[col] = df[col].astype(float)

    df = df.rename(columns={"Batch": "FD Run ID", "CV": "CV (%)"})

    return df


def pivot_on_seed(df):
    df = data_cleaning(df)
    raw_cfu = delta_time_cal(df)

    pivot_rawcfu = df.pivot(index="FD Run ID", columns="Week", values=["CFU/mL", "Extender CFU/mL", "Water Activity"])
    pivot_rawcfu.columns = [f"W{week}_{scale}" for scale, week in pivot_rawcfu.columns.to_list()]

    # remove cols that cause duplicated samples
    cfu = df.drop(
        [
            "Sample Description",
            "Water Activity",
            "CFU/mL",
            "SD CFU/mL",
            "Extender CFU/mL",
            "SD Extender CFU/mL",
            "CV (%)",
            "Water Activity",
            "Day",
            "Week",
        ],
        axis=1,
    )
    cfu = cfu.drop_duplicates(subset="FD Run ID").reset_index(drop=True)

    # join the pivot df with the original info
    clean_cfu = pd.merge(cfu, pivot_rawcfu, on="FD Run ID")

    return raw_cfu, clean_cfu
