import streamlit as st
import os
from database_functions.provider_functions import *
from database_functions.date_functions import *
from database_functions.schema import *
from database_functions.output_classes import *
from streamlit_components.streamlit_database import *


db_engine = create_engine("sqlite:///database.db", connect_args={"check_same_thread": False})
Session = sessionmaker(
    bind=db_engine,
    autoflush=False,
    autocommit=False
)
session = Session()

r = RankedPercentOutput(session, ["730"], ["extra"], ["530"])
date_range = get_date_range(session, "2026-01", "2026-01-30")
# for date in date_range:
date="2026-01-23"
rd = r.getRankingForDate(date)
print(rd)