import streamlit as st
import pandas as pd
from database_functions.output_classes import OutputColumn, OutputChunk, OutputSheet

ss = st.session_state

if "OUTPUT_PAGE" not in ss: ss["OUTPUT_PAGE"] = "SHEET"
OUTPUT_PAGE = ss["OUTPUT_PAGE"]

OUTPUT_PAGE_OPTIONS = ["LIST", "SHEET", "CHUNK"]

OUTPUT_PAGE = st.selectbox("PAGE", OUTPUT_PAGE_OPTIONS)

if OUTPUT_PAGE == "LIST":
    with st.container(border=True):
        LIST_MODE = st.radio(label="List By:",
                        options=["Provider Attribute", "Date Attribute"],
                        horizontal=True)
        date_attributes_excluded = None

elif OUTPUT_PAGE == "SHEET":
    pass

elif OUTPUT_PAGE == "CHUNK":
    pass

