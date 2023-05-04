import streamlit as st
from datetime import date

from utils import upload_dataset


def pivot_on_seed_app():
    st.title('Pivot On-seed Data Dashboard')
    data = upload_dataset()
    st.write('Time Range')
    exp_period = st.slider(
        'Choose a time range of completed experiments:',
        date(2019, 1, 1),
        date.today(),
        value=(date(2020, 1, 1), date(2021, 1, 1)),
        format='YYYY/MM/DD'
    )
