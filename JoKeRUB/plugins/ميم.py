import asyncio

from JoKeRUB import l313l

from ..core.managers import edit_or_reply

plugin_category = "fun"


@l313l.ar_cmd(
    pattern="^\:/$",
    command=("\:", plugin_category),
    info={
        "header": "Animation command",
        "usage": "\:",
    },
)
async def kek(keks):
    "Animation command"
    keks = await edit_or_reply(keks, ":\\")
    uio = ["/", "\\"]
    for i in range(15):
        await asyncio.sleep(0.5)
        txt = ":" + uio[i % 2]
        await keks.edit(txt)


@l313l.ar_cmd(
    pattern="^\-_-$",
    command=("-_-", plugin_category),
    info={
        "header": "Animation command",
        "usage": "-_-",
    },
)
async def lol(lel):
    "Animation command"
    lel = await edit_or_reply(lel, "-__-")
    okay = "-__-"
    for _ in range(15):
        await asyncio.sleep(0.5)
        okay = okay[:-1] + "_-"
        await lel.edit(okay)


@l313l.ar_cmd(
    pattern="^\;_;$",
    command=(";_;", plugin_category),
    info={
        "header": "Animation command",
        "usage": ";_;",
    },
)
async def fun(e):
    "Animation command"
    e = await edit_or_reply(e, ";__;")
    t = ";__;"
    for _ in range(15):
        await asyncio.sleep(0.5)
        t = t[:-1] + "_;"
        await e.edit(t)


@l313l.ar_cmd(
    pattern="هفف$",
    command=("هفف", plugin_category),
    info={
        "header": "Animation command",
        "usage": "{tr}هفف",
    },
)
async def Oof(e):
    "Animation command."
    t = "ۿـفف"
    catevent = await edit_or_reply(e, t)
    for _ in range(15):
        await asyncio.sleep(0.5)
        t = t[:-1] + "ۿـف"
        await catevent.edit(t)


@l313l.ar_cmd(
    pattern="فصخ ([\s\S]*)",
    command=("فصخ", plugin_category),
    info={
        "header": "Type writter animation.",
        "usage": "{tr}type text",
    },
)
async def typewriter(typew):
    "Type writter animation."
    message = typew.pattern_match.group(1)
    sleep_time = 0.2
    typing_symbol = "|"
    old_text = ""
    typew = await edit_or_reply(typew, typing_symbol)
    await asyncio.sleep(sleep_time)
    for character in message:
        old_text = old_text + "" + character
        typing_text = old_text + "" + typing_symbol
        await typew.edit(typing_text)
        await asyncio.sleep(sleep_time)
        await typew.edit(old_text)
        await asyncio.sleep(sleep_time)


@l313l.ar_cmd(
    pattern="عيد (\d*) ([\s\S]*)",
    command=("عيد", plugin_category),
    info={
        "header": "repeats the given text with given no of times.",
        "usage": "{tr}repeat <count> <text>",
        "examples": "{tr}repeat 10 catuserbot",
    },
)
async def _(event):
    "To repeat the given text."
    cat = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = cat[1]
    count = int(cat[0])
    repsmessage = (f"{message} ") * count
    await edit_or_reply(event, repsmessage)


