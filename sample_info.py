import streamlit as st
import pandas as pd
import numpy as np

from utils import upload_dataset


def cast_df_columns(df):
    """
    The cast_df_columns function takes a dataframe as input and returns the same dataframe with
    the columns that are categorical variables cast to pandas.Categorical dtype. The function also adds
    categories to each column that were not present in the original dataset, but are present in other datasets.

    :param df: Pass in the dataframe to be modified
    :return: The dataframe with the columns casted as categories
    """
    mapping_category_to_col = {
        "Strain": ['Klebsiella variicola', 'Kosakonia sacchari'],
        'Fermentation Scale': ['14L', '150K'],
        'Ingredient 1': ['40% Sucrose', '45.5% Sucrose'],
        'Ingredient 2': ['8% KH2PO4', '10% Maltodextrin', '22.75% Inulin'],
        'Ingredient 3': ['10.2% K2HPO4', '0.5% MgSO4'],
        'Ingredient 4': [],
        'Container': ['Foil pouch']
    }
    for col, categories in mapping_category_to_col.items():
        if col in df.columns:
            df[col] = df[col].astype("category").cat.add_categories(categories)

    return df

def sample_info_app():
    st.title('WP4 FD Sample Information ')
    st.subheader('Data Entry for New Sample')
    
    #dict_form = {
    #    "Strain": ['Klebsiella variicola', 'Kosakonia sacchari'],
    #    'Fermentation Scale': ['14L', '150K'],
    #    'Ingredient 1': ['40% Sucrose', '45.5% Sucrose'],
    #    'Ingredient 2': ['8% KH2PO4', '10% Maltodextrin'],
    #    'Ingredient 3': ['10.2% K2HPO4', '0.5% MgSO4'],
    #    'Ingredient 4': ['a','b'],
    #    'Container': ['Foil pouch', 'Mylar']
    #}
#
    #df = pd.DataFrame(dict_form)
    #old_dataframe = st.experimental_data_editor(df, num_rows="dynamic")
    ##new_dataframe = pd.concat([old_dataframe, new_dataframe])
    #
    #return old_dataframe