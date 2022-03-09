from pyrogram.storage import FileStorage


class Storage(FileStorage):
    USERNAME_TTL = 48 * 60 * 60  # 24 hours
