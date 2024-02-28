import asyncio

from telethon.sync import TelegramClient
from app.core.repositories import users, channels
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantCreator

from app.settings import settings
import logging


def parse_channels_and_groups():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    with TelegramClient("channel_parser", settings.telegram_api_id, settings.telegram_api_hash) as client:
        for dialog in client.iter_dialogs():
            if dialog.is_group:
                channel = channels.save_channel(dialog.entity.id, dialog.name, "")
                # admins = [_user.id for _user in
                #           client.iter_participants(entity=dialog.entity, filter=ChannelParticipantsAdmins)]
                admins = []
                for _user in client.iter_participants(entity=dialog.entity):
                    if _user.is_self or _user.bot or _user.deleted or _user.id in admins:
                        continue
                    full_name = _user.first_name
                    if _user.last_name:
                        full_name += f" {_user.last_name}"
                    users.create_user(
                        _user.id,
                        _user.username,
                        full_name,
                        _user.phone,
                        channel.id
                    )
