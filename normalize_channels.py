import asyncio

import funcy


async def main():
    with open('channels.txt') as chats_file:
        chat_names = funcy.lfilter(None, chats_file.readlines())
    chat_names = list(set(chat_names))
    normalized_names = []
    for chat_name in chat_names:
        chat_name = chat_name.removeprefix('https://t.me/').removeprefix('@').strip()
        normalized_names.append(chat_name)
    for name in sorted(set(normalized_names)):
        print(name)

asyncio.run(main())
