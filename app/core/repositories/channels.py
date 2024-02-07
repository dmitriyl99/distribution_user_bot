from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.db import engine
from app.core.models.models import Channel


def save_channel(telegram_chat_id, name, username) -> Channel:
    with Session(engine) as session:
        stmt = select(Channel).where(Channel.telegram_chat_id == telegram_chat_id)
        channel: Channel = session.scalar(stmt)
        if not channel:
            channel = Channel(
                telegram_chat_id=telegram_chat_id,
                name=name,
                username=username
            )
            session.add(channel)
        else:
            channel.name = name
            channel.username = username
        session.commit()
        session.refresh(channel)

        return channel
