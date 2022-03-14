from pyrogram.storage import FileStorage


class Storage(FileStorage):
    USERNAME_TTL = 72 * 60 * 60  # 72 hours
