import streamlit as st
import os
from database_functions.provider_functions import *
from database_functions.date_functions import *
from database_functions.schema import *
from database_functions.output_classes import *
from streamlit_components.streamlit_database import *
from streamlit_calendar import calendar
ss = st.session_state

db_engine = create_engine("sqlite:///database.db", connect_args={"check_same_thread": False})
Session = sessionmaker(
    bind=db_engine,
    autoflush=False,
    autocommit=False
)
session = Session()
# d = get_date_range(session, start_date="2026-02", end_date="2026-02-32")
for d in get_date_range(session, start_date="2026-02", end_date="2026-02-32"):
    providers_on_day = get_providers_on_date(session, d)
    for provider in providers_on_day:
        attributes_on_day = session.execute(
                                    select(DateAttribute)
                                    .join(ProviderDate, DateAttribute.provider_date_id == ProviderDate.id)
                                    .where(ProviderDate.date == d)
                                    .where(ProviderDate.provider_id == provider.id)   # or Provider.name filter via join
                                ).scalars().all()
        # st.write(provider.name, [a.name for a in attributes_on_day])
# calendar()