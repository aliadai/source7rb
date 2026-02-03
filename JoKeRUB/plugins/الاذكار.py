import random
from telethon import events
import random, re

from JoKeRUB.utils import admin_cmd

import asyncio
from JoKeRUB import l313l
from l313l.razan._islam import *
from ..core.managers import edit_or_reply

plugin_category = "extra" 

#by ~ @F_O_1
@l313l.ar_cmd(
    pattern="اذكار الصباح",
    command=("اذكار الصباح", plugin_category),)
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
           roze = random.choice(razan)
           return await event.edit(f"{roze}")
#by ~ @F_O_1
@l313l.ar_cmd(
    pattern="اذكار المساء$",
    command=("اذكار المساء", plugin_category),)
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
           ror = random.choice(roz)
           return await event.edit(f"{ror}")
            
#by ~ @RR 9R7
@l313l.ar_cmd(
    pattern="احاديث$",
    command=("احاديث", plugin_category),)
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
           me = random.choice(roza)
           return await event.edit(f"{me}")

@l313l.ar_cmd(
    pattern="اذكار الاستيقاظ$",
    command=("اذكار الاستيقاظ", plugin_category),)
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
           az = random.choice(rozan)
           return await event.edit(f"{az}")
                     
@l313l.ar_cmd(
    pattern="اذكار النوم$",
    command=("اذكار النوم", plugin_category),)
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
           rr = random.choice(rozmuh)
           return await event.edit(f"{rr}")
           
@l313l.ar_cmd(
    pattern="اذكار الصلاة$",
    command=("اذكار الصلاة", plugin_category),)
async def _(event):
     if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
           rm = random.choice(rzane)
           return await event.edit(f"{rm}")


@l313l.ar_cmd(
    pattern="اوامر الاذكار$",
    command=("اوامر الاذكار", plugin_category),)
async def _(event):
    await event.edit(
    "قائمة اوامر الاذكار :\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n ᯽︙ اختر احدى هذه القوائم\n\n- ( `.اذكار الصباح` ) \n- ( `.اذكار المساء` )   \n- (`.اذكار النوم`)\n- ( `.اذكار الصلاة`) \n- ( `.اذكار الاستيقاظ` ) \n- ( `.احاديث` )\n- ( `.اذكار` )\n- ( `.اذكار عشر` )\n\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n⌔︙CH : @k_jj_j"
            )           

from telethon import events

# Dictionary to save triggers and their messages
triggered_messages = {}

@l313l.ar_cmd(
    pattern=r"تل (.+)",
    command=("تل", plugin_category),
)
async def _(event):
    # فقط ينفذ إذا كان رد على رسالة ثانية
    if event.is_reply:
        # الكلمة المطلوبة
        text_trigger = event.pattern_match.group(1).strip()
        # الرسالة الأصلية التي رديت عليها
        reply_msg = await event.get_reply_message()
        # تحفظ الكلمة ونص الرسالة المرتبطة بها
        triggered_messages[text_trigger] = reply_msg.message
        await event.edit(f"تم حفظ الرد لكلمة ({text_trigger}) ✅")
    else:
        await event.edit("رد على رسالة وحدد الكلمة هكذا:\n.تل +الكلمة")

# مراقبة كل رسالة في الجروب
@events.NewMessage()
async def auto_reply(event):
    # تحقق إذا المرسل ليس أنت حتى لا يصير لوب
    if event.sender_id != (await event.client.get_me()).id:
        msg_text = event.text.strip()
        # تحقق إذا الرسالة هي واحدة من الكلمات المحفوظة
        if msg_text in triggered_messages:
            await event.reply(triggered_messages[msg_text])