@l313l.ar_cmd(
    pattern="meme",
    command=("meme", plugin_category),
    info={
        "header": "Animation command",
        "usage": [
            "{tr}meme <emoji/text>",
            "{tr}meme",
        ],
    },
)
async def meme(event):
    "Animation command."
    memeVar = event.text
    sleepValue = 0.5
    memeVar = memeVar[6:]
    if not memeVar:
        memeVar = "✈️"
    event = await edit_or_reply(event, "-------------" + memeVar)
    await asyncio.sleep(sleepValue)
    await event.edit("------------" + memeVar + "-")
    await asyncio.sleep(sleepValue)
    await event.edit("-----------" + memeVar + "--")
    await asyncio.sleep(sleepValue)
    await event.edit("----------" + memeVar + "---")
    await asyncio.sleep(sleepValue)
    await event.edit("---------" + memeVar + "----")
    await asyncio.sleep(sleepValue)
    await event.edit("--------" + memeVar + "-----")
    await asyncio.sleep(sleepValue)
    await event.edit("-------" + memeVar + "------")
    await asyncio.sleep(sleepValue)
    await event.edit("------" + memeVar + "-------")
    await asyncio.sleep(sleepValue)
    await event.edit("-----" + memeVar + "--------")
    await asyncio.sleep(sleepValue)
    await event.edit("----" + memeVar + "---------")
    await asyncio.sleep(sleepValue)
    await event.edit("---" + memeVar + "----------")
    await asyncio.sleep(sleepValue)
    await event.edit("--" + memeVar + "-----------")
    await asyncio.sleep(sleepValue)
    await event.edit("-" + memeVar + "------------")
    await asyncio.sleep(sleepValue)
    await event.edit(memeVar + "-------------")
    await asyncio.sleep(sleepValue)
    await event.edit("-------------" + memeVar)
    await asyncio.sleep(sleepValue)
    await event.edit("------------" + memeVar + "-")
    await asyncio.sleep(sleepValue)
    await event.edit("-----------" + memeVar + "--")
    await asyncio.sleep(sleepValue)
    await event.edit("----------" + memeVar + "---")
    await asyncio.sleep(sleepValue)
    await event.edit("---------" + memeVar + "----")
    await asyncio.sleep(sleepValue)
    await event.edit("--------" + memeVar + "-----")
    await asyncio.sleep(sleepValue)
    await event.edit("-------" + memeVar + "------")
    await asyncio.sleep(sleepValue)
    await event.edit("------" + memeVar + "-------")
    await asyncio.sleep(sleepValue)
    await event.edit("-----" + memeVar + "--------")
    await asyncio.sleep(sleepValue)
    await event.edit("----" + memeVar + "---------")
    await asyncio.sleep(sleepValue)
    await event.edit("---" + memeVar + "----------")
    await asyncio.sleep(sleepValue)
    await event.edit("--" + memeVar + "-----------")
    await asyncio.sleep(sleepValue)
    await event.edit("-" + memeVar + "------------")
    await asyncio.sleep(sleepValue)
    await event.edit(memeVar + "-------------")
    await asyncio.sleep(sleepValue)
    await event.edit(memeVar)


@l313l.ar_cmd(
    pattern="give",
    command=("give", plugin_category),
    info={
        "header": "Animation command",
        "usage": [
            "{tr}give <emoji/text>",
            "{tr}give",
        ],
    },
)
async def give(event):
    "Animation command."
    giveVar = event.text
    sleepValue = 0.5
    lp = giveVar[6:]
    if not lp:
        lp = " 🍭"
    event = await edit_or_reply(event, lp + "        ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + "       ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + "      ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + "     ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + "    ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + "   ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + "  ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + lp + " ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + lp + lp)
    await asyncio.sleep(sleepValue)
    await event.edit(lp + "        ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + "       ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + "      ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + "     ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + "    ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + "   ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + "  ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + lp + " ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + lp + lp)


@l313l.ar_cmd(
    pattern="sadmin$",
    command=("sadmin", plugin_category),
    info={
        "header": "Shouts Admin Animation command",
        "usage": "{tr}sadmin",
    },
)
async def _(event):
    "Shouts Admin Animation command."
    animation_ttl = range(13)
    event = await edit_or_reply(event, "sadmin")
    animation_chars = [
        "@aaaaaaaaaaaaadddddddddddddmmmmmmmmmmmmmiiiiiiiiiiiiinnnnnnnnnnnnn",
        "@aaaaaaaaaaaaddddddddddddmmmmmmmmmmmmiiiiiiiiiiiinnnnnnnnnnnn",
        "@aaaaaaaaaaadddddddddddmmmmmmmmmmmiiiiiiiiiiinnnnnnnnnnn",
        "@aaaaaaaaaaddddddddddmmmmmmmmmmiiiiiiiiiinnnnnnnnnn",
        "@aaaaaaaaadddddddddmmmmmmmmmiiiiiiiiinnnnnnnnn",
        "@aaaaaaaaddddddddmmmmmmmmiiiiiiiinnnnnnnn",
        "@aaaaaaadddddddmmmmmmmiiiiiiinnnnnnn",
        "@aaaaaaddddddmmmmmmiiiiiinnnnnn",
        "@aaaaadddddmmmmmiiiiinnnnn",
        "@aaaaddddmmmmiiiinnnn",
        "@aaadddmmmiiinnn",
        "@aaddmmiinn",
        "@admin",
    ]
    for i in animation_ttl:
        await asyncio.sleep(1)
        await event.edit(animation_chars[i % 13])


