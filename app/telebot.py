from telethon.sync import TelegramClient, events

from app.core.repositories import users, channels
from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantCreator

api_id = 3705975
api_hash = 'b694f055d1d9048cef688448bd8d3815'


with TelegramClient("channel_parser", api_id, api_hash) as client:
    for dialog in client.iter_dialogs():
        if dialog.is_group:
            if dialog.name == 'Support - Compliance / Merchant':
                # channel = channels.save_channel(dialog.entity.id, dialog.name, "")
                admins = [_user.id for _user in client.iter_participants(entity=dialog.entity, filter=ChannelParticipantsAdmins)]
                print(admins)
                for _user in client.iter_participants(entity=dialog.entity):
                    if _user.is_self or _user.bot or _user.deleted or _user.id in admins:
                        print(f"Skip user {_user.first_name}")
                        continue
                    full_name = _user.first_name
                    if _user.last_name:
                        full_name += f" {_user.last_name}"
                    print(_user)
                    # users.create_user(
                    #     _user.id,
                    #     _user.username,
                    #     full_name,
                    #     _user.phone,
                    #     channel.id
                    # )
                break
