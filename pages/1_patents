from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import streamlit as st

from src.views import render_patent_view

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "sample.csv"
PROCESSED = ROOT / "data" / "processed.csv"


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    frame = pd.read_csv(
        path,
        dtype={"country_code": str},
        keep_default_na=False,
        na_values=[""],
        parse_dates=["date"],
    )
    return frame.sort_values(["country", "date"]).reset_index(drop=True)


def data_path() -> Path:
    sample_mode = os.getenv("DASHBOARD_SAMPLE_MODE", "0") == "1"
    if sample_mode or not PROCESSED.exists():
        return SAMPLE
    return PROCESSED


st.title("AI patents by country")
st.write(
    "**Question:** Which countries lead AI patenting, and how has their share of "
    "world AI patents changed from 2010 to 2024?"
)
st.caption("Audience: policy analysts comparing national innovation in AI.")

data = load_data(str(data_path()))

with st.container(key="patent_leaders"):
    render_patent_view(data)

with st.expander("Data and limitations"):
    st.markdown(
        "**Source:** OECD AI patent indicators, based on Patent Cooperation Treaty (PCT) "
        "applications. Counts are by priority year, and recent years may be estimates."
    )
    st.markdown(
        "**Shares:** each country's count divided by the world total (ALL). Others = world "
        "total minus the five countries shown."
    )
    st.markdown(
        "**Limitations:** patents measure inventions that are patented, not research quality "
        "or commercial success. Patent rules differ between offices."
    )
