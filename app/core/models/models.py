from . import Base

from sqlalchemy import Integer, BigInteger, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class Channel(Base):
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_chat_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(100), nullable=True)


class Distribution(Base):
    __tablename__ = "distributions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    interval_measure: Mapped[str] = mapped_column(String(100))
    interval_number: Mapped[int] = mapped_column(Integer)
    interval_count: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(String)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_user_id: Mapped[int] = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(200))
    phone: Mapped[str] = mapped_column(String(20))
    channel_id: Mapped[int] = mapped_column(ForeignKey("channels.id"))
    distribution_id: Mapped[int] = mapped_column(ForeignKey("distributions.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    channel: Mapped[Channel] = relationship()
    distribution: Mapped[Distribution] = relationship()

    def __repr__(self):
        return f'User(id={self.id!r}, telegram_chat_id={self.telegram_chat_id!r}, username={self.username!r}, ' \
               f'name={self.name!r}, channel_id={self.channel!r}, distribution_id={self.distribution_id!r})'
