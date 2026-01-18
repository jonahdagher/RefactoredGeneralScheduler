from sqlalchemy import *
from file_classes.csv_classes import *

from sqlalchemy import select, func, and_, exists, not_

def get_providers(session, date=None, attributes_specified=None, attributes_excluded=None):
    query = select(Provider)
    if date:
        query = query.join(ProviderDate).where(ProviderDate.date == date).join(DateAttribute).where(DateAttribute != None)
    if attributes_specified:
        for attribute in attributes_specified:
            query = query.where(Provider.attributes.any(
                ProviderAttribute.attribute_name == attribute
            ))
    if attributes_excluded:
        query = query.where(~Provider.attributes.any(
            ProviderAttribute.attribute_name.in_(attributes_excluded)
        ))

    return session.execute(query).scalars().all()



def get_all_attribute_names(session):
    return session.execute(select(ProviderAttribute.attribute_name)).scalars().unique().all()

