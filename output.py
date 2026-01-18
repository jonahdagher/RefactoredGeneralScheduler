import streamlit as st
import pandas as pd
from database_functions.output_classes import OutputColumn, OutputChunk, OutputSheet

ss = st.session_state

if "OUTPUT_PAGE" not in ss: ss["OUTPUT_PAGE"] = "SHEET"
OUTPUT_PAGE = ss["OUTPUT_PAGE"]

OUTPUT_PAGE = st.selectbox("PAGE", ["SHEET", "TEST"])

if OUTPUT_PAGE == "SHEET":
    if st.button(label="Create New Output" if "NEW_OUTPUT" not in ss else "Confirm"):
        if "NEW_OUTPUT" not in ss:
            ss.NEW_OUTPUT = dict()
        else:
            ss.pop("NEW_OUTPUT")
        st.rerun()

    if "NEW_OUTPUT" in ss:
        with st.container(border=True):
            #How many chunks per row in output
            ss.NEW_OUTPUT["CHUNKS_PER_ROW"] = st.slider(label="Chunks per Row", 
                                                        min_value=1, 
                                                        max_value=20, 
                                                        value=5)
            
            #Should weeks be ordered, start with monday end with friday (only available if Chunks per Row is 5)
            isNotFivePerRow = ss.NEW_OUTPUT["CHUNKS_PER_ROW"] != 5
            ss.NEW_OUTPUT["ALIGN_WEEK"] = st.checkbox(label="Align week", 
                                                    value=not isNotFivePerRow,
                                                    disabled=isNotFivePerRow,
                                                    help="Chunks per Row Must be 5 to Align Weeks" if isNotFivePerRow else None)
            st.write("Select Chunk Pattern")
            col1, col2 = st.columns([7,3])
            with col1:
                st.selectbox(label="Select Chunk Pattern", label_visibility="collapsed",options=["TEST"])
            with col2:
                if st.button(label="Create New Pattern", disabled="NEW_CHUNK" in ss["NEW_OUTPUT"]):
                    ss["NEW_OUTPUT"]["NEW_CHUNK"] = dict()

            if "NEW_CHUNK" in ss["NEW_OUTPUT"]:
                NEW_CHUNK = ss["NEW_OUTPUT"]["NEW_CHUNK"]
                st.divider()