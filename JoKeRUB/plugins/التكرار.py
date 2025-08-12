# By JoKeRUB 2021-2023 - تعديل بواسطة Copilot Chat
import asyncio
import base64
import re
from telethon.tl import functions, types
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.utils import get_display_name
from JoKeRUB import l313l
from telethon import events
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.tools import media_type
from ..helpers.utils import _catutils
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID

yaAli = False
client = l313l
Mukrr = Config.MUKRR_ET or "مكرر"

# دالة التكرار الأساسية
async def spam_function(event, reply_msg, args, sleeptimem, sleeptimet, DelaySpam=False):
    try:
        counter = int(args[0])
    except Exception:
        return await edit_delete(event, "⌔∮ يجب كتابة عدد صحيح لمرات التكرار.")

    # تكرار نص أو رد على رسالة
    if len(args) == 2:
        spam_message = str(args[1])
        for _ in range(counter):
            if gvarstatus("spamwork") is None:
                return
            if event.reply_to_msg_id:
                await reply_msg.reply(spam_message)
            else:
                await event.client.send_message(event.chat_id, spam_message)
            await asyncio.sleep(sleeptimet)
    elif event.reply_to_msg_id and reply_msg.media:
        for _ in range(counter):
            if gvarstatus("spamwork") is None:
                return
            sent = await event.client.send_file(event.chat_id, reply_msg, caption=reply_msg.text)
            await _catutils.unsavegif(event, sent)
            await asyncio.sleep(sleeptimem)
    elif event.reply_to_msg_id and reply_msg.text:
        spam_message = reply_msg.text
        for _ in range(counter):
            if gvarstatus("spamwork") is None:
                return
            await event.client.send_message(event.chat_id, spam_message)
            await asyncio.sleep(sleeptimet)
    else:
        return await edit_delete(event, "⌔∮ يجب كتابة عدد ونص أو الرد على رسالة.")

    # إخطار في بوت لوج
    if BOTLOG:
        msg = f"**⌔∮ تم تنفيذ التكرار بنجاح في الدردشة مع :** {counter} مرات."
        if event.is_private:
            await event.client.send_message(BOTLOG_CHATID, msg)
        else:
            chat_name = get_display_name(await event.get_chat())
            await event.client.send_message(BOTLOG_CHATID, f"{msg} في: {chat_name}")

# أمر .كرر
@l313l.ar_cmd(pattern="كرر(?: |$)(.*)")
async def spammer(event):
    reply_msg = await event.get_reply_message()
    args = event.pattern_match.group(1).split(" ", 1)
    if not args or not args[0].isdigit():
        return await edit_delete(event, "⌔∮ يجب كتابة عدد التكرار ثم النص أو الرد على رسالة.")
    counter = int(args[0])
    sleeptimet = 0.5 if counter > 50 else 0.1
    sleeptimem = 1 if counter > 50 else 0.3
    await event.delete()
    addgvar("spamwork", True)
    await spam_function(event, reply_msg, args, sleeptimem, sleeptimet)

# أمر .مكرر (تكرار مع وقت)
@l313l.on(admin_cmd(pattern=f"{Mukrr} ?(.*)"))
async def mukrr_spam(event):
    reply_msg = await event.get_reply_message()
    args = event.pattern_match.group(1).split(" ", 2)
    if len(args) < 2 or not args[0].isdigit() or not args[1].isdigit():
        return await edit_delete(event, "⌔∮ الصيغة: مكرر <ثواني> <عدد> <نص أو رد>")
    sleeptimet = sleeptimem = int(args[0])
    counter = int(args[1])
    msg = args[2] if len(args) > 2 else ""
    args = [str(counter), msg]
    await event.delete()
    addgvar("spamwork", True)
    await spam_function(event, reply_msg, args, sleeptimem, sleeptimet, DelaySpam=True)

# أمر تكرار الملصق
@l313l.ar_cmd(pattern="تكرار الملصق$")
async def stickerpack_spam(event):
    reply = await event.get_reply_message()
    if not reply or media_type(reply) != "Sticker":
        return await edit_delete(event, "⌔∮ قم بالرد على ملصق لإرسال جميع ملصقات الحزمة.")
    try:
        stickerset_attr = reply.document.attributes[1]
        catevent = await edit_or_reply(event, "⌔∮ جاري إحضار تفاصيل الحزمة...")
    except Exception:
        return await edit_delete(event, "⌔∮ لا يمكن إيجاد الحزمة!")
    try:
        get_stickerset = await event.client(GetStickerSetRequest(
            types.InputStickerSetID(
                id=stickerset_attr.stickerset.id,
                access_hash=stickerset_attr.stickerset.access_hash,
            )
        ))
    except Exception:
        return await edit_delete(event, "⌔∮ لا يمكن جلب الحزمة!")
    reqd_sticker_set = await event.client(
        functions.messages.GetStickerSetRequest(
            stickerset=types.InputStickerSetShortName(
                short_name=get_stickerset.set.short_name
            )
        )
    )
    addgvar("spamwork", True)
    for m in reqd_sticker_set.documents:
        if gvarstatus("spamwork") is None:
            return
        await event.client.send_file(event.chat_id, m)
        await asyncio.sleep(0.7)

