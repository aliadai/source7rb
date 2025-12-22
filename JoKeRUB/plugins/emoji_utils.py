import html
import os

from requests import get
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import get_input_location, pack_bot_file_id
from telethon.tl.types import MessageEntityMentionName
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from ..sql_helper.globals import gvarstatus

from JoKeRUB import l313l
from JoKeRUB.core.logger import logging
from telethon.extensions import markdown, html
from telethon import types
from telethon.tl.types import MessageEntityCustomEmoji
from ..Config import Config
from ..core.managers import edit_or_reply, edit_delete
from ..helpers import get_user_from_event, reply_id
from . import spamwatch
from .emoji_utils import CustomParseMode, process_custom_emojis_ids

JEP_EM = Config.ID_EM or " •❃ "
ID_EDIT = gvarstatus("ID_ET") or "ايدي"

plugin_category = "utils"
LOGS = logging.getLogger(name)
 
# مطورين السورس
DEV_IDS = {7182427468, 7790006404}

# تخزين محلي مبسط لرتب المستخدمين (غير دائم عبر إعادة التشغيل)
USER_RANKS = {}
async def get_user_from_event(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_object = await event.client.get_entity(previous_message.sender_id)
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if not user:
            self_user = await event.client.get_me()
            user = self_user.id
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        if isinstance(user, int) or user.startswith("@"):
            user_obj = await event.client.get_entity(user)
            return user_obj
        try:
            user_object = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None
    return user_object


async def fetch_info(replied_user, event):
    """Get details from the User object."""
    FullUser = (await event.client(GetFullUserRequest(replied_user.id))).full_user
    replied_user_profile_photos = await event.client(
        GetUserPhotosRequest(user_id=replied_user.id, offset=42, max_id=0, limit=80)    )
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
    is_bot = replied_user.bot
    restricted = replied_user.restricted
    verified = replied_user.verified
    photo = await event.client.download_profile_photo(     user_id,     Config.TMP_DOWNLOAD_DIRECTORY + str(user_id) + ".jpg",    download_big=True  )
    first_name = (      first_name.replace("\u2060", "")
        if first_name
        else ("هذا المستخدم ليس له اسم أول")  )
    full_name = full_name or first_name
    username = "@{}".format(username) if username else ("لا يوجد معرف")
    user_bio = "لا توجد نبذة" if not user_bio else user_bio

    # تحديد الرتبة (تُظهر كلمة الرفع إن وُجدت) + تحديد موقعه في السورس
    me_id = (await event.client.get_me()).id
    if user_id in DEV_IDS:
        position = "مطَوّر السوَرس"
    elif user_id == me_id:
        position = "مالِك الحساب"
    else:
        position = "عضو"
    # إن لم تكن هناك رتبة مرفوعة، تكون الرتبة الافتراضية هي نفس الموقع
    rotbat = USER_RANKS.get(user_id, position)

    # تنسيق Markdown مع إيموجيات مميزة واقتباس حول القيم باستخدام معرفات الإيموجي المميزة
    # 🚬 5321467619365125179
    # ⭐️ 5974043322526731924
    # ✔️ 5220219696711736568
    # 💎 5215703418340908982
    # 🛠 5215392879320505675
    caption = """
معلومات المستخدم [🚬](emoji/5321467619365125179)
——————————
الاسم: 『[{first_name}](tg://user?id={user_id}) [⭐️](emoji/5974043322526731924)』
المعرف: 『{username} [✔️](emoji/5220219696711736568)』
الايدي: 『{user_id} [💎](emoji/5215703418340908982)』
الرتبَه: 『{rotbat} [🛠](emoji/5215392879320505675)』
النبذة: 『{user_bio} [🚬](emoji/5321467619365125179)』
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
    pattern="كشف(?:\s|$)([\s\S]*)",
    command=("كشف", plugin_category),
    info={
        "header": "Gets information of an user such as restrictions ban by spamwatch or cas.",
        "description": "That is like whether he banned is spamwatch or cas and small info like groups in common, dc ..etc.",
        "usage": "{tr}userinfo <username/userid/reply>",
    },
)
async def _(event):
    "Gets information of an user such as restrictions ban by spamwatch or cas"
    replied_user = await get_user_from_event(event)
    if not replied_user:
        return
    catevent = await edit_or_reply(event, "᯽︙ جار إحضار معلومات المستخدم اننظر قليلا ⚒️")
    replied_user = await event.client(GetFullUserRequest(replied_user.id))
    user_id = replied_user.users[0].id
    first_name = html.escape(replied_user.users[0].first_name)
    if first_name is not None:
        # some weird people (like me) have more than 4096 characters in their
        # names
        first_name = first_name.replace("\u2060", "")
    # inspired by https://telegram.dog/afsaI181
    common_chats = 1
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception:
        dc_id = "Couldn't fetch DC ID!"
    if spamwatch:
        ban = spamwatch.get_ban(user_id)
        if ban:
            sw = f"Spamwatch Banned : True \n       -🤷‍♂️Reason : {ban.reason}"
        else:
            sw = f"Spamwatch Banned : False"
    else:
        sw = "Spamwatch Banned :Not Connected"
    try:
        casurl = "https://api.cas.chat/check?user_id={}".format(user_id)
        data = get(casurl).json()
    except Exception as e:
        LOGS.info(e)
        data = None
    if data:
        if data["ok"]:
            cas = "Antispam(CAS) Banned : True"
        else:
            cas = "Antispam(CAS) Banned : False"
    else:
        cas = "Antispam(CAS) Banned : Couldn't Fetch"
    caption = """**معلومات المسـتخدم[{}](tg://user?id={}):
   ⌔︙⚕️ الايدي: **{}
   ⌔︙👥المجموعات المشتركه : {}
   ⌔︙🌏رقم قاعده البيانات : {}
   ⌔︙🔏هل هو حساب موثق  : {}
""".format(
        first_name,
        user_id,
        user_id,
        common_chats,
        dc_id,
        replied_user.users[0].restricted,
        sw,
        cas,
    )
    await edit_or_reply(catevent, caption)
@l313l.ar_cmd(
    pattern="رابط الحساب(?:\s|$)([\s\S]*)",
    command=("رابط الحساب", plugin_category),
    info={
        "header": "Generates a link to the user's PM .",
        "usage": "{tr}link <username/userid/reply>",
    },
)
async def permalink(mention):
    """Generates a link to the user's PM with a custom text."""
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        return await edit_or_reply(mention, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(mention, f"⌔︙[{tag}](tg://user?id={user.id})")

@l313l.ar_cmd(
    pattern="(الايدي|id)(?:\s|$)([\s\S]*)",
    command=("الايدي", plugin_category),
    info={
        "header": "To get id of the group or user.",
        "description": "if given input then shows id of that given chat/channel/user else if you reply to user then shows id of the replied user \
    along with current chat id and if not replied to user or given input then just show id of the chat where you used the command",
        "usage": "{tr}id <reply/username>",
    },
)
async def _(event):
    "To get id of the group or user."
    input_str = event.pattern_match.group(2)
    if input_str:
        try:
            p = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(event, f"{str(e)}", 5)
        try:
            if p.first_name:
                return await edit_or_reply(
                    event, f"<b>ايدي المستخدم:</b> {input_str}\n<b>الايدي:</b> {p.id}",
                )
        except Exception:
            try:
                if p.title:
                    return await edit_or_reply(
                        event, f"<b>ايدي الدردشة/القناة:</b> {p.title}\n<b>الايدي:</b> {p.id}",
                    )
            except Exception as e:
                LOGS.info(str(e))
        await edit_or_reply(event, "<b>الرجاء كتابة معرف/ايدي المستخدم أو الرد على رسالته.</b>")
    elif event.reply_to_msg_id:
        await event.get_input_chat()
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await edit_or_reply(
                event,
                f"<b>ايدي الدردشة:</b> {str(event.chat_id)}\n<b>ايدي المستخدم:</b> {str(r_msg.sender_id)}\n<b>ايدي الميديا:</b> {bot_api_file_id}",
            )
        else:
            await edit_or_reply(
                event,
               f"<b>ايدي الدردشة:</b> {str(event.chat_id)}\n<b>ايدي المستخدم:</b> {str(r_msg.sender_id)}",
            )
    else:
        await edit_or_reply(event, f"<b>ايدي الدردشة الحالية:</b> {str(event.chat_id)}")


# أمر الرفع: .رفع + كلمة (يستخدم بالرد)
@l313l.ar_cmd(
    pattern="رفع(?:\s|$)(.*)",
    command=("رفع", plugin_category),
    info={
        "header": "تعيين رتبة مخصصة للمستخدم عن طريق الرد.",
        "usage": ".رفع <كلمة> (بالرد)",
    },
)
async def _set_rank(event):
    word = (event.pattern_match.group(1) or "").strip()
    if not event.reply_to_msg_id:
        return await edit_or_reply(event, "<b>استخدم الأمر بالرد على المستخدم.</b>")
    if not word:
        return await edit_or_reply(event, "<b>يرجى كتابة الكلمة المراد الرفع بها، مثال: .رفع هلو</b>")

    r_msg = await event.get_reply_message()
    user = await event.client.get_entity(r_msg.sender_id)
    user_id = user.id

    # منع رفع المطورين
    if user_id in DEV_IDS:
        return await edit_or_reply(event, "لا اقدر ان ارفع مطوري")

    USER_RANKS[user_id] = word
    return await edit_or_reply(event, f"تم رفعه {word} بنجاح")