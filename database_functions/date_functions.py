from sqlalchemy import select, and_, exists, not_
from file_classes.csv_classes import *
from database_functions.provider_functions import get_provider_by_name

from sqlalchemy import *
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

def get_provider_dates(session, provider, start=None, end=None,  date_attributes_included = None, date_attributes_excluded=None, noOFF=True):
    provider = get_provider_by_name(session, provider)
    query = select(ProviderDate).join(Provider).where(Provider.id == provider.id)
    if noOFF:
        query = query.where(~ProviderDate.attributes.any(DateAttribute.name == "OFF"))
    if start:
        query = query.where(ProviderDate.date >= start)
    if end:
        query = query.where(ProviderDate.date <= end)

    if date_attributes_included:
        query = query.join(ProviderDate.attributes).where(DateAttribute.name.in_(date_attributes_included))
    if date_attributes_excluded:
        query = query.where(~ProviderDate.attributes.any(DateAttribute.name.in_(date_attributes_excluded)))

    return session.execute(query).scalars().all()


    return session.execute(query).scalars().all()
def get_providers_on_date(session, date, date_attr_included=None, date_attr_excluded=None):
    q = (
        select(Provider)
        .join(ProviderDate, ProviderDate.provider_id == Provider.id)
        .where(ProviderDate.date == date)
    )
    q = q.where(~ProviderDate.attributes.any(DateAttribute.name == "OFF"))
    if date_attr_included:
        for attr in date_attr_included:
            q = q.where(ProviderDate.attributes.any(DateAttribute.name == attr))
    if date_attr_excluded:
        for attr in date_attr_excluded:
            q = q.where(~ProviderDate.attributes.any(DateAttribute.name == attr))

    return session.execute(q).scalars().all()

def get_date_attributes(session, provider, date):

    provider = get_provider_by_name(session, provider)

    query = select(DateAttribute).join(ProviderDate).where(ProviderDate.date == date, ProviderDate.provider_id==provider.id)
    return session.execute(query).scalars().all()