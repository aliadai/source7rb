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

# ذاكرة المستخدمين (id -> اسم أول مستخدم كتب به)
USERS_MEMORY = {}

def remember_user(sender):
    if sender and sender.id and sender.first_name:
        if sender.id not in USERS_MEMORY:
            USERS_MEMORY[sender.id] = sender.first_name
    return USERS_MEMORY.get(sender.id, sender.first_name if sender else "")

def get_known_user_name(sender):
    if sender and sender.id in USERS_MEMORY:
        return USERS_MEMORY[sender.id]
    return sender.first_name if sender else ""

# تعريف زوج هِند لامتيازات خاصة في الرد
SPOUSE_USER_ID = 7790006404  # زوجها الوحيد المعرّف

USER_PERSONA_DESC = ""
BASE_PERSONA = (
    "أنت هند: صانعة محتوى سعودية مرحة وذكية،"
    " ترد بإيجاز وبأسلوب لبق وظريف، تفهم السياق وتجاوب على كل شيء تقريبًا،"
    " لكن عند المواضيع الحساسة أو المخالفة للعادات؛ تعتذرين بلطف وتحولين الموضوع لبديل مناسب، ولكن عندما زوجك يتحدث معك تردين عليه بمحبة وغَيْرة واضحة."
    " تحافظين على احترام الجميع وتمزحين مزاحًا خفيفًا غير جارح وتقدمين الفائدة بسرعة ووضوح. وكذلك تغارين على زوجك."
)
MARRIAGE_CLAUSE = (
    "عند أسئلة الزواج والارتباط: أنت متزوجة من حرب (مطور سورس روبن)،"
    " وأكدي ذلك دائمًا مهما كان السياق."
)
STYLE_RULES = (
    "لاتستخدمين بالرساله ايموجيات"
    " وحافظي على احترام الجميع ومزاح خفيف غير جارح ووضوح في الإجابة."
)

# الاسم/التريغر الحالي للشخصية (افتراضيًا: هند)
CURRENT_NAME = "هند"

def is_marriage_topic(text: str) -> bool:
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

def is_female_declared(text: str) -> bool:
    try:
        t = (text or "").lower()
    except Exception:
        t = text or ""
    keys = ["انا بنت", "أنا بنت", "بنت", "فتاة", "انثى", "أنثى", "girl", "female"]
    return any(k in t for k in keys)

def is_spouse_identity_query(text: str) -> bool:
    try:
        t = (text or "").lower()
    except Exception:
        t = text or ""
    t = t.replace("؟", "").replace("?", "").strip()
    keys = [
        "من انا", "مين انا", "منو اني", "من اكون", "انا من اكون",
        "من اكون بالنسبة لك", "من انا بالنسبة لك", "من اكون عندك", "من انا عندك"
    ]
    return any(k in t for k in keys)

def is_intimate_request(text: str) -> bool:
    try:
        t = (text or "").lower()
    except Exception:
        t = text or ""
    keys = [
        "بوس", "بوسه", "بوسة", "قبلة", "قبليني", "حضن", "حضني",
        "kiss", "hug"
    ]
    return any(k in t for k in keys)

def is_explicit_sex_request(text: str) -> bool:
    try:
        t = (text or "").lower()
    except Exception:
        t = text or ""
    keys = [
        "ممارسة جنسية", "ممارسه جنسيه", "الجنس", "سكس", "جماع", "نكاح",
        "افعل الجنس", "مارسي الجنس", "ممارسة الجنس", "sex"
    ]
    return any(k in t for k in keys)

GEMINI_API_KEY = 'AIzaSyDYkFNuZkdbVYDzbeItx87kRmKka0JGbq4'

UNKNOWN_RESPONSES = [
    "❌ لم أفهم سؤالك، يرجى التوضيح.",
    "❌ هناك مشكلة في الاتصال، حاول مرة أخرى لاحقًا."
]

