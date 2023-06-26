import streamlit as st
import pandas as pd
import numpy as np

from src.utils.streamlit_utils import upload_dataset, remove_spaces, convert_time_features
from src.infrastructure.data_management import DataManager


def cast_df_columns(df):
    """
    The cast_df_columns function takes a dataframe as input and returns the same dataframe with
    the columns that are categorical variables cast to pandas.Categorical dtype. The function also adds
    categories to each column that were not present in the original dataset, but are present in other datasets.

    :param df: Pass in the dataframe to be modified
    :return: The dataframe with the columns cast as categories
    """

    mapping_category_to_col = {
        "Strain": ["Klebsiella variicola", "Kosakonia sacchari"],
        "Fermentation Scale": ["14L", "150K"],
        "Cryo mix": ["DSR", "PVT40%", "PVT70%", "SKP"],
        "Ingredient 1": ["40% Sucrose", "45.5% Sucrose"],
        "Ingredient 2": ["8% KH2PO4", "10% Maltodextrin", "22.75% Inulin"],
        "Ingredient 3": ["10.2% K2HPO4", "0.5% MgSO4"],
        "Dry in-house": ["TRUE", "FALSE"],
        "Container": ["Foil pouch", "Mylar bag"],
    }

    for col, categories in mapping_category_to_col.items():
        if col in df.columns:
            # This only works with new variables to add in, can't work if the values already exist
            df[col] = df[col].astype("category").cat.add_categories(categories)

            # Turn the current values into selectable
            # df[col] = df[col].astype("category")
    return df


# An empty df to take in user's inputs
empty_df = pd.DataFrame(
    {
        "FD sample ID": [""],
        "FD Run ID": [""],
        "Strain": [""],
        "EFT date": [None],
        "Broth ID": [""],
        "Fermentation Scale": [""],
        "Ferm condition": [""],
        "EFT (hr)": [np.nan],
        "Broth titer (CFU/mL)": [""],
        "Broth age (day)": [np.nan],
        "Pelletization date": [None],
        "Cryo mix": [""],
        "Ingredient 1": [""],
        "Ingredient 2": [""],
        "Ingredient 3": [""],
        "Cryo mix addition rate": [np.nan],
        "FD start date": [None],
        "FD recipe": [""],
        "FD pressure (mTorr)": [""],
        "FD run time (hr)": [np.nan],
        "Primary ramp rate (C/min)": [np.nan],
        "PA receive date": [None],  # can take date, string, or None
        "Dry in-house": [""],
        "Dried appearance": [""],
        "Container": [""],
        "Bulk density (g/mL)": [""],
        "Water activity": [""],
        "Viability (CFU/g)": [""],
    }
)


# ================================== DASHBOARD ==============================================
def sample_info_app():
    st.title("WP4 FD Sample Information")
    st.subheader("New Sample Information Data Entry")

    st.info("Developer use for testing - Upload historical data")
    if "df" not in st.session_state:
        # df = upload_dataset()
        df = DataManager().fetch_data("sample_info", "*")
        st.session_state.df = df
        st.write(df)
        # if st.button("Save?"):
        #     df_v0 = hist_data_cleaning(df)
        #     # df_v0 = feature_eng(df_v0)
        #     df_v0 = sample_info(df_v0)
        #     st.session_state.df = df_v0
        #     st.experimental_rerun()
        # else:
        #     st.stop()

    with st.expander("**IMPORTANT**: Instruction for entering new sample information"):
        st.write(
            """
                 * Enter the date in `MM/DD/YY` format.
                 * Enter values in scientific notation (where applicable): 4.05E11 or 4.05E+11
                 * Dropdown features:
                     * Strain, Fermentation Scale, Cryo mix, Dry in-house
                     * Ingredient 1, Ingredient 2, Ingredient 3, Container

                 * Add rows: scroll to the bottom-most row and click on the “+” sign in any cell
                 * Delete rows: select one or multiple rows, then press the `delete` key on your keyboard
                 """
        )

    if "empty_df" not in st.session_state:
        st.session_state["empty_df"] = cast_df_columns(empty_df.copy())

    with st.form("my_form"):
        input_df = st.experimental_data_editor(st.session_state["empty_df"], num_rows="dynamic")

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.subheader("Sample Information Compilation")

            # Process the df
            df_v = sample_info(input_df)  # new entries
            df_v0 = st.session_state.df  # historical data

            # Join the new inputs to historical dataset
            df_v1 = pd.concat([df_v0, df_v], ignore_index=True)
            df_v1 = df_v1.drop_duplicates(
                subset=["FD sample ID", "FD Run ID", "Strain", "EFT date"], keep="last", ignore_index=True
            )
            df_v1.dropna(subset=["FD Run ID"], inplace=True)

            # =============================================================================
            #         gb = GridOptionsBuilder.from_dataframe(df_v1)
            #         gb.configure_pagination()
            #         gb.configure_side_bar()
            #         gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=True)
            #         gridOptions = gb.build()
            #
            #         AgGrid(df_v1, gridOptions=gridOptions, enable_enterprise_modules=True)
            # =============================================================================
            st.write(df_v1)
            # TODO: upload this df to database
            st.session_state.df = df_v1  # goes to database: a full sample_info df
            st.write(df_v1.shape)

    if len(st.session_state.df) > 0:
        st.download_button(
            label="Download Sample Info report as CSV",
            data=st.session_state.df.to_csv(),
            file_name="sample_info.csv",
            mime="text/csv",
        )


