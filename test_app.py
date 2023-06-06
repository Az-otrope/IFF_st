# Purpose: to test out streamlit features locally 

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid


## Create an empty DataFrame with columns A, B, and C
#empty_df = pd.DataFrame(columns=['A', 'B', 'C'])
#
## Use st.empty() to create a container for the DataFrame
#container = st.empty()
#
## Display the empty DataFrame within the container
#container.dataframe(empty_df)
#
## Use st.text_input() to get user input
#a_value = st.text_input("Enter a value for column A:")
#b_value = st.text_input("Enter a value for column B:")
#c_value = st.text_input("Enter a value for column C:")
#
## Use pd.concat() to add the user input to the DataFrame
#if st.button("Add row"):
#    new_row = pd.DataFrame([[a_value, b_value, c_value]], columns=['A', 'B', 'C'])
#    empty_df = pd.concat([empty_df, new_row], ignore_index=True)
#    container.dataframe(empty_df)

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
#

# Create a sample DataFrame
#df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': ['apple', 'banana', 'apple', 'orange'],
#                  'C':['x','y','z','o']})
#
## Use the DataFrameInput component to display the DataFrame with a selectbox for column B
#with st.form("my_form"):
#    edited_df = st.experimental_data_editor(df, num_rows='dynamic')
#    for col in df.columns:
#        df[col] = df[col].astype('category')
#    
#    submitted = st.form_submit_button("Submit")
#
#if submitted:
#    # Get the updated DataFrame from the component value
#    updated_df = pd.DataFrame(edited_df)
#    st.write(updated_df)

df = pd.DataFrame({'Courses': pd.Series(dtype='str'),
                   'Fee': pd.Series(dtype='int'),
                   'Duration': pd.Series(dtype='str'),
                   'Discount': pd.Series(dtype='float'),
                   'date': pd.Series(dtype='object')})
edit_df = st.experimental_data_editor(df, num_rows='dynamic')
