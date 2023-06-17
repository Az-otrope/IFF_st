# Purpose: to test out streamlit features locally 

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid

## Use AgGrid
#st.title('Static DataFrame')
#df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
#st.write(df)
#
#st.title('AgGrid DataFrame')
#
## turn the df to AgGrid object and editable
#response = AgGrid(df, editable=True)
## make edits
#edited_df = response['data']
#st.write('Edited DataFrame')
#st.dataframe(edited_df)

#df = pd.DataFrame(
#        [
#            {"command": "st.selectbox", "rating": 4, "is_widget": True},
#            {"command": "st.balloons", "rating": 5, "is_widget": False},
#            {"command": "st.time_input", "rating": 3, "is_widget": True},
#        ]
#)
#df["command"] = (
#    df["command"].astype("category").cat.add_categories(["st.button", "st.radio"])
#)
#edited_df = st.experimental_data_editor(df)

# ================================================================================

# df = pd.DataFrame({'Courses': pd.Series(dtype='str'),
#                    'Fee': pd.Series(dtype='int'),
#                    'Duration': pd.Series(dtype='str'),
#                    'Discount': pd.Series(dtype='float'),
#                    'date': pd.Series(dtype='object')})
# edit_df = st.experimental_data_editor(df, num_rows='dynamic')

# ================================================================================

# This code allows only 1 entry at a time, has to delete the old entry before enter a new one
if 'dataframe' not in st.session_state:
    st.session_state['dataframe'] = pd.DataFrame()

user_input = st.text_input("Enter a value")
if st.button("Add to dataframe"):
    new_row = pd.DataFrame({'Value': [user_input]})
    st.session_state['dataframe'] = st.session_state['dataframe'].append(new_row, ignore_index=True)

st.write("Updated Dataframe:")
st.write(st.session_state['dataframe'])

