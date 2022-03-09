from pyrogram.storage import FileStorage


class Storage(FileStorage):
    USERNAME_TTL = 24 * 60 * 60  # 24 hours