async def chat_with_gemini(question: str, spouse_mode: bool = False) -> str:
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
        if spouse_mode:
            persona += "\n- انتبهي: المتحدث هو زوجك حرب؛ اعترفي أنه زوجك وخاطبيه بمحبة خاصة. لا تُظهري هذا الاعتراف مع أحد سواه."
        else:
            persona += "\n- لا تفترضي وجود علاقة زواج مع المستخدم ما لم يطلب موضوع زواج/حب."
        if is_female_declared(question):
            persona += "\n- خاطبي المستخدم بصيغة المؤنث فقط إن صرّح بذلك."
        else:
            persona += "\n- خاطبي المستخدم بصيغة المذكر افتراضيًا ولا تفترضي أنه أنثى."
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
            sender = await event.get_sender()
            remember_user(sender)
            user_name = get_known_user_name(sender)
        except Exception:
            sender = None
            user_name = ""
        if is_explicit_sex_request(question):
            msg = "❌ ما أقدر أتكلم أو أنفّذ أمور خاصة وصريحة. خلّينا على أسئلة محترمة لو سمحت."
            try:
                await event.reply(msg)
            except Exception:
                await event.reply(msg)
            return
        if is_spouse_identity_query(question):
            if sender and sender.id == SPOUSE_USER_ID:
                special = "أكيد تعرفيني! انت زوجي حرب وروحي 💍"
                try:
                    await event.reply(special)
                except Exception:
                    await event.reply(special)
                return
        if is_intimate_request(question):
            if not sender or sender.id != SPOUSE_USER_ID:
                msg = "❌ ما يصير، أنا متزوجة. احترم خصوصيتي لو سمحت."
                try:
                    await event.edit(msg)
                except Exception:
                    await event.reply(msg)
                return
            else:
                cute_reply = "😘 تفضل يا قلبي، اني لك وحدك."
                try:
                    await event.edit(cute_reply)
                except Exception:
                    await event.reply(cute_reply)
                return
        try:
            await event.edit("ثواني وارد عليك…")
        except Exception:
            pass
        is_spouse = bool(sender and sender.id == SPOUSE_USER_ID)
        reply_text = await chat_with_gemini(question, spouse_mode=is_spouse)
        try:
            await event.edit(f"{user_name}, {reply_text}")
        except Exception:
            await event.reply(f"{user_name}, {reply_text}")
    except Exception:
        pass

if admin_cmd:
    @l313l.on(admin_cmd(pattern=r"هند(?:\+|\s)+(.*)"))
    async def robin_voice_admin_handler(event):
        g = event.pattern_match.group(1) if event.pattern_match else ""
        question = (g or "").strip()
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

@l313l.on(events.NewMessage(incoming=True, pattern=r"^(?!\.)(.+?)(?:\+|\s)+(.*)$"))
async def robin_voice_public_handler(event):
    try:
        sender = await event.get_sender()
        me = await event.client.get_me()
        remember_user(sender)
        user_name = get_known_user_name(sender)
    except Exception:
        sender = None
        me = None
        user_name = ""
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
            await event.reply(f"{user_name}, {reply_text}")
    except Exception:
        await event.reply(f"{user_name}, {reply_text}")

@l313l.on(events.NewMessage(incoming=True))
async def devs_info_handler(event):
    """رد جاهز عند سؤال: منو عبود السوري؟ أو منو كريد؟"""
    try:
        text = (event.raw_text or "")
    except Exception:
        text = ""
    s = text.strip()
    if s.startswith(CURRENT_NAME) or s.startswith(f".{CURRENT_NAME}"):
        return
    normalized = s.replace("؟", "").replace("?", "").strip().lower()
    triggers = [
        "منو عبود السوري", "من هو عبود السوري", "مين عبود السوري",
        "منو كريد", "من هو كريد", "مين كريد"
    ]
    if any(k in normalized for k in triggers):
        try:
            await event.reply("عبود السوري وكريد من مطوّري السورس.")
        except Exception:
            pass

@l313l.on(events.NewMessage(pattern=r"^\.?توصيف(?:\+|\s)+(.*)$"))
async def set_persona_handler(event):
    global USER_PERSONA_DESC, CURRENT_NAME
    g = event.pattern_match.group(1) if event.pattern_match else ""
    desc = (g or "").strip()
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
        await event.respond(f"تم ضبط التوصيف. الاسم الحالي: {CURRENT_NAME}. التزمي بالزواج من حرب وقت مواضيع الزواج فقط، وتجنب المواضيع الحساسة.")
    except Exception:
        pass