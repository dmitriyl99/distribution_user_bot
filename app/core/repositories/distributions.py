from typing import List, Type
from sqlalchemy.orm import Session

from app.core.db import engine
from app.core.models.models import Distribution


def create_distribution(
        name: str,
        interval_measure: str | None,
        interval_number: int | None,
        interval_count: int | None,
        text: str
) -> Distribution:
    with Session(engine) as session:
        distribution = Distribution(
            name=name,
            interval_measure=interval_measure,
            interval_number=interval_number,
            interval_count=interval_count,
            text=text
        )
        session.add(distribution)
        session.commit()
        session.refresh(distribution)

    return distribution


def get_all_distributions() -> List[Type[Distribution]]:
    with Session(engine) as session:
        return session.query(Distribution).all()