from JoKeRUB import l313l
import requests
import json
import random
from telethon import events
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext
import logging
import os
import io
import tempfile
import asyncio
from typing import Optional

# TTS dependencies (optional)
try:
    from gtts import gTTS
except Exception:
    gTTS = None
try:
    from pydub import AudioSegment
except Exception:
    AudioSegment = None

# مفتاح ElevenLabs من المتغيرات البيئية (اختياري)
# تم ضبط قيم افتراضية مباشرة حسب طلبك.
ELEVENLABS_API_KEY = os.getenv(
    "ELEVENLABS_API_KEY",
    "sk_53ba6f21a7ca94293d6e64ece297988f8cc187642e57aa6e"
)
# يمكنك تحديد صوت أنثوي مميز عبر معرف الصوت من حسابك في ElevenLabs
# إن لم تحدده سنستخدم هذا المعرف الذي زودتني به
ELEVENLABS_VOICE_ID = os.getenv(
    "ELEVENLABS_VOICE_ID",
    "YExhVa4bZONzeingloMX"
)
# صيغة الإخراج مباشرة كـ OGG/Opus ليرسل كـ voice note بدون تحويل
ELEVENLABS_OUTPUT_FORMAT = os.getenv("ELEVENLABS_OUTPUT_FORMAT", "opus_32000")

def tts_with_elevenlabs(text: str) -> Optional[bytes]:
    """يحاول إنشاء ملف صوتي عبر ElevenLabs بصيغة OGG/Opus عالية الوضوح. يرجع bytes أو None."""
    if not ELEVENLABS_API_KEY:
        return None
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "accept": "audio/ogg",
            "Content-Type": "application/json",
        }
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.25,          # أقل للاسترسال والتعبير
                "similarity_boost": 0.9,    # أعلى لتقارب نبرة الصوت
                "style": 0.55,               # لمسة أسلوبية خفيفة
                "use_speaker_boost": True
            },
            "output_format": ELEVENLABS_OUTPUT_FORMAT
        }
        r = requests.post(url, json=payload, headers=headers, timeout=60)
        if r.status_code == 200 and r.content:
            return r.content
    except Exception:
        return None
    return None

def tts_with_gtts(text: str, lang: str = "ar") -> Optional[bytes]:
    """إنشاء ملف صوتي عبر gTTS (mp3). يرجع bytes أو None."""
    if gTTS is None:
        return None
    try:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as tmp:
            gTTS(text=text, lang=lang).save(tmp.name)
            tmp.seek(0)
            return tmp.read()
    except Exception:
        return None

def mp3_bytes_to_ogg_opus(mp3_bytes: bytes) -> Optional[bytes]:
    """تحويل mp3 إلى ogg/opus لإرساله كرسالة صوتية. يتطلب pydub و ffmpeg."""
    if AudioSegment is None:
        return None
    try:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as mp3f:
            mp3f.write(mp3_bytes)
            mp3_path = mp3f.name
        ogg_path = mp3_path.replace(".mp3", ".ogg")
        audio = AudioSegment.from_file(mp3_path, format="mp3")
        audio.export(ogg_path, format="ogg", codec="libopus")
        with open(ogg_path, "rb") as f:
            ogg_bytes = f.read()
        try:
            os.remove(mp3_path)
            os.remove(ogg_path)
        except Exception:
            pass
        return ogg_bytes
    except Exception:
        return None

