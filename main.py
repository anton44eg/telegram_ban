import asyncio
from contextlib import suppress
import os
import time
import random

import funcy
import pickledb
from pyrogram import Client
from pyrogram.errors import UsernameInvalid, UsernameNotOccupied, ChannelPrivate, FloodWait
from pyrogram.raw.functions.messages import Report
from pyrogram.raw.types import InputReportReasonViolence

api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')


BANNED_TIMEOUT = 12 * 60 * 60  # 12 Hours

get_key = lambda channel_name: f'channel:{channel_name}'


def save_banned(db, channel_name):
    db.set(get_key(channel_name), int(time.time()))


def is_banned_recently(db, channel_name):
    if not (timestamp := db.get(get_key(channel_name))):
        return False
    if (time.time() - int(timestamp)) > BANNED_TIMEOUT:
        return False
    return True


async def main():
    db = pickledb.load('state/db.db', True)
    with open('channels.txt') as chats_file:
        channel_names = funcy.lfilter(None, chats_file.readlines())
    with open('report_texts.txt') as texts_file:
        texts = funcy.lfilter(None, texts_file.readlines())
    async with Client("my_account", api_id, api_hash, no_updates=True, workdir='state') as app:
        channel_names = list(set(channel_names))
        random.shuffle(channel_names)
        print(f'{len(channel_names)} in list')
        for channel_name in channel_names:
            channel_name = channel_name.removeprefix('https://t.me/').removeprefix('@').strip()
            if is_banned_recently(db, channel_name):
                print(f'{channel_name} was already reported in last 12 hours')
                continue
            with suppress(UsernameInvalid, UsernameNotOccupied, ChannelPrivate):
                try:
                    print(f'Reporting {channel_name}')
                    chat = await app.get_chat(channel_name)
                    messages = await app.get_history(chat.id)
                    num_messages = random.randint(3, 10)
                    await app.send(
                        Report(
                            peer=await app.resolve_peer(peer_id=chat.id),
                            id=[
                                message.message_id
                                for msg_num, message in enumerate(messages)
                                if msg_num < num_messages
                            ],
                            reason=InputReportReasonViolence(),
                            message=random.choice(texts)
                        )
                    )
                    save_banned(db, channel_name)
                    print(f'Channel {channel_name} reported')
                except FloodWait:
                    await asyncio.sleep(60)
            await asyncio.sleep(random.randint(1, 20))

if __name__ == '__main__':
    asyncio.run(main())
