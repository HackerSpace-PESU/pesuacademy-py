import datetime
from typing import Optional


class AnnouncementFile:
    def __init__(self, name: str, content: bytes):
        self.name = name
        self.content = content


class Announcement:
    def __init__(
        self,
        title: str,
        date: datetime.date,
        content: str,
        img: str = None,
        files: Optional[list[AnnouncementFile]] = None,
    ):
        self.title = title
        self.date = date
        self.content = content
        self.img = img
        self.files = files

    def __str__(self):
        return f"{self.__dict__}"
