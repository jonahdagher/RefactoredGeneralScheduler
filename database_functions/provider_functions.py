from sqlalchemy import select, and_, exists, not_
from file_classes.csv_classes import *

from sqlalchemy import select, func, and_, exists, not_

def get_providers(session, attributes_specified=None, attributes_excluded=None):
    attributes_specified = attributes_specified or []
    attributes_excluded = attributes_excluded or []

    # subquery: choose ONE provider.id per provider.name
    subq = select(func.min(Provider.id).label("id")).group_by(Provider.name)
    print(subq)

    for attr in attributes_specified:
        subq = subq.where(
            exists(
                select(1).where(
                    and_(
                        ProviderAttribute.provider_id == Provider.id,
                        ProviderAttribute.attribute_name == attr
                    )
                )
            )
        )

    for attr in attributes_excluded:
        subq = subq.where(
            not_(
                exists(
                    select(1).where(
                        and_(
                            ProviderAttribute.provider_id == Provider.id,
                            ProviderAttribute.attribute_name == attr
                        )
                    )
                )
            )
        )

    subq = subq.subquery()

    # final: fetch Provider objects whose id is in that per-name chosen set
    stmt = select(Provider).where(Provider.id.in_(select(subq.c.id)))

    return session.execute(stmt).scalars().all()



def get_all_attribute_names(session):
    return session.execute(select(ProviderAttribute.attribute_name)).scalars().unique().all()

