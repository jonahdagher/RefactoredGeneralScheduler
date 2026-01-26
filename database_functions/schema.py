from sqlalchemy import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


Base = declarative_base()
class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    attributes = relationship("ProviderAttribute", back_populates="provider")

    dates = relationship("ProviderDate", back_populates="provider")

class ProviderAttribute(Base):
    __tablename__ = "provider_attributes"

    provider_id = Column(ForeignKey("providers.id"), primary_key=True)
    attribute_name = Column(String, primary_key=True)

    provider = relationship("Provider", back_populates="attributes")
    color = Column(String)

class ProviderAttributeType(Base):
    __tablename__ = "provider_attribute_types"

    name = Column(String, primary_key=True)
    color = Column(String)


class ProviderDate(Base):
    __tablename__ = "provider_dates"

    id = Column(Integer, primary_key=True)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)
    date = Column(String, nullable=False)

    attributes = relationship("DateAttribute", back_populates="date")

    color = Column(String)
    value = Column(String)

    provider = relationship("Provider", back_populates="dates")

    __table_args__ = (UniqueConstraint("provider_id", "date", name="uq_provider_date"),)

class DateAttribute(Base):
    __tablename__ = "date_attributes"

    id = Column(Integer, primary_key=True)

    provider_date_id = Column(Integer, ForeignKey("provider_dates.id", ondelete="CASCADE"), nullable=False)
    name = Column(String)
    date = relationship("ProviderDate", back_populates="attributes")

class PreviousRankings(Base):
    __tablename__ = "previous_rankings"

    id = Column(Integer, primary_key = True)
    year_month = Column(String, nullable=False, unique=True)
    ranking_lists = Column(JSON)

def remove_provider_dates_by_month(session, year_month):
    month_prefix = f"{year_month}-"
    session.execute(
        delete(ProviderDate
            ).where(ProviderDate.date.like(f"{month_prefix}%"))
    )