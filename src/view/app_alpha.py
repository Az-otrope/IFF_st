import sys
from pathlib import Path
import streamlit as st

try:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
except:
    pass

from src.view.boost import boost_app
from src.view.pivot_in_pack import pivot_in_pack_app
from src.view.pivot_on_seed import pivot_on_seed_app
from src.view.sample_info import sample_info_app
from src.view.home_page import homepage

import warnings

warnings.filterwarnings("ignore")
st.set_page_config(layout="wide")

# DASHBOARD
add_sidebar = st.sidebar.selectbox("Option", ("Home", "Sample Information", "Pivot In-pack", "Pivot On-seed", "Boost"))
st.warning("EXPERIMENTAL AND DEVELOPING STAGE")

if __name__ == "__main__":
    if add_sidebar == "Home":
        homepage()
    elif add_sidebar == "Pivot In-pack":
        pivot_in_pack_app()
    elif add_sidebar == "Pivot On-seed":
        pivot_on_seed_app()
    elif add_sidebar == "Boost":
        boost_app()
    elif add_sidebar == "Sample Information":
        sample_info_app()
