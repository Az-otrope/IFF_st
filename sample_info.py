import streamlit as st

import pandas as pd
import numpy as np
from utils import upload_dataset


# Time features
time_feats = ['PA receive date', 'FD start date', 'EFT date','Pelletization date']


def data_cleaning(df):
    """
    The data_cleaning function cleans up the historical dataset resulting in the desired format. 
    This function removes untracked features, formats the date time and NaN values 
    
    INPUT: a dataframe containing historical data
    
    OUTPUT: a clean dataframe 
    """
    
    df.columns = [column.strip() for column in df.columns]
    try:
        df.drop(['Storage tracking','Seed treatment','Ingredient4','Yield (%)','Log loss','Note'], axis=1, inplace=True)
    except:
        pass
    
    
    df.dropna(subset=['FD Run ID'], inplace=True)
    df['FD run time (hr)'] = df['FD run time (hr)'].apply(lambda x:float(x.split()[0]))
    
    
    for col in time_feats:
        df[col] = pd.to_datetime(df[col],infer_datetime_format=True, format="%m/%d/%y",errors='coerce')
    # If the values were 'Dry in PA', the command above turns the str to NaT. Thus, have to revert the input
    df['PA receive date'] = df['PA receive date'].replace({np.nan: 'Dry in PA'})
    
    
    df['Viability (CFU/g)'] = df['Viability (CFU/g)'].replace(['#DIV/0!','n/m'], np.NaN)
    df['Viability (CFU/g)'] = df['Viability (CFU/g)'].astype(float)
    
    return df


def cast_df_columns(df):
    """
    The cast_df_columns function takes a dataframe as input and returns the same dataframe with
    the columns that are categorical variables cast to pandas.Categorical dtype. The function also adds
    categories to each column that were not present in the original dataset, but are present in other datasets.

    :param df: Pass in the dataframe to be modified
    :return: The dataframe with the columns casted as categories
    """
    
    mapping_category_to_col = {
        'Strain': ['Klebsiella variicola', 'Kosakonia sacchari'],
        'Fermentation Scale': ['14L', '150K'],
        'Cryo mix': ['DSR', 'PVT40%', 'PVT70%', 'SKP'],
        'Ingredient 1': ['40% Sucrose', '45.5% Sucrose'],
        'Ingredient 2': ['8% KH2PO4', '10% Maltodextrin', '22.75% Inulin'],
        'Ingredient 3': ['10.2% K2HPO4', '0.5% MgSO4'],
        'Container': ['Foil pouch','Mylar bag']
    }
        
    for col, categories in mapping_category_to_col.items():
        if col in df.columns:
            # This only works with new variables to add in, can't work if the values already exist 
            df[col] = df[col].astype("category").cat.add_categories(categories)

            ## Turn the current values into selectable 
            #df[col] = df[col].astype("category")

    return df


empty_df = pd.DataFrame(
        {
            'FD sample ID':[''],
            'FD Run ID':[''],
            'Strain':[''],
            'EFT date':[None],
            'Broth ID':[''],
            'Fermentation Scale':[''],
            'Ferm condition':[''],
            'EFT (hr)':[np.nan],
            'Broth titer (CFU/mL)':[np.nan],
            'Broth age (day)':[np.nan],
            'Pelletization date':[None],
            'Cryo mix':[''],
            'Ingredient 1':[''],
            'Ingredient 2':[''],
            'Ingredient 3':[''],
            'Cryo mix addition rate':[np.nan],
            'FD start date':[None],
            'FD cycle recipe':[''],
            'FD pressure (mTorr)':[''],
            'FD run time (hr)':[np.nan],
            'Primary ramp rate (C/min)':[np.nan],
            'PA receive date':[''], # case: Dry in PA
            'Dried appearance':[''],
            'Container':[''],
            'Water activity':[''],
            'Viability (CFU/g)':[np.nan]
            }
        )


