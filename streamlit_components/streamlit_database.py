import streamlit as st

from sqlalchemy import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

from file_classes.csv_classes import *
from database_functions.provider_functions import *




def provider_attribute_editor(session, provider=None, attribute=None):
    if "REVERT_KEY" not in st.session_state:
        st.session_state.REVERT_KEY = 0

    all_providers = session.execute(select(Provider)).scalars().all()
    all_attribute_names = session.execute(select(ProviderAttribute.attribute_name).distinct()).scalars().all()

    if not provider:
        provider = st.selectbox(label="Select Provider", options=all_providers, format_func=lambda p: p.name)
    if not attribute:
        if not provider:
            st.error("Please Select a Provider to Edit")
     
        else:

            provider_current_attributes = session.execute(select(ProviderAttribute.attribute_name).join(Provider).where(Provider.name == provider.name)).scalars().all()   
            edited_attributes = st.multiselect(label=f"Classes for {provider.name}", options=all_attribute_names, default=provider_current_attributes, key=f"attribute_multiselect_{st.session_state.REVERT_KEY}")

            if set(provider_current_attributes) != set(edited_attributes):
                if st.button("CONFIRM"):
                    pass
                if st.button("REVERT"):
                    # st.session_state.REVERT_KEY += 1
                    st.rerun()

def create_provider_attribute(session):
    p = st.selectbox(label="Provider", options=get_providers(session), format_func= lambda p: p.name)
    an = st.text_input("Attribute Name")
    if st.button("Create"):
        session.add(ProviderAttribute(
            provider=p,
            attribute_name=an
        ))

import json
def create_attribute_filter(path, default_inputs=None, default_attributes=None):

    #Load Existing Links from File
    with open(path, "r") as js:
        attribute_filters = json.load(js)

        if default_inputs:
            default_inputs = set(default_inputs).difference(set(attribute_filters.keys()))

        #Display the existing links
        with st.expander("Existing Links"):
            for filter, attribute in attribute_filters.items():
                st.write(filter, attribute)
                st.divider()

        #On button press Start "CREATING_NEW" mode (status stored in session state)
        if "CREATING_NEW" not in st.session_state: st.session_state.CREATING_NEW = False
        if not st.session_state.CREATING_NEW:
            if st.button("CREATE + "): 
                st.session_state.CREATING_NEW = True
                st.rerun()

        #If Creating a new link
        if st.session_state.CREATING_NEW:
            with st.expander("Filter", expanded=True):
                col1, col2, col3 = st.columns([2,2,1])

                #Define input
                with col1:
                    with st.container(border=True):

                        #Select filter mode
                        filter_mode = st.radio(label="Filter Input", 
                                    horizontal=True, 
                                    options=["Detected", "Manual"],
                                    key="filter-mode" + filter + attribute)
                        
                        #Input as plain text if manual
                        if filter_mode == "Manual":
                            new_input = st.text_input(label="Filter",
                                            label_visibility="collapsed",
                                            key="filter-input" + filter + attribute)
                        
                        #Display list from "default_inputs" if detected
                        elif filter_mode == "Detected":
                            new_input = st.selectbox(label="filter",
                                        label_visibility="collapsed",
                                        options=default_inputs,
                                        key="select_box" + filter + attribute)

                with col2:
                    with st.container(border=True):
                        filter_mode = st.radio(label="Filter Input", 
                                    horizontal=True, 
                                    options=["Detected", "Manual"],
                                    key="attr-mode" + filter + attribute)
                        
                        if filter_mode == "Manual":
                            new_output = st.text_input(label="Filter",
                                            label_visibility="collapsed",
                                            key="attr-input" + filter + attribute)
                            
                        elif filter_mode == "Detected":
                            new_output = st.selectbox(label="filter",
                                        label_visibility="collapsed",
                                        options=default_attributes,
                                        key="attr-select_box" + filter + attribute)
                with col3:
                    with st.container(border=True):
                        if st.button("Create",
                                    key="edit" + filter + attribute):
                            js.close()
                            with open(path, "w") as js:
                                attribute_filters[new_input] = new_output
                                json.dump(attribute_filters, js, indent=2)
                            st.session_state.CREATING_NEW = False
                            st.rerun()



