import streamlit as st
import os
from database_functions.provider_functions import *
from database_functions.date_functions import *
from database_functions.schema import *
from database_functions.output_classes import *
from streamlit_components.streamlit_database import *
from database_functions.calendar_functions import get_provider_calendar_entries
from streamlit_calendar import calendar
ss = st.session_state

db_engine = create_engine("sqlite:///database.db", connect_args={"check_same_thread": False})
Session = sessionmaker(
    bind=db_engine,
    autoflush=False,
    autocommit=False
)
session = Session()

if "CAL_VIEW" not in ss: ss.CAL_VIEW = "dayGridMonth"
if "CLICKED_DATE" not in ss: ss.CLICKED_DATE = "2026-01-26"

def switch_mode():
    if ss.CAL_VIEW == "dayGridMonth":
        ss.CAL_VIEW = "listDay"
    else:
        ss.CAL_VIEW = "dayGridMonth"
    st.rerun()

if st.button("Switch Mode"):
    switch_mode()

#Set filter mode (exclusive or inclusive)
filter_mode = st.radio(label="Mode", options=["Exclusive", "Inclusive"], horizontal=True)
filterExclusive = True if filter_mode == "Exclusive" else False

#Create a multiselect with all the available attributes to filter by
with open("attribute_filter.json", "r") as js: all_date_attribute_names = set(json.load(js).values())
attributes_to_display = set(st.multiselect("test", options=all_date_attribute_names))

if st.button("Generate"):
    ss.CAL_ENTRIES = get_provider_calendar_entries(session,
    start = ss.CLICKED_DATE[:7],
    end = ss.CLICKED_DATE[:7] + "32",
    attributes_filter = attributes_to_display,
    filterExclusively = filterExclusive)

#Initalize the calendar
cal = calendar(events=ss.CAL_ENTRIES, options={
    "height":"1000px",
    "initialView": ss.CAL_VIEW, #Day or month
    "initialDate": ss.CLICKED_DATE #What day to focus on when in day view
})

#Set a default date ()
if "CLICKED_DATE" not in ss: ss.CLICKED_DATE = "2026-01-26"

try:
    if cal["callback"] == "dateClick":
        ss.CLICKED_DATE = clicked_date = cal["dateClick"]["date"][:10]
        switch_mode()
    elif cal["callback"] == "eventClick" and ss.CAL_VIEW == "dayGridMonth":
        ss.CLICKED_DATE = cal["eventClick"]["event"]["start"]
        switch_mode()
    st.write(ss.CLICKED_DATE)
except KeyError:
    pass
