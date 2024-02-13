from typing import List

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


def update_user_distribution(telegram_user_id, distribution: Distribution):
    with Session(engine) as session:
        user = session.query(User).filter(User.telegram_user_id == telegram_user_id).first()
        if user:
            user.distribution_id = distribution.id
            session.commit()
