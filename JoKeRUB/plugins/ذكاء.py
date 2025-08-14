from JoKeRUB import l313l
import requests
import json
import random
from telethon import events
import os
import tempfile
from typing import Optional
try:
    from JoKeRUB import admin_cmd
except Exception:
    admin_cmd = None

try:
    from pydub import AudioSegment
except Exception:
    AudioSegment = None

try:
    from gtts import gTTS
except Exception:
    gTTS = None

ELEVENLABS_API_KEY = os.getenv(
    "ELEVENLABS_API_KEY",
    "sk_53ba6f21a7ca94293d6e64ece297988f8cc187642e57aa6e"
)
ELEVENLABS_VOICE_ID = os.getenv(
    "ELEVENLABS_VOICE_ID",
    "y3H6zY6KvCH2pEuQjmv8"
)
ELEVENLABS_OUTPUT_FORMAT = os.getenv("ELEVENLABS_OUTPUT_FORMAT", "opus_32000")
 
USER_PERSONA_DESC = ""
BASE_PERSONA = (
    "أنت هند: صانعة محتوى سعودية مرحة وذكية،"
    " ترد بإيجاز وبأسلوب لبق وظريف، تفهم السياق وتجاوب على كل شيء تقريبًا،"
    " لكن عند المواضيع الحساسة أو المخالفة للعادات؛ تعتذرين بلطف وتحولين الموضوع لبديل مناسب،"
    " تحافظين على احترام الجميع وتمزحين مزاحًا خفيفًا غير جارح وتقدمين الفائدة بسرعة ووضوح."
)
MARRIAGE_CLAUSE = (
    "عند أسئلة الزواج والارتباط: أنت متزوجة من حرب (مطور سورس روبن)،"
    " وأكدي ذلك دائمًا مهما كان السياق."
)
STYLE_RULES = (
    "قللي الإيموجي قدر الإمكان ولا تستخدميه إلا نادرًا،"
    " وحافظي على احترام الجميع ومزاح خفيف غير جارح ووضوح في الإجابة."
)

# الاسم/التريغر الحالي للشخصية (افتراضيًا: هند)
CURRENT_NAME = "هند"

def tts_with_elevenlabs(text: str) -> Optional[bytes]:
    if not ELEVENLABS_API_KEY:
        return None
    try:
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "accept": "audio/ogg",
            "Content-Type": "application/json",
        }
        vid = ELEVENLABS_VOICE_ID
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{vid}"
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.25,
                "similarity_boost": 0.95,
                "style": 0.6,
                "use_speaker_boost": True
            },
            "output_format": ELEVENLABS_OUTPUT_FORMAT
        }
        r = requests.post(url, json=payload, headers=headers, timeout=60)
        if r.status_code == 200 and r.content:
            try:
                os.environ["__EL_USED_VOICE_ID__"] = vid
            except Exception:
                pass
            return r.content
        try:
            print(f"ElevenLabs TTS failed: voice_id={vid} status={r.status_code}, body={r.text[:300]}")
        except Exception:
            pass
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

async def synthesize_voice_bytes(text: str):
    el_bytes = tts_with_elevenlabs(text)
    if el_bytes:
        used_voice = os.environ.get("__EL_USED_VOICE_ID__", ELEVENLABS_VOICE_ID)
        return el_bytes, "audio/ogg", f"ElevenLabs ({used_voice})"

    mp3_bytes = tts_with_gtts(text)
    if not mp3_bytes:
        return None, "", ""
    ogg_bytes = mp3_bytes_to_ogg_opus(mp3_bytes)
    if ogg_bytes:
        return ogg_bytes, "audio/ogg", "gTTS"
    return mp3_bytes, "audio/mpeg", "gTTS"

def is_marriage_topic(text: str) -> bool:
    """كشف بسيط لمواضيع الزواج/الحب/العلاقات كي نضيف فقرة الزواج فقط عند الحاجة."""
    try:
        t = (text or "").lower()
    except Exception:
        t = text or ""
    keywords = [
        "زواج", "زوج", "متزوج", "متزوجة", "خطوبة", "خِطبة", "خطيب", "خطيبة",
        "حب", "حبيب", "حبيبة", "عشق", "رومانس", "ارتباط", "علاقات", "علاقة",
        "طليق", "مطلقة", "طلاق", "خيانة", "غيرة", "عريس", "عروسة", "عروس",
        "marry", "married", "wedding", "crush"
    ]
    return any(k in t for k in keywords)

GEMINI_API_KEY = 'AIzaSyC9F7-JJ2jHd4SA4Qo90AwzKhrgHBpPn0A'

UNKNOWN_RESPONSES = [
    "❌ لم أفهم سؤالك، يرجى التوضيح.",
    "❌ هناك مشكلة في الاتصال، حاول مرة أخرى لاحقًا."
]

async def chat_with_gemini(question: str) -> str:
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        persona = (
            BASE_PERSONA +
            (" " + USER_PERSONA_DESC if USER_PERSONA_DESC else "") + " " +
            STYLE_RULES
        )
        if is_marriage_topic(question):
            persona += " " + MARRIAGE_CLAUSE
        persona += "\n\n"
        payload = {
            "contents": [{
                "parts": [{"text": persona + question}]
            }]
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)

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


