from sqlalchemy import select, and_, exists, not_
from file_classes.csv_classes import *

from sqlalchemy import select, func, and_, exists, not_


def get_date_range(session, start_date=None, end_date=None):
    query = select(ProviderDate.date)
    if start_date:
        query = query.where(ProviderDate.date >= start_date)
    if end_date:
        query = query.where(ProviderDate.date <= end_date)

    results = session.execute(query)
    return results.scalars().unique().all()
