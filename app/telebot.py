from telethon.sync import TelegramClient, events

from app.core.repositories import users, channels

api_id = 3705975
api_hash = 'b694f055d1d9048cef688448bd8d3815'


with TelegramClient("channel_parser", api_id, api_hash) as client:
    for dialog in client.iter_dialogs():
        if dialog.is_group:
            print(dialog.name)
            if dialog.name == 'Support - Compliance / Merchant':
                channel = channels.save_channel(dialog.entity.id, dialog.name, "")
                for _user in client.iter_participants(entity=dialog.entity):
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
                break
