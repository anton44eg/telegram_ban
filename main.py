import asyncio
from contextlib import suppress
import logging
import os
import random

import funcy
from pyrogram import Client
from pyrogram.errors import UsernameInvalid, UsernameNotOccupied
from pyrogram.raw.functions.messages import Report
from pyrogram.raw.types import InputReportReasonViolence

api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')


async def main():
    with open('chats.txt') as chats_file:
        chat_names = funcy.lfilter(None, chats_file.readlines())
    with open('report_texts.txt') as texts_file:
        texts = funcy.lfilter(None, texts_file.readlines())
    async with Client("my_account", api_id, api_hash) as app:
        random.shuffle(list(set(chat_names)))
        for chat_name in chat_names:
            with suppress(UsernameInvalid, UsernameNotOccupied):
                chat_name = chat_name.removeprefix('https://t.me/').removeprefix('@').strip()
                print(f'Baning {chat_name}')
                chat = await app.get_chat(chat_name)
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
                print(f'Channel {chat_name} reported')
            await asyncio.sleep(random.randint(1, 60))

asyncio.run(main())
