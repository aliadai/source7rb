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

GEMINI_API_KEY = 'AIzaSyC9F7-JJ2jHd4SA4Qo90AwzKhrgHBpPn0A'

UNKNOWN_RESPONSES = [
    "❌ لم أفهم سؤالك، يرجى التوضيح.",
    "❌ هناك مشكلة في الاتصال، حاول مرة أخرى لاحقًا."
]

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


@l313l.on(events.NewMessage(pattern=r"^\.روبن(?:\+|\s)+(.*)$"))
async def robin_direct_handler(event):
    g = event.pattern_match.group(1) if event.pattern_match else ""
    question = (g or "").strip()
    if not question:
        try:
            await event.edit("اكتب سؤالك بعد روبن مثل: .روبن+شنو معنى الحياة؟ أو .روبن شنو معنى الحياة؟")
        except Exception:
            await event.reply("اكتب سؤالك بعد روبن مثل: .روبن+شنو معنى الحياة؟ أو .روبن شنو معنى الحياة؟")
        return
    try:
        await event.edit("ثواني وارد عليك…")
    except Exception:
        pass
    reply_text = await chat_with_gemini(question)
    audio_bytes, mime, source = await synthesize_voice_bytes(reply_text)
    description = (
        f"الصوت: {source}\n"
        f"وصف الصوتية: رد مؤنث لطيف مع لمسة مزاح.\n\n"
        f"النص المقروء:\n{reply_text}"
    )
    try:
        if audio_bytes and mime == "audio/ogg":
            with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as f:
                f.write(audio_bytes)
                path = f.name
            await event.client.send_file(event.chat_id, file=path, voice_note=True, caption=description)
            try:
                os.remove(path)
            except Exception:
                pass
        elif audio_bytes:
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

if admin_cmd:
    @l313l.on(admin_cmd(pattern=r"روبن(?:\+|\s)+(.*)"))
    async def robin_voice_admin_handler(event):
        g = event.pattern_match.group(1) if event.pattern_match else ""
        question = (g or "").strip()
        if not question:
            await event.reply("اكتب سؤالك بعد روبن مثل: روبن شنو معنى الحياة؟ أو روبن+شنو معنى الحياة؟")
            return
        try:
            await event.edit("ثواني وارد عليك…")
        except Exception:
            pass
        reply_text = await chat_with_gemini(question)
        audio_bytes, mime, source = await synthesize_voice_bytes(reply_text)
        description = (
            f"الصوت: {source}\n"
            f"وصف الصوتية: رد مؤنث لطيف مع لمسة مزاح.\n\n"
            f"النص المقروء:\n{reply_text}"
        )
        try:
            if audio_bytes and mime == "audio/ogg":
                with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as f:
                    f.write(audio_bytes)
                    path = f.name
                await event.client.send_file(event.chat_id, file=path, voice_note=True, caption=description)
                try:
                    os.remove(path)
                except Exception:
                    pass
            elif audio_bytes:
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

# مستمع عام لرسائل الجميع بدون نقطة أو معها: "روبن+سؤال" أو "روبن سؤال"
@l313l.on(events.NewMessage(incoming=True, pattern=r"^\.?روبن(?:\+|\s)+(.*)$"))
async def robin_voice_public_handler(event):
    try:
        sender = await event.get_sender()
        me = await event.client.get_me()
    except Exception:
        sender = None
        me = None
    g = event.pattern_match.group(1) if event.pattern_match else ""
    question = (g or "").strip()
    if sender and me and sender.id == me.id:
        if admin_cmd:
            return
        if not question:
            try:
                await event.edit("اكتب سؤالك بعد روبن مثل: روبن شنو معنى الحياة؟ أو روبن+شنو معنى الحياة؟")
            except Exception:
                await event.reply("اكتب سؤالك بعد روبن مثل: روبن شنو معنى الحياة؟ أو روبن+شنو معنى الحياة؟")
            return
        try:
            await event.edit("ثواني وارد عليك…")
        except Exception:
            pass
    else:
        if not question:
            await event.reply("اكتب سؤالك بعد روبن مثل: روبن شنو معنى الحياة؟ أو روبن+شنو معنى الحياة؟")
            return
    reply_text = await chat_with_gemini(question)
    audio_bytes, mime, source = await synthesize_voice_bytes(reply_text)
    description = (
        f"الصوت: {source}\n"
        f"وصف الصوتية: رد مؤنث لطيف مع لمسة مزاح.\n\n"
        f"النص المقروء:\n{reply_text}"
    )
    try:
        if audio_bytes and mime == "audio/ogg":
            with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as f:
                f.write(audio_bytes)
                path = f.name
            if sender and me and sender.id == me.id:
                await event.client.send_file(event.chat_id, file=path, voice_note=True, caption=description)
            else:
                await event.client.send_file(event.chat_id, file=path, voice_note=True, caption=description, reply_to=event.id)
            try:
                os.remove(path)
            except Exception:
                pass
        elif audio_bytes:
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                f.write(audio_bytes)
                path = f.name
            if sender and me and sender.id == me.id:
                await event.client.send_file(event.chat_id, file=path, caption=description)
            else:
                await event.client.send_file(event.chat_id, file=path, caption=description, reply_to=event.id)
            try:
                os.remove(path)
            except Exception:
                pass
        else:
            await event.reply(f"{reply_text}\n\n(ملاحظة: تعذّر إنشاء صوتية الآن)")
    except Exception as e:
        await event.reply(f"حدث خطأ أثناء إرسال الصوتية.\n\n{reply_text}")
