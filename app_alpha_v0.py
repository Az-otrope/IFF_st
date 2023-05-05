import streamlit as st

from boost import boost_app
from pivot_in_pack import pivot_in_pack_app
from pivot_on_seed import pivot_on_seed_app

import pandas as pd

import warnings
warnings.filterwarnings("ignore")

if 'pivot_df' not in st.session_state:
    st.session_state['pivot_df'] = pd.DataFrame()

# DASHBOARD
add_sidebar = st.sidebar.selectbox('Project', ('Boost','Pivot In-pack','Pivot On-seed'))
                                  

if __name__ == '__main__':
    if add_sidebar == 'Pivot In-pack':
        pivot_in_pack_app()
    elif add_sidebar == 'Pivot On-seed':
        pivot_on_seed_app()
    elif add_sidebar == 'Boost':
        boost_app()
