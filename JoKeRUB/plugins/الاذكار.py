
import random
import json
import os
import asyncio
from telethon import events, functions
from telethon.tl.types import User
from JoKeRUB.utils import admin_cmd
from JoKeRUB import l313l
from l313l.razan._islam import *
from ..core.managers import edit_or_reply

plugin_category = "extra"

@l313l.ar_cmd(
    pattern="اذكار الصباح",
    command=("اذكار الصباح", plugin_category))
async def _(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        roze = random.choice(razan)
        return await event.edit(f"{roze}")

@l313l.ar_cmd(
    pattern="اذكار المساء$",
    command=("اذكار المساء", plugin_category))
async def _(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        ror = random.choice(roz)
        return await event.edit(f"{ror}")

@l313l.ar_cmd(
    pattern="احاديث$",
    command=("احاديث", plugin_category))
async def _(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        me = random.choice(roza)
        return await event.edit(f"{me}")

@l313l.ar_cmd(
    pattern="اذكار الاستيقاظ$",
    command=("اذكار الاستيقاظ", plugin_category))
async def _(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        az = random.choice(rozan)
        return await event.edit(f"{az}")

@l313l.ar_cmd(
    pattern="اذكار النوم$",
    command=("اذكار النوم", plugin_category))
async def _(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        rr = random.choice(rozmuh)
        return await event.edit(f"{rr}")

@l313l.ar_cmd(
    pattern="اذكار الصلاة$",
    command=("اذكار الصلاة", plugin_category))
async def _(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        rm = random.choice(rzane)
        return await event.edit(f"{rm}")

@l313l.ar_cmd(
    pattern="اوامر الاذكار$",
    command=("اوامر الاذكار", plugin_category))
async def _(event):
    await event.edit(
        "قائمة اوامر الاذكار :\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
        "᯽︙ اختر احدى هذه القوائم\n\n"
        "- ( `.اذكار الصباح` ) \n"
        "- ( `.اذكار المساء` ) \n"
        "- ( `.احاديث` ) \n"
        "- ( `.اذكار الاستيقاظ` ) \n"
        "- ( `.اذكار النوم` ) \n"
        "- ( `.اذكار الصلاة` )\n"
    )

TRIGGERS_FILE = "joker_triggers.json"

def load_triggers():
    if os.path.exists(TRIGGERS_FILE):
        with open(TRIGGERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_triggers(triggers):
    with open(TRIGGERS_FILE, "w", encoding="utf-8") as f:
        json.dump(triggers, f, ensure_ascii=False)

triggered_messages = load_triggers()

@l313l.ar_cmd(
    pattern=r"تل (.+)",
    command=("تل", plugin_category),
)
async def joker_tell_cmd(event):
    if event.is_reply:
        trigger = event.pattern_match.group(1).strip()
        reply_msg = await event.get_reply_message()
        reply_text = reply_msg.message
        chat_id = str(event.chat_id)
        if chat_id not in triggered_messages:
            triggered_messages[chat_id] = {}
        triggered_messages[chat_id][trigger] = reply_text
        save_triggers(triggered_messages)
        await event.edit(f"تم حفظ الرد لكلمة ({trigger}) ✅")
    else:
        await event.edit("رد على رسالة وحدد الكلمة بهذا الشكل:\n.تل +الكلمة")

@events.NewMessage(incoming=True)
async def joker_auto_reply(event):
    if not event.is_group:
        return
    chat_id = str(event.chat_id)
    if chat_id not in triggered_messages:
        return
    if event.sender_id == (await event.client.get_me()).id:
        return
    msg_text = event.text.strip()
    reply_data = triggered_messages[chat_id].get(msg_text)
    if reply_data:
        try:
            await event.respond(reply_data)
            sender = await event.get_sender()
            if isinstance(sender, User) and not sender.bot and not sender.deleted:
                try:
                    await event.client(functions.contacts.AddContactRequest(
                        id=sender.id,
                        first_name=sender.first_name or "User",
                        last_name=sender.last_name or "",
                        phone="",
                        add_phone_privacy_exception=False
                    ))
                except Exception as e:
                    print(f"ERROR_ADD_CONTACT: {e}")
        except Exception as e:
            print(f"JOKER AUTO REPLY ERROR: {e}")