import random
import re
import time
from platform import python_version

from telethon import version, Button, events
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon.events import CallbackQuery

from JoKeRUB import StartTime, l313l, JEPVERSION

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import catalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import mention

plugin_category = "utils"

@l313l.ar_cmd(
    pattern="المطور$",
    command=("المطور", plugin_category),
    info={
        "header": "لأظهار مطورين السورس",
        "usage": [
            "{tr}المطور",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details"
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    EMOJI = gvarstatus("ALIVE_EMOJI") or "  - "
    CUSTOM_ALIVE_TEXT = gvarstatus("ALIVE_TEXT")
    
    cat_caption = f"**🔰 مطورين سورس Robin 🔰**\n\n"
    cat_caption += f"━━━━━━━━━━━━━━━━━━━━━\n"
    cat_caption += f"👨‍💻 **المطور الأول** : @is7rB\n"
    cat_caption += f"👨‍💻 **المطور الثاني** : @this7rB\n"
    cat_caption += f"━━━━━━━━━━━━━━━━━━━━━\n"
    cat_caption += f"📢 **قناة السورس** : @RobinSource\n"
    cat_caption += f"━━━━━━━━━━━━━━━━━━━━━"
    await event.reply(cat_caption, reply_to=reply_to_id)

@l313l.tgbot.on(CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await catalive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)

progs = [1374312239, 393120911, 7182427468, 5564802580, 7790006404]

@l313l.on(events.NewMessage(incoming=True))
async def reda(event):
    if event.reply_to and event.sender_id in progs:
       reply_msg = await event.get_reply_message()
       owner_id = reply_msg.from_id.user_id
       if owner_id == l313l.uid:
           if event.message.message == "بلوك من السورس":
               await event.reply("**حاظر مطوري ، لقد تم حظره من استخدام السورس**")
               addgvar("blockedfrom", "yes")
           elif event.message.message == "الغاء البلوك من السورس":
               await event.reply("**حاظر مطوري، لقد الغيت البلوك**")
               delgvar("blockedfrom")
                
