from typing import List, Type
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.db import engine
from app.core.models.models import User, Distribution


def get_all_users() -> List[User]:
    users: List[User] = []
    with Session(engine) as session:
        stmt = select(User).options(joinedload(User.channel), joinedload(User.distribution))
        for user in session.scalars(stmt):
            users.append(user)
    return users


def create_user(telegram_user_id, username, name, phone, channel_id) -> User:
    with Session(engine) as session:
        user = User(
            telegram_user_id=telegram_user_id,
            username=username,
            name=name,
            phone=phone,
            channel_id=channel_id
        )
        session.add(user)
        session.commit()

        return user


def update_user_distribution(telegram_user_id, distribution: Distribution | None):
    with Session(engine) as session:
        user = session.query(User).filter(User.telegram_user_id == telegram_user_id).first()
        if user:
            user.distribution_id = distribution.id if distribution else None
            user.distribution_sent = False
            user.distribution_date = None
            session.commit()


def get_users_by_distribution_id(distribution_id: int) -> List[Type[User]]:
    with Session(engine) as session:
        return session.query(User).filter(User.distribution_id == distribution_id).all()


def set_distribution_sent(user: User, distribution_date: datetime):
    with Session(engine) as session:
        session.add(user)
        user.distribution_sent = True
        user.distribution_date = distribution_date
        session.commit()