def sample_info_app():
    st.title('WP4 FD Sample Information')
    st.subheader('New Sample Information Data Entry')
    
    st.info('Developer use for testing - Upload historical data')
    if "df" not in st.session_state:
        df = upload_dataset()
        if st.button("Save?"):
            # breakpoint()
            df_v0 = data_cleaning(df)
            df_v0 = feature_eng(df_v0)
            st.session_state.df = df_v0
            st.experimental_rerun()
        else:
            st.stop()
    
    
    with st.expander('IMPORTANT: Instruction for entering new sample information'):
        st.write('''
                 * Add rows: scroll to the bottom-most row and click on the “+” sign in any cell
                 * Delete rows: select one or more rows and press the `delete` key on your keyboard 
                 * Enter the date in `MM/DD/YY` format. 
                 * Enter numerical values in full (i.e. NOT scientific)
                 * Dropdown features: 
                     * Strain, Fermentation Scale, Cryo mix, 
                     * Ingredient 1, Ingredient 2, Ingredient 3, Container
                 ''')
    

    if "empty_df" not in st.session_state:
        st.session_state["empty_df"] = cast_df_columns(empty_df.copy())

    with st.form("my_form"):
        input_df = st.experimental_data_editor(st.session_state["empty_df"], num_rows="dynamic")
        
        submitted = st.form_submit_button("Submit")
        if submitted:
           st.subheader('Sample Information Compilation')
           
           # Process new dataframe
           df_v = sample_info(input_df)
           df_v0 = sample_info(st.session_state.df)

           # Join the new inputs to historical dataset
           df_v1 = df_v0.append(df_v, ignore_index=True)
           df_v1 = df_v1.drop_duplicates(subset=['FD sample ID', "FD Run ID", "Strain", "EFT date"], keep='last', ignore_index=True)

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
           st.session_state.df = df_v1
           st.write(df_v1.shape)

    if len(st.session_state.df) >0:
        st.download_button(
            label="Download Sample Info report as CSV",
            data=st.session_state.df.to_csv(),
            file_name='sample_info.csv',
            mime='text/csv')
        

def convert_time_features(i):
    """
    The convert_time_features function
    """
    if i == '':
        return None
    try:
        return pd.to_datetime(i, infer_datetime_format=True, format="%m/%d/%y")
    except ValueError:
        return i
    
    
def feature_eng(df):
    """
    This function format datetime and numerical features in the desirable format; 
    then create a column "Cryo mix Coef" containing a coefficient associates to each cryo-mix type. 
    
    INPUT: a dataframe with user inputs
    
    OUTPUT: a dataframe with features engineered for further analysis
    """
    
    for col in df:
        df[col] = df[col].apply(lambda x:x.strip())
        
    # Numerical features
    num_feat = ['EFT (hr)','Broth titer (CFU/mL)','Broth age (day)','Cryo mix addition rate',
                'FD run time (hr)','Primary ramp rate (C/min)','Viability (CFU/g)']

    for col in num_feat:
        df[col] = df[col].astype(float)


    # Coefficient    
    cryo_coef = {
        'PVT70%': 0.285,
        'DSR': 0.342,
        'SKP': 0.380
    }
    df['Cryo mix Coef'] = df['Cryo mix'].map(cryo_coef)

    return df


def cal_yield(row):
    """
    Calculate the fermentation broth's yield
    """
    
    if row.isna().any():
        return np.nan
    else:
        return round((row['Viability (CFU/g)']*row['Cryo mix Coef']/row['Broth titer (CFU/mL)'])*100,2)

    
def log_loss(x):
    """
    Calculate log10 loss of yield
    """
    
    if pd.isna(x):
        return np.nan
    else:
        return round(np.log10(x/100),2)

    
def sample_info(df):
    """
    The sample_info function takes in a dataframe containing user inputs, then formats the datetime, numerical and cateogrical features.
    This function performs calcualtion on the material's yield and log loss. 
    It returns a dataframe with sample's information entered by the user and according calcualted values
    
    INPUT: a dataframe with user inputs
    
    OUTPUT: a dataframe with sample's information and analysis 
    """
    
    for col in time_feats:
        df[col] = df[col].apply(convert_time_features)
        
        
    df = feature_eng(df)
    
    to_cal = df[['Broth titer (CFU/mL)','Viability (CFU/g)','Cryo mix Coef']]
    df['Yield (%)'] = to_cal.apply(cal_yield, axis=1)
    df['Log Loss'] = df['Yield (%)'].apply(log_loss)
    
    return df 




