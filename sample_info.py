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
    #st.subheader('New Sample Information Data Entry')
    
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
    df = upload_dataset()
    # st.write(st.session_state)
    if len(df) > 0:
        #df_v = cast_df_columns(df)
        st.subheader('Current Sample Information Compilation')
        old_df = sample_info(df)
        df_v0 = st.experimental_data_editor(old_df, num_rows="dynamic")
        st.write(df_v0.shape)
    ##new_dataframe = pd.concat([old_dataframe, new_dataframe])
    #
    #return old_dataframe
    
def data_cleaning(df):
    df.columns = [column.strip() for column in df.columns]
    df.drop(['Storage tracking','Seed treatment','Ingredient4','Yield (%)','Log loss','Note'], axis=1, inplace=True)
    df.dropna(subset=['FD Run ID'], inplace=True)
    
    time_feat = ['EFT date','Pelletization date','FD start date','PA receive date']
    for col in time_feat:
        df[col] = pd.to_datetime(df[col],infer_datetime_format=True,format="%m/%d/%y",errors='coerce')
    df['PA receive date'] = df['PA receive date'].replace({np.nan: 'Dry in PA'})
    
    df['FD run time (hr)'] = df['FD run time (hr)'].apply(lambda x:float(x.split()[0]))
    
    df['Viability (CFU/g)'] = df['Viability (CFU/g)'].replace(['#DIV/0!','n/m'], np.NaN)
    df['Viability (CFU/g)'] = df['Viability (CFU/g)'].astype(float)
    
    return df


def feature_eng(df):
    cryo_coef = {'PVT70%': 0.285, 'DSR': 0.342, 'SKP': 0.380}
    
    df['Cryo mix Coef'] = df['Cryo mix'].map(cryo_coef)
    
    return df


def cal_yield(row):
    if row.isna().any():
        return np.nan
    else:
        return round((row['Viability (CFU/g)']*row['Cryo mix Coef']/row['Broth titer (CFU/mL)'])*100,2)

    
def log_loss(x):
    if pd.isna(x):
        return np.nan
    else:
        return round(np.log10(x/100),2)

    
def sample_info(df):
    df = data_cleaning(df)
    df = feature_eng(df)
    
    to_cal = df[['Broth titer (CFU/mL)','Viability (CFU/g)','Cryo mix Coef']]
    df['Yield (%)'] = to_cal.apply(cal_yield, axis=1)
    df['Log Loss'] = df['Yield (%)'].apply(log_loss)
    
    return df 
