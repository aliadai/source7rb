import re

from telethon import Button, events
from telethon.events import CallbackQuery

from l313l.razan.resources.assistant import *
from l313l.razan.resources.mybot import *
from JoKeRUB import l313l
from ..core import check_owner
from ..Config import Config

JEP_IC = None
ROE = """**مرحباً بك في سورس روبن الشفافة**

**قائمة الأوامر المتاحة:**

**1 - أوامر الإدمن**
**2 - أوامر البوت**
**3 - الحساب**
**4 - المجموعات**
**5 - الصيغ والجهات**
**6 - الحماية وتلكراف**
**7 - أوامر التسلية**
**8 - الترحيبات والردود**
**9 - أوامر المساعدة**
**10 - الملصقات والصور**
**11 - التكرار والتنظيف**
**12 - الترفيه**
**13 - الأكستـرا**
**14 - الانتحال والتقليد**

**اختر الرقم المطلوب من الأزرار أدناه**"""

if Config.TG_BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        await bot.get_me()
        if query.startswith("اوامري") and event.query.user_id == bot.uid:
            buttons = [
                [Button.inline("1", data="l313l0")],
                [
                    Button.inline("2", data="rozbot"),
                    Button.inline("3", data="Jmrz"),
                ],
                [
                    Button.inline("4", data="gro"),
                    Button.inline("5", data="sejrz"),
                ],
                [
                    Button.inline("6", data="grrz"),
                    Button.inline("7", data="tslrzj"),
                ],
                [
                    Button.inline("8", data="r7brz"),
                    Button.inline("9", data="krrznd"),
                ],
                [
                    Button.inline("10", data="jrzst"),
                    Button.inline("11", data="iiers"),
                ],
                [
                    Button.inline("12", data="rfhrz"),
                    Button.inline("13", data="extra"),
                ],
                [
                    Button.inline("14", data="uscuxrz"),
                ],
            ]
            result = builder.article(
                title="سورس روبن الشفافة",
                text=ROE,
                buttons=buttons,
                link_preview=False,
            )
            await event.answer([result] if result else None)


@bot.on(admin_cmd(outgoing=True, pattern="اوامري"))
async def repo(event):
    if event.fwd_from:
        return
    F_O_1 = Config.TG_BOT_USERNAME
    if event.reply_to_msg_id:
        await event.get_reply_message()
    response = await bot.inline_query(F_O_1, "اوامري")
    await response[0].click(event.chat_id)
    await event.delete()


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"l313l0")))
@check_owner
async def _(event):
    buttons = [
    [
      Button.inline("التالي", data="jrzst"),
      Button.inline("القائمة الرئيسية", data="ROE"),]]
    await event.edit(ROZADM, buttons=buttons)

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"jrzst")))
@check_owner
async def _(event):
    butze = [
    [
     Button.inline("التالي", data="tslrzj"),
     Button.inline("رجوع", data="l313l0")]]
    await event.edit(GRTSTI, buttons=butze)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"tslrzj")))
@check_owner
async def _(event):
    buttons = [
    [
     Button.inline("التالي", data="krrznd"),
     Button.inline("رجوع", data="jrzst")]]
    await event.edit(JMAN, buttons=buttons)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"krrznd")))
@check_owner
async def _(event):
    buttons = [
    [
      Button.inline("التالي", data="rozbot"),
      Button.inline("رجوع", data="tslrzj")]]
    await event.edit(TKPRZ, buttons=buttons)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"rozbot")))
@check_owner
async def _(event):
    buttons = [
    [
     Button.inline("التالي", data="Jmrz"),
     Button.inline("رجوع", data="krrznd")]]
    await event.edit(ROZBOT, buttons=buttons)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"Jmrz")))
@check_owner
async def _(event):
    buttons = [
    [
     Button.inline("التالي", data="r7brz"),
     Button.inline("رجوع", data="rozbot")]]
    await event.edit(JROZT, buttons=buttons)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"r7brz")))
@check_owner
async def _(event):
    buttons = [
    [
     Button.inline("التالي", data="sejrz"),
     Button.inline("رجوع", data="Jmrz")]]
    await event.edit(JMTRD, buttons=buttons)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"sejrz")))
@check_owner
async def _(event):
    buttons = [
    [
     Button.inline("التالي", data="gro"),
     Button.inline("رجوع", data="r7brz")]]
    await event.edit(ROZSEG, buttons=buttons)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"gro")))
@check_owner
async def _(event):
    buttons = [
    [
     Button.inline("التالي", data="grrz"),
     Button.inline("رجوع", data="sejrz")]]
    await event.edit(JMGR1,buttons=buttons)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"grrz")))
@check_owner
async def _(event):
    buttons = [
    [
     Button.inline("التالي", data="iiers"),
     Button.inline("رجوع", data="gro")]]
    await event.edit(ROZPRV, buttons=buttons)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"iiers")))
@check_owner
async def _(event):
    buttons = [
    [
     Button.inline("التالي", data="rfhrz"),
     Button.inline("رجوع", data="grrz")]]
    await event.edit(HERP, buttons=buttons)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"rfhrz")))
@check_owner
async def _(event):
    buttons = [
    [
     Button.inline("التالي", data="uscuxrz"),
     Button.inline("رجوع", data="iiers")]]
    await event.edit(T7SHIZ, buttons=buttons)


@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"extra")))
@check_owner
async def _(event):
    buttons = [
    [
     Button.inline("التالي", data="uscuxrz"),
     Button.inline("رجوع", data="rfhrz")]]
    await event.edit(HERP, buttons=buttons)

@l313l.tgbot.on(CallbackQuery(data=re.compile(rb"uscuxrz")))
@check_owner
async def _(event):
    buttons = [[Button.inline("رجوع", data="extra"),]]
    await event.edit(CLORN, buttons=buttons)