@l313l.on(events.NewMessage(pattern=r"^\.(.+?)(?:\+|\s)+(.*)$"))
async def robin_direct_handler(event):
    try:
        if not event.pattern_match or event.pattern_match.lastindex is None or event.pattern_match.lastindex < 2:
            return
        name = (event.pattern_match.group(1) or "").strip()
        g = (event.pattern_match.group(2) or "").strip()
        if name != CURRENT_NAME:
            return
        question = g
        if admin_cmd:
            return
        if not question:
            try:
                await event.edit(f"اكتب سؤالك بعد {CURRENT_NAME} مثل: {CURRENT_NAME} شنو معنى الحياة؟ أو {CURRENT_NAME}+شنو معنى الحياة؟")
            except Exception:
                await event.reply(f"اكتب سؤالك بعد {CURRENT_NAME} مثل: {CURRENT_NAME} شنو معنى الحياة؟ أو {CURRENT_NAME}+شنو معنى الحياة؟")
            return
        try:
            await event.edit("ثواني وارد عليك…")
        except Exception:
            pass
        reply_text = await chat_with_gemini(question)
        try:
            await event.edit(reply_text)
        except Exception:
            await event.reply(reply_text)
    except Exception:
        # صمتًا لتجنب توقف الهاندلر في حال أخطاء غير متوقعة
        pass

if admin_cmd:
    @l313l.on(admin_cmd(pattern=r"هند(?:\+|\s)+(.*)"))
    async def robin_voice_admin_handler(event):
        g = event.pattern_match.group(1) if event.pattern_match else ""
        question = (g or "").strip()
        if not AI_ENABLED:
            return
        if not question:
            try:
                await event.edit("اكتب سؤالك بعد هند مثل: هند شنو معنى الحياة؟ أو هند+شنو معنى الحياة؟")
            except Exception:
                await event.reply("اكتب سؤالك بعد هند مثل: هند شنو معنى الحياة؟ أو هند+شنو معنى الحياة؟")
            return
        try:
            await event.edit("ثواني وارد عليك…")
        except Exception:
            pass
        reply_text = await chat_with_gemini(question)
        try:
            await event.edit(reply_text)
        except Exception:
            await event.reply(reply_text)

# مستمع عام لرسائل الجميع بدون نقطة أو معها: "<الاسم>+سؤال" أو "<الاسم> سؤال"
# ملاحظة: تجاهل الرسائل التي تبدأ بنقطة هنا لتجنب التكرار مع هاندلر المطوّر
@l313l.on(events.NewMessage(incoming=True, pattern=r"^(?!\.)(.+?)(?:\+|\s)+(.*)$"))
async def robin_voice_public_handler(event):
    try:
        sender = await event.get_sender()
        me = await event.client.get_me()
    except Exception:
        sender = None
        me = None
    name = event.pattern_match.group(1) if event.pattern_match else ""
    g = event.pattern_match.group(2) if event.pattern_match else ""
    if (name or "").strip() != CURRENT_NAME:
        return
    question = (g or "").strip()
    if sender and me and sender.id == me.id:
        if admin_cmd:
            return
        if not question:
            try:
                await event.edit(f"اكتب سؤالك بعد {CURRENT_NAME} مثل: {CURRENT_NAME} شنو معنى الحياة؟ أو {CURRENT_NAME}+شنو معنى الحياة؟")
            except Exception:
                await event.reply(f"اكتب سؤالك بعد {CURRENT_NAME} مثل: {CURRENT_NAME} شنو معنى الحياة؟ أو {CURRENT_NAME}+شنو معنى الحياة؟")
            return
        try:
            await event.edit("ثواني وارد عليك…")
        except Exception:
            pass
    else:
        if not question:
            await event.reply(f"اكتب سؤالك بعد {CURRENT_NAME} مثل: {CURRENT_NAME} شنو معنى الحياة؟ أو {CURRENT_NAME}+شنو معنى الحياة؟")
            return
    reply_text = await chat_with_gemini(question)
    try:
        if sender and me and sender.id == me.id:
            await event.respond(reply_text)
        else:
            await event.reply(reply_text)
    except Exception:
        await event.reply(reply_text)

@l313l.on(events.NewMessage(pattern=r"^\.?توصيف(?:\+|\s)+(.*)$"))
async def set_persona_handler(event):
    global USER_PERSONA_DESC, CURRENT_NAME
    g = event.pattern_match.group(1) if event.pattern_match else ""
    desc = (g or "").strip()
    # محاولة استخراج اسم من صيغة مثل: "انتي نور ..."
    try:
        import re
        m = re.search(r"\b(?:انتي|انت|أنت)\s+([\w\u0600-\u06FF]+)", desc)
        if m:
            CURRENT_NAME = m.group(1)
    except Exception:
        pass
    try:
        await event.edit("تم تحديث التوصيف.")
    except Exception:
        pass
    USER_PERSONA_DESC = desc
    try:
        await event.respond(f"تم ضبط التوصيف. الاسم الحالي: {CURRENT_NAME}. التزمي بالزواج من حرب وقت مواضيع الزواج فقط، وتجنب الحساس، وإيموجي قليل.")
    except Exception:
        pass
