from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="Global AI concentration", layout="wide")

pages = [
    st.Page("pages/1_patents.py", title="Patents", default=True),
    st.Page("pages/2_publications.py", title="Publications"),
    st.Page("pages/3_investments.py", title="Investments"),
    st.Page("pages/4_concentration.py", title="Concentration + Narrative"),
]
st.navigation(pages).run()
