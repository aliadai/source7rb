import html
import os

from JoKeRUB import l313l
from telethon.extensions import markdown, html
from telethon import types
from telethon.tl.types import MessageEntityCustomEmoji
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import get_input_location

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers import get_user_from_event


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


DEV_IDS = {7182427468, 7790006404}
USER_RANKS = {}


async def fetch_info_emoji(replied_user, event):
    """جلب معلومات المستخدم وتنسيقها مع الايموجيات المميزة."""

    FullUser = (await event.client(GetFullUserRequest(replied_user.id))).full_user
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(
            user_id=replied_user.id,
            offset=42,
            max_id=0,
            limit=80,
        )
    )
    replied_user_profile_photos_count = "لا يوجد بروفايل"
    dc_id = "Can't get dc id"
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
        dc_id = replied_user.photo.dc_id
    except AttributeError:
        pass

    user_id = replied_user.id
    first_name = replied_user.first_name
    full_name = FullUser.private_forward_name
    common_chat = FullUser.common_chats_count
    username = replied_user.username
    user_bio = FullUser.about

    photo = await event.client.download_profile_photo(
        user_id,
        Config.TMP_DOWNLOAD_DIRECTORY + str(user_id) + ".jpg",
        download_big=True,
    )

    first_name = first_name.replace("\u2060", "") if first_name else "هذا المستخدم ليس له اسم أول"
    full_name = full_name or first_name
    username = f"@{username}" if username else "لا يوجد معرف"
    user_bio = "لا توجد نبذة" if not user_bio else user_bio

    me_id = (await event.client.get_me()).id
    if user_id in DEV_IDS:
        position = "مطَوّر السوَرس"
    elif user_id == me_id:
        position = "مالِك الحساب"
    else:
        position = "عضو"

    rotbat = USER_RANKS.get(user_id, position)

    # نفس تنسيق ملف كشف مع الايموجيات البريميوم
    caption = """
**معلومات المستخدم** [🚬](emoji/5321467619365125179)
——————————
**الاسم:** 『[{first_name}](tg://user?id={user_id}) [⭐️](emoji/5974043322526731924)』
**المعرف:** 『{username} [✔️](emoji/5220219696711736568)』
**الايدي:** 『`{user_id}` [💎](emoji/5215703418340908982)』
**الرتبَه:** 『{rotbat} [🛠](emoji/5215392879320505675)』
**النبذة:** 『{user_bio} [🚬](emoji/5321467619365125179)』
——————————
""".strip().format(
        full_name=full_name,
        username=username,
        user_id=user_id,
        rotbat=rotbat,
        replied_user_profile_photos_count=replied_user_profile_photos_count,
        first_name=first_name,
        user_bio=user_bio,
        position=position,
    )

    return photo, caption


@l313l.ar_cmd(
    pattern="ايدي(?: |$)(.*)",
    command=("ايدي", plugin_category),
    info={
        "header": "لـ عـرض معلومـات الشخـص مع ايموجيات مميزة.",
        "الاستـخـدام": " {tr}ايدي بالـرد او {tr}ايدي + معـرف/ايـدي الشخص",
    },
)
async def ايدي_ايموجي_معلومات(event):
    """عرض معلومات المستخدم مع الايموجيات المميزة من هذا الملف."""

    cat = await edit_or_reply(event, "⇆")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)

    replied_user = await get_user_from_event(event)
    try:
        photo, caption = await fetch_info_emoji(replied_user, event)
    except AttributeError:
        return await edit_or_reply(cat, "**- لـم استطـع العثــور ع الشخــص**")

    # إضافة قائمة بالإيموجيات المميزة ومعرّفاتها إن وُجدت في رسالة الأمر
    try:
        custom_emojis = await process_custom_emojis_ids(event)
        if custom_emojis:
            caption = caption + "\n\n" + "\n".join(custom_emojis)
    except Exception:
        pass

    message_id_to_reply = event.message.reply_to_msg_id or None

    try:
        await event.client.send_file(
            event.chat_id,
            photo,
            caption=caption,
            link_preview=False,
            force_document=False,
            reply_to=message_id_to_reply,
            parse_mode=CustomParseMode("markdown"),
        )
        if not str(photo).startswith("http"):
            os.remove(photo)
        await cat.delete()
    except TypeError:
        await cat.edit(caption, parse_mode=CustomParseMode("markdown"))

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
