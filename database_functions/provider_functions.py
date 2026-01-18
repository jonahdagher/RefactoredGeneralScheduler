from sqlalchemy import *
from file_classes.csv_classes import *

from sqlalchemy import select, func, and_, exists, not_

def get_providers(session, provider_attributes_specified=None, provider_attributes_excluded=None, date=None, date_attributes_specified=None, date_attributes_excluded=None):
    query = select(Provider)
    if date:
        query = query.join(ProviderDate).where(ProviderDate.date == date)
    if date_attributes_specified:
        for attribute in date_attributes_specified:
            query = query.where(ProviderDate.attributes.any(
                DateAttribute.name == attribute
            ))
    if date_attributes_excluded:
        query = query.where(~ProviderDate.attributes.any(
            DateAttribute.name.in_(date_attributes_excluded)
        ))
    if provider_attributes_specified:
        for attribute in provider_attributes_specified:
            query = query.where(Provider.attributes.any(
                ProviderAttribute.attribute_name == attribute
            ))
    if provider_attributes_excluded:
        query = query.where(~Provider.attributes.any(
            ProviderAttribute.attribute_name.in_(provider_attributes_excluded)
        ))

    return session.execute(query).scalars().all()



def get_all_attribute_names(session):
    return session.execute(select(ProviderAttribute.attribute_name)).scalars().unique().all()

