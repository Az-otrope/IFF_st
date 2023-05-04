import streamlit as st
from datetime import date
import pandas as pd
import numpy as np
import altair as alt

from utils import upload_dataset


def boost_app():
    st.title('Boost Data Dashboard')
    data = upload_dataset()
    st.write('Time Range')
    exp_period = st.slider(
        'Choose a time range of completed experiments:',
        date(2019, 1, 1),
        date.today(),
        value=(date(2020, 1, 1), date(2021, 1, 1)),
        format='YYYY/MM/DD'
    )
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
    c = alt.Chart(chart_data).mark_circle().encode(x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
    st.altair_chart(c, use_container_width=True)