# أمر سبام بالحرف
@l313l.ar_cmd(pattern="سبام (.*)")
async def letter_spam(event):
    message = event.pattern_match.group(1).replace(" ", "")
    await event.delete()
    addgvar("spamwork", True)
    for letter in message:
        if gvarstatus("spamwork") is None:
            return
        await event.respond(letter)

# أمر سبام بالكلمة
@l313l.ar_cmd(pattern="وسبام (.*)")
async def word_spam(event):
    message = event.pattern_match.group(1).split()
    await event.delete()
    addgvar("spamwork", True)
    for word in message:
        if gvarstatus("spamwork") is None:
            return
        await event.respond(word)

# أمر إيقاف التكرار
@l313l.ar_cmd(pattern="ايقاف التكرار$")
async def stop_spam(event):
    if gvarstatus("spamwork") is not None:
        delgvar("spamwork")
        return await edit_delete(event, "⌔∮ تم إيقاف التكرار.")
    return await edit_delete(event, "⌔∮ التكرار غير مفعل.")

# دوال النشر الجماعي
async def hrb_nshr(client, sleeptimet, chat, message):
    global yaAli
    yaAli = True
    while yaAli:
        if message.media:
            await client.send_file(chat, message.media, caption=message.text)
        else:
            await client.send_message(chat, message.text)
        await asyncio.sleep(sleeptimet)

@l313l.ar_cmd(pattern="نشر (.*)")
async def group_publish(event):
    await event.delete()
    params = event.pattern_match.group(1).split(" ", 1)
    if len(params) < 2 or not params[0].isdigit():
        return await edit_delete(event, "⌔∮ الصيغة: نشر <ثواني> <usernames...> مع الرد على الرسالة.")
    seconds = int(params[0])
    usernames = params[1].split()
    message = await event.get_reply_message()
    if not message:
        return await edit_delete(event, "⌔∮ يجب الرد على رسالة للنشر.")
    global yaAli
    yaAli = True
    for username in usernames:
        try:
            chat = await event.client.get_entity(username)
            await hrb_nshr(event.client, seconds, chat.id, message)
        except Exception as e:
            await edit_delete(event, f"⌔∮ لا يمكن العثور على المجموعة {username}: {str(e)}")
        await asyncio.sleep(1)

async def hrb_allnshr(client, sleeptimet, message):
    global yaAli
    yaAli = True
    hrb_chats = await client.get_dialogs()
    while yaAli:
        for chat in hrb_chats:
            if chat.is_group and chat.title != "مشتركين 7rB  • Team 7rB ":
                try:
                    if message.media:
                        await client.send_file(chat.id, message.media, caption=message.text)
                    else:
                        await client.send_message(chat.id, message.text)
                except Exception:
                    pass
        await asyncio.sleep(sleeptimet)

@l313l.ar_cmd(pattern="نشر_كروبات (.*)")
async def publish_all_groups(event):
    await event.delete()
    params = event.pattern_match.group(1).split()
    if not params or not params[0].isdigit():
        return await edit_delete(event, "⌔∮ الصيغة: نشر_كروبات <ثواني> مع الرد على رسالة.")
    sleeptimet = int(params[0])
    message = await event.get_reply_message()
    if not message:
        return await edit_delete(event, "⌔∮ يجب الرد على رسالة للنشر.")
    global yaAli
    yaAli = True
    await hrb_allnshr(event.client, sleeptimet, message)

super_groups = ["super", "سوبر"]
async def hrb_supernshr(client, sleeptimet, message):
    global yaAli
    yaAli = True
    hrb_chats = await client.get_dialogs()
    while yaAli:
        for chat in hrb_chats:
            if chat.is_group and any(word in chat.title.lower() for word in super_groups):
                try:
                    if message.media:
                        await client.send_file(chat.id, message.media, caption=message.text)
                    else:
                        await client.send_message(chat.id, message.text)
                except Exception:
                    pass
        await asyncio.sleep(sleeptimet)

@l313l.ar_cmd(pattern="سوبر (.*)")
async def publish_super_groups(event):
    await event.delete()
    params = event.pattern_match.group(1).split()
    if not params or not params[0].isdigit():
        return await edit_delete(event, "⌔∮ الصيغة: سوبر <ثواني> مع الرد على رسالة.")
    sleeptimet = int(params[0])
    message = await event.get_reply_message()
    if not message:
        return await edit_delete(event, "⌔∮ يجب الرد على رسالة للنشر.")
    global yaAli
    yaAli = True
    await hrb_supernshr(event.client, sleeptimet, message)

@l313l.ar_cmd(pattern="ايقاف (النشر|نشر)$")
async def stop_publish(event):
    global yaAli
    yaAli = False
    await event.edit("⌔∮ تم إيقاف النشر التلقائي بنجاح ✓")