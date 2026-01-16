"""
seed_test_data.py
Run: python seed_test_data.py
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from file_classes.csv_classes import (
    Base,
    Provider,
    ProviderDate,
    PreviousRankings,
    ProviderAttribute,
)

DB_URL = "sqlite:///database.db"


def seed():
    engine = create_engine(DB_URL, echo=False, future=True)
    SessionLocal = sessionmaker(bind=engine, future=True)

    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        # wipe for clean run (delete children first)
        session.query(ProviderDate).delete()
        session.query(PreviousRankings).delete()
        session.query(ProviderAttribute).delete()
        session.query(Provider).delete()
        session.commit()

        # --- Providers + Attributes ---
        providers = [
            Provider(
                name="Alice Chen",
                attributes=[
                    ProviderAttribute(attribute_name="regular"),
                ],
            ),
            Provider(
                name="Ben Diaz",
                attributes=[
                    ProviderAttribute(attribute_name="regular"),
                    ProviderAttribute(attribute_name="float"),
                ],
            ),
            Provider(
                name="Cara Singh",
                attributes=[
                    ProviderAttribute(attribute_name="coral_springs"),
                ],
            ),
            Provider(
                name="Dylan Park",
                attributes=[
                    ProviderAttribute(attribute_name="regular"),
                ],
            ),
        ]

        session.add_all(providers)
        session.commit()

        provider_by_name = {
            p.name: p for p in session.query(Provider).all()
        }

        # --- ProviderDates ---
        schedule = {
            "Alice Chen": [
                ("2026-01-05", "AM", "#92D050", "working"),
                ("2026-01-07", "AM", "#FFFFFF", "working"),
            ],
            "Ben Diaz": [
                ("2026-01-06", "PM", "#00B0F0", "working"),
                ("2026-01-09", "PM", "#00B0F0", "working"),
            ],
            "Cara Singh": [
                ("2026-01-05", "AM", "#FFC000", "working"),
                ("2026-01-08", "AM", "#FFC000", "working"),
            ],
            "Dylan Park": [
                ("2026-01-07", "PM", "#FF0000", "working"),
            ],
        }

        provider_dates = []
        for name, entries in schedule.items():
            pid = provider_by_name[name].id
            for date, value, color, status in entries:
                provider_dates.append(
                    ProviderDate(
                        provider_id=pid,
                        date=date,
                        value=value,
                        color=color,
                    )
                )

        session.add_all(provider_dates)
        session.commit()

        # --- PreviousRankings ---
        session.add(
            PreviousRankings(
                year_month="2026-01",
                ranking_lists={
                    "AM": ["Alice Chen", "Cara Singh"],
                    "PM": ["Ben Diaz", "Dylan Park"],
                },
            )
        )
        session.commit()

        print("Seeded providers:", session.query(Provider).count())
        print("Seeded provider_attributes:", session.query(ProviderAttribute).count())
        print("Seeded provider_dates:", session.query(ProviderDate).count())
        print("Seeded previous_rankings:", session.query(PreviousRankings).count())


if __name__ == "__main__":
    seed()
