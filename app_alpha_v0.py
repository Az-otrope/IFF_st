import warnings
import yaml
from yaml.loader import SafeLoader

import streamlit as st
import streamlit_authenticator as stauth

from boost import boost_app
from pivot_in_pack import pivot_in_pack_app
from pivot_on_seed import pivot_on_seed_app
from sample_info import sample_info_app
from home_page import homepage

warnings.filterwarnings("ignore")

with open('aut.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
name, authentication_status, username = authenticator.login('Login', 'main')
if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')
    # DASHBOARD
    add_sidebar = st.sidebar.selectbox('Option', ('Home','Pivot Sample Information','Pivot In-pack',
                                                  'Pivot On-seed','Boost Sample Information','Boost'))
    if __name__ == '__main__':
        if add_sidebar == 'Home':
            homepage()
        elif add_sidebar == 'Pivot Sample Information':
            sample_info_app()
        elif add_sidebar == 'Pivot In-pack':
            pivot_in_pack_app()
        elif add_sidebar == 'Pivot On-seed':
            pivot_on_seed_app()
        elif add_sidebar == 'Boost':
            boost_app() 
        elif add_sidebar == 'Boost Sample Information':
            pass
elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')
# =============================================================================
# 
# 
# st.set_page_config(layout="wide")
# 
# 
# # DASHBOARD
# add_sidebar = st.sidebar.selectbox('Option', ('Home','Pivot Sample Information','Pivot In-pack',
#                                               'Pivot On-seed','Boost Sample Information','Boost'))                                 
# 
# if __name__ == '__main__':
#     if add_sidebar == 'Home':
#         homepage()
#     elif add_sidebar == 'Pivot Sample Information':
#         sample_info_app()
#     elif add_sidebar == 'Pivot In-pack':
#         pivot_in_pack_app()
#     elif add_sidebar == 'Pivot On-seed':
#         pivot_on_seed_app()
#     elif add_sidebar == 'Boost':
#         boost_app() 
#     #elif add_sidebar == 'Boost Sample Inormation':
#         
# 
# =============================================================================
