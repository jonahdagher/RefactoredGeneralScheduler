import streamlit as st

from sqlalchemy import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

from file_classes.csv_classes import *
from database_functions.provider_functions import *
import time




def provider_attribute_editor(session, provider=None, attribute=None):
    all_providers = session.execute(select(Provider)).scalars().all()
    all_attribute_names = get_all_provider_attribute_names(session)

    if provider is None:
        provider = st.selectbox("Select Provider", options=all_providers, format_func=lambda p: p.name)

    if provider is None:
        st.error("Please Select a Provider to Edit")
        return

    provider_current_attributes = session.execute(
        select(ProviderAttribute.attribute_name)
        .where(ProviderAttribute.provider_id == provider.id)
    ).scalars().all()

    key = f"attribute_multiselect_{provider.id}"

    if key not in st.session_state:
        st.session_state[key] = provider_current_attributes

    edited_attributes = st.multiselect(
        f"Classes for {provider.name}",
        options=all_attribute_names,
        key=key,
        format_func= lambda a: a.name
    )

    if set(provider_current_attributes) != set(edited_attributes):
        col1, col2 = st.columns(2)

        with col1:
            if st.button("CONFIRM"):
                provider = session.get(Provider, provider.id)
                session.execute(delete(ProviderAttribute).where(ProviderAttribute.provider_id == provider.id))
                session.add_all([
                    ProviderAttribute(provider_id=provider.id, attribute_name =a.name) for a in edited_attributes
                ])
                session.commit()

        with col2:
            if st.button("REVERT"):
                st.session_state[key] = provider_current_attributes
                st.rerun()


def create_provider_attribute(session):
    an = st.text_input("Attribute Name")
    color = st.color_picker("Attribute Color")
    if st.button("Create"):
        session.add(ProviderAttributeType(
            name=an,
            color=color
        ))

        session.commit()
        st.success(f"Attribute [{an}] Commited!")

import json
def create_attribute_filter(path, default_inputs=None, default_outputs=None):

    #Load Existing Links from File
    with open(path, "r") as js: attribute_filters = json.load(js)

    if default_inputs:
        default_inputs = set(default_inputs).difference(set(attribute_filters.keys()))

    #Display the existing links
    with st.expander("Existing Links"):
        for input, output in list(attribute_filters.items()):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                
                if input[0] == "#":
                    st.color_picker("input color", value=input, disabled=True, label_visibility="collapsed")
                else:
                    st.subheader(input)
            with col2:
                st.subheader(":")
            with col3:
                st.subheader(output)
            with col4:
                if st.button("delete", key=input):
                    with open(path, "w") as js:
                        del attribute_filters[input]
                        with open(path, "w") as js: json.dump(attribute_filters, js, indent=2)
                        st.rerun()
        #On button press Start "CREATING_NEW" mode (status stored in session state)
    if "CREATING_NEW" not in st.session_state: st.session_state.CREATING_NEW = False
    if not st.session_state.CREATING_NEW:
        if st.button("CREATE + "): 
            st.session_state.CREATING_NEW = True
            st.rerun()

    #If Creating a new link
    if st.session_state.CREATING_NEW:
            st.divider()
            col1, col2, col3 = st.columns([2,2,1])

            #Define input
            with col1:
                with st.container(border=True):

                    #Select filter mode
                    filter_mode = st.radio(label="Filter Input", 
                                horizontal=True, 
                                options=["Detected", "Manual"],)
                    
                    #Input as plain text if manual
                    if filter_mode == "Manual":
                        new_input = st.text_input(label="Filter",
                                        label_visibility="collapsed",
                                        key="manual_input")
                    
                    #Display list from "default_inputs" if detected
                    elif filter_mode == "Detected":
                        new_input = st.selectbox(label="filter",
                                    label_visibility="collapsed",
                                    options=default_inputs,)

            with col2:
                with st.container(border=True):
                    filter_mode = st.radio(label="Filter Output", 
                                horizontal=True, 
                                options=["Detected", "Manual"],)
                    
                    if filter_mode == "Manual":
                        new_output = st.text_input(label="Filter",
                                        label_visibility="collapsed",
                                        key="manual_output")
                        
                    elif filter_mode == "Detected":
                        new_output = st.selectbox(label="filter",
                                    label_visibility="collapsed",
                                    options=default_outputs,)
            with col3:
                with st.container(border=True):
                    #CREATE BUTTON
                    if st.button("Create Link",):
                        js.close()
                        with open(path, "w") as js:
                            attribute_filters[new_input] = new_output
                            json.dump(attribute_filters, js, indent=2)
                        st.session_state.CREATING_NEW = False
                        st.rerun()
                    #CANCEL BUTTON
                    elif st.button(label="Cancel",):
                    
                        st.session_state.CREATING_NEW = False
                        st.rerun()