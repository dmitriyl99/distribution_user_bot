import datetime

from telethon.sync import TelegramClient

from app.core.repositories import users as users_repository
from app.core.repositories import distributions as distributions_repository
from app.settings import settings

import asyncio

import time


def distribute(distribution_id: int):
    users = users_repository.get_users_by_distribution_id(distribution_id)
    distribution = distributions_repository.get_distribution_by_id(distribution_id)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    with TelegramClient("channel_parser", settings.telegram_api_id, settings.telegram_api_hash) as client:
        for user in users:
            client.send_message(user.telegram_user_id, distribution.text)
            print(f"send message to {user.name}")
            users_repository.set_distribution_sent(user, datetime.datetime.now())
            time.sleep(5)

