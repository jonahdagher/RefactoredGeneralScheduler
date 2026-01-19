from sqlalchemy import select, and_, exists, not_
from file_classes.csv_classes import *

from sqlalchemy import select, func, and_, exists, not_
import json


def get_date_range(session, start_date=None, end_date=None):
    query = select(ProviderDate.date)
    if start_date:
        query = query.where(ProviderDate.date >= start_date)
    if end_date:
        query = query.where(ProviderDate.date <= end_date)

    results = session.execute(query)
    return results.scalars().unique().all()

def get_date_attribute_filters(path):
    with open(path, "r") as js:
        data = json.load(js)
    return data

from sqlalchemy import delete, select

def delete_dates_in_range(session, start_date=None, end_date=None):
    # subquery selecting ProviderDate ids in range
    ids_q = select(ProviderDate.id)
    if start_date:
        ids_q = ids_q.where(ProviderDate.date >= start_date)
    if end_date:
        ids_q = ids_q.where(ProviderDate.date <= end_date)

    # delete child rows first
    session.execute(
        delete(DateAttribute).where(DateAttribute.provider_date_id.in_(ids_q))
    )

    # delete parent rows
    res = session.execute(
        delete(ProviderDate).where(ProviderDate.id.in_(ids_q))
    )

    session.commit()
    return res.rowcount

