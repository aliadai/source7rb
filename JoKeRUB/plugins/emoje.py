from JoKeRUB import l313l
from telethon.extensions import markdown, html
from telethon import types
from telethon.tl.types import MessageEntityCustomEmoji


plugin_category = "utils"


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


async def process_custom_emojis_ids(event):
    """استخراج الايموجيات المخصصة من الرسالة وإرجاعها كنصوص منسّقة."""

    message_text = event.message.message
    custom_emojis = []

    if event.entities:
        # تجنّب تكرار نفس الاوفست أكثر من مرة
        processed_offsets = set()

        for entity in event.entities:
            if isinstance(entity, MessageEntityCustomEmoji):
                if entity.offset not in processed_offsets:
                    try:
                        # قصّ الايموجي من النص بحسب الطول والاوفست
                        emoji = message_text[entity.offset : entity.offset + entity.length]
                        emoji_id = entity.document_id

                        if emoji and emoji_id:
                            # تنسيق عربي قريب من أسلوب باقي السورس
                            custom_emojis.append(
                                f"⌔︙ايدي الايموجي : `{emoji_id}` | الايموجي : {emoji} \n"
                                f"⌔︙رابطه : [{emoji}](emoji/{emoji_id})"
                            )
                            processed_offsets.add(entity.offset)
                    except Exception as e:
                        print(f"Error processing emoji: {e}")

    return custom_emojis


@l313l.ar_cmd(
    pattern="تجربة(?:\s|$)([\s\S]*)",
    command=("تجربة", plugin_category),
    info={
        "header": "عرض قائمة اوامر القوائم مع ايموجيات مخصصة.",
        "usage": "{tr}تجربة",
    },
)
async def تجربة_ايموجي(event):
    await event.edit(
        """
✧ `.م1` [⚙️](emoji/5971846335085678067)  
✧ `.م2` [📟](emoji/5260640681906419699)  
✧ `.م3` [⛳️](emoji/5264710717470158023)  
✧ `.م4` [🛠](emoji/5863945989127148135)  
✧ `.م5` [🎯](emoji/5397782960512444700)  
✧ `.م6` [💰](emoji/5213094908608392768)  
✧ `.م7` [🎲](emoji/5879623757923881824)  
✧ `.م8` [🧩](emoji/5429368540849260641)  
""",
        link_preview=None,
        parse_mode=CustomParseMode("markdown"),
    )


@l313l.ar_cmd(
    pattern="ايدي_ايموجي(?:\s|$)([\s\S]*)",
    command=("ايدي_ايموجي", plugin_category),
    info={
        "header": "استخراج آيديات الايموجيات المخصصة من الرسالة.",
        "usage": "{tr}ايدي_ايموجي (بالرد على رسالة تحوي ايموجيات)",
    },
)
async def ايدي_ايموجي_كوماند(event):
    custom_emojis = await process_custom_emojis_ids(event)

    if custom_emojis:
        for line in custom_emojis:
            await event.client.send_message(
                event.chat_id,
                line,
                parse_mode=CustomParseMode("markdown"),
            )
    else:
        await event.edit("⌔︙ما لقيت اي ايموجي مخصص بالرسالة.")