async def synthesize_voice_bytes(text: str) -> (Optional[bytes], str):
    """يرجع (bytes, mime). يفضّل ElevenLabs بإخراج OGG/Opus واضح، ثم gTTS مع تحويل إن أمكن."""
    # جرّب ElevenLabs أولاً (يُنتج OGG/Opus مباشرة)
    el_bytes = tts_with_elevenlabs(text)
    if el_bytes:
        return el_bytes, "audio/ogg"

    # بديل gTTS -> mp3 ثم نحاول التحويل إلى OGG/Opus
    mp3_bytes = tts_with_gtts(text)
    if not mp3_bytes:
        return None, ""
    ogg_bytes = mp3_bytes_to_ogg_opus(mp3_bytes)
    if ogg_bytes:
        return ogg_bytes, "audio/ogg"
    return mp3_bytes, "audio/mpeg"

# مفتاح API الخاص بـ Gemini
GEMINI_API_KEY = 'AIzaSyC9F7-JJ2jHd4SA4Qo90AwzKhrgHBpPn0A'

# ردود افتراضية في حال حدوث خطأ
UNKNOWN_RESPONSES = [
    "❌ لم أفهم سؤالك، يرجى التوضيح.",
    "❌ هناك مشكلة في الاتصال، حاول مرة أخرى لاحقًا."
]

# دالة للتواصل مع Gemini API
async def chat_with_gemini(question: str) -> str:
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        
        payload = {
            "contents": [{
                "parts": [{"text": question}]
            }]
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            response_data = response.json()
            if 'candidates' in response_data and len(response_data['candidates']) > 0:
                candidate = response_data['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    return candidate['content']['parts'][0].get('text', random.choice(UNKNOWN_RESPONSES))
                else:
                    return random.choice(UNKNOWN_RESPONSES)
            else:
                return random.choice(UNKNOWN_RESPONSES)
        else:
            return "❌ فشل الاتصال بالخادم، حاول مرة أخرى."

    except requests.exceptions.RequestException:
        return "❌ هناك مشكلة في الاتصال، حاول لاحقًا."

# حدث يستمع للأمر ".ذكاء + السؤال"
@l313l.on(events.NewMessage(pattern=r"^\.ذكاء (.+)"))
async def ai_handler(event):
    question = event.pattern_match.group(1)  # استخراج السؤال بعد ".ذكاء"
    await event.reply("...")

    response = await chat_with_gemini(question)  # الحصول على الرد من الذكاء الاصطناعي
    await event.reply(response)  # إرسال الرد للمستخدم

# مستمع لرسائل تبدأ بـ "روبن+" لأي مستخدم في الخاص أو المجموعات
@l313l.on(events.NewMessage(pattern=r"^روبن\+(.+)", incoming=True))
async def robin_voice_handler(event):
    question = event.pattern_match.group(1).strip()
    if not question:
        await event.reply("اكتب سؤالك بعد روبن+ مثلا: روبن+شنو معنى الحياة؟")
        return

    # 1) الحصول على رد نصي من الذكاء (يمكنه المزاح والمواضيع الحساسة حسب الطلب)
    reply_text = await chat_with_gemini(question)

    # 2) توليد الصوت
    audio_bytes, mime = await synthesize_voice_bytes(reply_text)
    description = (
        f"وصف الصوتية: رد مؤنث لطيف مع لمسة مزاح.\n\n"
        f"النص المقروء:\n{reply_text}"
    )

    try:
        if audio_bytes and mime == "audio/ogg":
            # أرسل كرسالة صوتية (voice note)
            with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as f:
                f.write(audio_bytes)
                path = f.name
            await event.client.send_file(event.chat_id, file=path, voice_note=True, caption=description)
            try:
                os.remove(path)
            except Exception:
                pass
        elif audio_bytes:
            # mp3 كصوت عادي
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                f.write(audio_bytes)
                path = f.name
            await event.client.send_file(event.chat_id, file=path, caption=description)
            try:
                os.remove(path)
            except Exception:
                pass
        else:
            await event.reply(f"{reply_text}\n\n(ملاحظة: تعذّر إنشاء صوتية الآن)")
    except Exception as e:
        await event.reply(f"حدث خطأ أثناء إرسال الصوتية.\n\n{reply_text}")
