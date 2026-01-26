import streamlit as st
import os
from file_classes.csv_classes import *
from database_functions.provider_functions import *
from database_functions.date_functions import get_date_range, delete_dates_in_range
from database_functions.schema import *
from streamlit_components.streamlit_database import *

db_path = r"sqlite:///C:/Users/jonah/Desktop/RefactoredWaterfall/database.db"
schedule_files = os.listdir("C:\\Users\\jonah\\Desktop\\Waterfall\\schedules")

schedule_path = st.selectbox("Select Schedule Path", key=2, 
             options=schedule_files)

ss = st.session_state

if "NEW_BATCH" not in ss: ss.NEW_BATCH = None

#READ/CANCEL button creates or clears the new session depending on the state
if st.button("READ" if not ss.NEW_BATCH else "CANCEL"): 
    if not ss.NEW_BATCH: 
        ss.NEW_BATCH = {"Created": True}
    else: 
        ss.pop("NEW_BATCH")
    st.rerun()

if "NEW_BATCH" not in ss: ss.NEW_BATCH = None

if ss.NEW_BATCH:
    try:
        schedule = ScheduleFile("C:\\Users\\jonah\\Desktop\\Waterfall\\schedules\\" + schedule_path)
    except ValueError:
        st.error(f"There was an issue extracting the month and year from {schedule_path} please ensure the file name contains the month (written) and year (XXXX)")
        st.date_input("Manual Date Input", "00-00-0000")

    
    db_engine = create_engine("sqlite:///database.db", connect_args={"check_same_thread": False})
    Session = sessionmaker(
        bind=db_engine,
        autoflush=False,
        autocommit=False
    )
    session = Session()
    Base.metadata.create_all(db_engine)

    existing_days_for_inputted_month = get_date_range(session, f"{schedule.year_month}-01", f"{schedule.year_month}-31")
    if existing_days_for_inputted_month:
        st.warning(f"Detected existing dates for month [{schedule.year_month}]. Commiting changes will overide these dates")


    #Identify any newly detected providers and handle them.
    providers_existing_in_database = set([p.name for p in get_providers(session)])
    providers_found_in_file = set(schedule.getProviderRows().keys())

    #Providers found in file that are not already in the database
    if "new_providers" not in ss.NEW_BATCH:
        ss.NEW_BATCH["new_providers"] = providers_found_in_file.difference(providers_existing_in_database)

    if "processed_new_providers" not in ss.NEW_BATCH:
        ss.NEW_BATCH["processed_new_providers"] = {}
 
    unprocessed_providers = ss.NEW_BATCH["new_providers"].difference(set(ss.NEW_BATCH["processed_new_providers"].keys()))    
    # with st.expander("View State"):
    #     st.write(providers_existing_in_database)
    #     st.write(ss.NEW_BATCH)
    #     st.write(unprocessed_providers)

    with st.container(border=True):

        if unprocessed_providers:

            selected_provider = st.selectbox("Select Provider", options=unprocessed_providers)
        
            #Multiselect box to apply attributes to new providers
            if selected_provider:
                selected_provider_attributes = st.multiselect("Select Attributes to Apply", options=get_all_provider_attribute_names(session), format_func=lambda an: an.name)
            
            #Confirm and Delete Buttons
            col1, col2 = st.columns(2)

            with col1:
                confirmedRemove = st.checkbox("CONFIRM REMOVE")
                Remove_button = st.button("REMOVE", disabled=not confirmedRemove)

            with col2:
                addAll = st.checkbox("Add All New Providers")
                if st.button("CONFIRM" if not addAll else "ADD ALL", disabled=confirmedRemove):
                    if not addAll:
                        ss.NEW_BATCH["processed_new_providers"][selected_provider] = list(selected_provider_attributes)        
                    else:
                        for name in unprocessed_providers:
                                ss.NEW_BATCH["processed_new_providers"][name] = []                                
                    st.rerun()
        else:
            st.success("No Unprocessed Providers Detected")
            if st.button(label="Commit Changes to Database"):
                if existing_days_for_inputted_month:
                    delete_dates_in_range(session, existing_days_for_inputted_month[0], existing_days_for_inputted_month[-1])
                    
                for name in ss.NEW_BATCH["processed_new_providers"]:
                    p = Provider(name=name)
                    p.attributes = [ProviderAttribute(attribute_name=pn.name) for pn in ss.NEW_BATCH["processed_new_providers"][name]]

                    session.add(p)
                session.flush()

                added_dates = []
                provider_schedules = schedule.getProviderSchedules()
                with open("attribute_filter.json", "r") as js: filter = json.load(js)
                with open("settings.json", "r") as s: settings = json.load(s)

                for name in provider_schedules:

                    provider_obj = session.execute(select(Provider).where(Provider.name == name)).scalar_one_or_none()

                    entries = provider_schedules[name].schedule
                    for entry in entries:

                        detected_attributes = []
                        if str(entry.value) not in filter or entry.value == None:
                            detected_attributes.append(settings["attributes"]["default_empty_attribute"])
                        else:
                            color_attribute = filter.get(str(entry.color))
                            value_attribute = filter.get(str(entry.value))

                            if color_attribute: detected_attributes.append(color_attribute)
                            if value_attribute: detected_attributes.append(value_attribute)
                            
                        pd = ProviderDate(
                            provider=provider_obj,
                            date=entry.date,
                            color=entry.color,
                            value=entry.value
                        )
                        
                        pd.attributes = [
                            DateAttribute(name=a)
                            for a in detected_attributes
                        ]

                        added_dates.append(pd)
                        
                session.add_all(added_dates)
                
                ss.pop("NEW_BATCH")
                # try:
                session.commit()
                # except:
                # session.rollback()
                st.rerun()
