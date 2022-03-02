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


async def main():
    with open('chats.txt') as chats_file:
        chat_names = funcy.lfilter(None, chats_file.readlines())
        chat_names = list(set(chat_names))
        for chat_name in chat_names:
            chat_name = chat_name.removeprefix('https://t.me/').removeprefix('@').strip()
            print(chat_name)

asyncio.run(main())
