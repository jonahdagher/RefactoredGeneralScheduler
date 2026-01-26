import json
import streamlit as st
from pathlib import Path

if "streamlit_json_key" not in st.session_state:
    st.session_state.streamlit_json_key = 0

st.session_state.streamlit_json_key

def path_setting(settings_path, key="paths"):

    #load json
    with open(settings_path, "r") as js: settings = json.load(js)

    #get all folder path keys and values
    folder_paths = settings["paths"]["folders"]

    #Select box to select folder path key
    path_name = st.selectbox("Path", options=folder_paths)

    existing_path_value = folder_paths[path_name]
    new_path_value = st.text_input("", existing_path_value, key=st.session_state.streamlit_json_key)

    if new_path_value != existing_path_value:
        pathExists = Path(new_path_value).exists()
        if not pathExists:
            st.error("Path Does Not Exist")
        if st.button("Confirm", disabled=not pathExists):
            settings["paths"]["folders"][path_name] = new_path_value
            with open(settings_path, "w") as js: json.dump(settings, js, indent=2)
            st.rerun()
            
        if st.button("Revert"):
            st.session_state.streamlit_json_key+=1
            st.rerun()
