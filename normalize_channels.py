import asyncio

import funcy


def normalize(filename):
    with open(filename) as chats_file:
        chat_names = funcy.lfilter(None, chats_file.readlines())
    chat_names = list(set(chat_names))
    normalized_names = []
    for chat_name in chat_names:
        chat_name = chat_name\
            .removeprefix('https://t.me/')\
            .removeprefix('http://t.me/')\
            .removeprefix('@')\
            .strip()
        if '/' in chat_name:
            chat_name = chat_name[:chat_name.index('/')]
        normalized_names.append(chat_name)
    with open(filename, 'w') as chats_file:
        chats_file.write('\n'.join(
            name
            for name in sorted(set(normalized_names))
            if not name.startswith('+')
        ))


def main():
    normalize('channels.txt')
    normalize('priority_channels.txt')


if __name__ == '__main__':
    main()