# =============================== END DASHBOARD ==============================================


def feature_eng(df):
    """
    This function formats datetime and numerical features in the desirable format;
    then creates a column "Cryo mix Coef" containing a coefficient associates to each cryo-mix type, and a column "FC"
    shortening the descriptions of "Ferm condition"

    INPUT: a dataframe with user inputs
    OUTPUT: a dataframe with features engineered for further analysis
    """
    # Time features
    time_feats = ["PA receive date", "FD start date", "EFT date", "Pelletization date"]

    for col in time_feats:
        df[col] = df[col].apply(convert_time_features)

    # Numerical features
    num_feat = [
        "EFT (hr)",
        "Broth titer (CFU/mL)",
        "Broth age (day)",
        "Cryo mix addition rate",
        "FD run time (hr)",
        "Primary ramp rate (C/min)",
        "Bulk density (g/mL)",
        "Viability (CFU/g)",
    ]

    for col in num_feat:
        try:
            df[col] = df[col].astype(float)
        except:
            pass

    # map the 'Ferm condition'
    ferm_cond_shortkey = {
        "Tryptone+Peptone": "T+P",
        "Tryptone only": "T only",
        "Glucose": "Glucose",
        "Glucose, no EPS, CR": "Glucose",
        "Peptone only, upconcentrated": "P only, con",
        "Potato peptone and tryptone, high viscosity by post-ferm addition of 0.7% XG": "T+P, 0.7% XG",
        "Peptone only": "P only",
        "Potato peptone and tryptone, low viscosity": "T+P",
        "Glucose, high EPS, CR": "Glucose",
        "tryptone only": "T only",
        "repeat of P080-22-Y007, tryptone + potato peptone": "T+P",
        "Tryptone + potato peptone, lower top feed rate, no EPS": "T+P",
        "tryptone + potato peptone, low top feed rate, no EPS, w 0.7% XG": "T+P, 0.7% XG",
        "repeat of P080-22-Y005, tryptone + potato peptone": "T+P",
        "Potato peptone only, less EPS, pH control": "P only",
        "Glucose, no EPS": "Glucose",
        "Glucose, high EPS, CR broth": "Glucose",
        "Greens": "Greens",
        "Glucose, high EPS": "Glucose",
    }
    df["FC"] = df["Ferm condition"].map(ferm_cond_shortkey)

    # Cryo coefficient
    cryo_coef = {"PVT70%": 0.285, "DSR": 0.342, "SKP": 0.380}
    df["Cryo mix Coef"] = df["Cryo mix"].map(cryo_coef)

    return df


def cal_yield(row):
    """
    Calculate the fermentation broth's yield
    """

    if row.isna().any():
        return np.nan
    else:
        return round((row["Viability (CFU/g)"] * row["Cryo mix Coef"] / row["Broth titer (CFU/mL)"]) * 100, 2)


def log_loss(x):
    """
    Calculate log10 loss of yield
    """

    if pd.isna(x):
        return np.nan
    else:
        return round(np.log10(x / 100), 2)


def sample_info(df):
    """
    The sample_info function takes in a dataframe containing user inputs, then formats the datetime, numerical and
    cateogrical features.
    This function performs calcualtion on the material's yield and log loss.
    It returns a dataframe with sample's information entered by the user and according calcualted values

    INPUT: a dataframe with user inputs
    OUTPUT: a dataframe with sample's information and broth's yield-loss
    """
    df = remove_spaces(df)
    df = feature_eng(df)

    to_cal = df[["Broth titer (CFU/mL)", "Viability (CFU/g)", "Cryo mix Coef"]]
    df["Yield (%)"] = to_cal.apply(cal_yield, axis=1)
    df["Log Loss"] = df["Yield (%)"].apply(log_loss)

    # re-arrange the columns order
    df = df[
        [
            "FD sample ID",
            "FD Run ID",
            "Strain",
            "EFT date",
            "Broth ID",
            "Fermentation Scale",
            "Ferm condition",
            "FC",
            "EFT (hr)",
            "Broth titer (CFU/mL)",
            "Broth age (day)",
            "Pelletization date",
            "Cryo mix",
            "Ingredient 1",
            "Ingredient 2",
            "Ingredient 3",
            "Cryo mix addition rate",
            "FD start date",
            "FD recipe",
            "FD pressure (mTorr)",
            "FD run time (hr)",
            "Primary ramp rate (C/min)",
            "PA receive date",
            "Dry in-house",
            "Dried appearance",
            "Container",
            "Bulk density (g/mL)",
            "Water activity",
            "Viability (CFU/g)",
            "Cryo mix Coef",
            "Yield (%)",
            "Log Loss",
        ]
    ]

    return df
