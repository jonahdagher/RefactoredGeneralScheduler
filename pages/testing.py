from streamlit_components.streamlit_database import *
from sqlalchemy import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from database_functions.provider_functions import *

import os



engine = create_engine("sqlite:///database.db")

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

session = SessionLocal()
with st.container(border=True):
    provider_attribute_editor(session)

st.divider()
with st.container(border=True):
    create_provider_attribute(session)

st.divider()

with st.container(border=True):
    schedule_files = os.listdir("C:\\Users\\jonah\\Desktop\\Waterfall\\schedules")
    p = st.selectbox(label="File to Detect Inputs From",
                options=schedule_files)

    s = ScheduleFile("C:\\Users\\jonah\\Desktop\\Waterfall\\schedules\\" + p)
    detected_cell_values = s.getAllCellValues()

    create_attribute_filter("attribute_filter.json", default_inputs=detected_cell_values, default_attributes= get_all_attribute_names(session))

