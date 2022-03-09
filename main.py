import asyncio
from contextlib import suppress
import os
import time
import random
from pathlib import Path

import funcy
import pickledb
from pyrogram import Client
from pyrogram.errors import UsernameInvalid, UsernameNotOccupied, ChannelPrivate, FloodWait, PeerIdInvalid
from pyrogram.raw.functions.messages import Report
from pyrogram.raw.types import InputReportReasonViolence

from storage import Storage

api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
account_name = os.environ.get('ACCOUNT_NAME', 'my_account')


BANNED_TIMEOUT = 12 * 60 * 60  # 12 Hours


def get_key(channel_name):
    return f'channel:{channel_name}'


def save_banned(db, channel_name):
    db.set(get_key(channel_name), int(time.time()))


def is_banned_recently(db, channel_name):
    if not (timestamp := db.get(get_key(channel_name))):
        return False
    if (time.time() - int(timestamp)) > BANNED_TIMEOUT:
        return False
    return True


async def send_report(app, channel_name, texts):
    print(f'Reporting {channel_name}')
    chat = await app.get_chat(channel_name)
    messages = await app.get_history(chat.id)
    num_messages = random.randint(3, 10)
    message_ids = [
        message.message_id
        for msg_num, message in enumerate(messages)
        if msg_num < num_messages
    ]
    if not message_ids:
        return
    await app.send(
        Report(
            peer=await app.resolve_peer(peer_id=chat.id),
            id=message_ids,
            reason=InputReportReasonViolence(),
            message=random.choice(texts)
        )
    )


async def main():
    db = pickledb.load(f'state/{account_name}.db', True)
    with open('channels.txt') as chats_file:
        channel_names = funcy.lfilter(None, chats_file.readlines())
    with open('report_texts.txt') as texts_file:
        texts = funcy.lfilter(None, texts_file.readlines())
    storage = Storage(account_name, Path('state'))
    async with Client(storage, api_id, api_hash, no_updates=True, workdir='state') as app:
        channel_names = list(set(channel_names))
        random.shuffle(channel_names)
        print(f'{len(channel_names)} in list')
        for channel_name in channel_names:
            if channel_name.startswith('+'):
                continue
            channel_name = channel_name.removeprefix('https://t.me/').removeprefix('@').strip()
            if is_banned_recently(db, channel_name):
                print(f'{channel_name} was already reported in last 12 hours')
                continue
            with suppress(
                UsernameInvalid,
                UsernameNotOccupied,
                ChannelPrivate,
                PeerIdInvalid,
            ):
                try:
                    await send_report(app, channel_name, texts)
                    save_banned(db, channel_name)
                    print(f'Channel {channel_name} reported')
                except FloodWait as e:
                    print(e)
                    await asyncio.sleep(5)
            await asyncio.sleep(random.randint(1, 20))

    print('\nРуський воєнний корабль, іди нахуй!')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\nРуський воєнний корабль, іди нахуй!')
