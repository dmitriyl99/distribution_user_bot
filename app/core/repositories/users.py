from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import engine
from app.core.models.models import User


def get_all_users() -> List[User]:
    users: List[User] = []
    with Session(engine) as session:
        stmt = select(User)
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

