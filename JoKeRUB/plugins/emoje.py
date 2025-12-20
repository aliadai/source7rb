from JoKeRUB import l313l
from telethon.extensions import markdown, html
from telethon import types


class InvalidFormatException(Exception):
    """استثناء يُستخدم عند تمرير نوع تنسيق غير مدعوم."""

    pass


class CustomParseMode:
    """وضع مخصص لتحليل النص مع دعم السبويلر والايموجيات المخصصة."""

    def __init__(self, parse_mode: str):
        self.parse_mode = parse_mode

    def parse(self, text):
        if self.parse_mode == "markdown":
            text, entities = markdown.parse(text)
        elif self.parse_mode == "html":
            text, entities = html.parse(text)
        else:
            raise InvalidFormatException("Invalid parse mode. Choose either Markdown or HTML.")

        for i, e in enumerate(entities):
            if isinstance(e, types.MessageEntityTextUrl):
                if e.url == "spoiler":
                    entities[i] = types.MessageEntitySpoiler(e.offset, e.length)
                elif e.url.startswith("emoji/"):
                    entities[i] = types.MessageEntityCustomEmoji(
                        e.offset, e.length, int(e.url.split("/")[1])
                    )
        return text, entities

    @staticmethod
    def unparse(text, entities):
        for i, e in enumerate(entities or []):
            if isinstance(e, types.MessageEntityCustomEmoji):
                entities[i] = types.MessageEntityTextUrl(
                    e.offset, e.length, f"emoji/{e.document_id}"
                )
            if isinstance(e, types.MessageEntitySpoiler):
                entities[i] = types.MessageEntityTextUrl(
                    e.offset, e.length, "spoiler"
                )
        return html.unparse(text, entities)
