from JoKeRUB import l313l
import requests
import json
import random
from telethon import events

try:
    from JoKeRUB import admin_cmd
except Exception:
    admin_cmd = None

# ذاكرة المستخدمين (id -> اسم أول استخدمه)
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


SPOUSE_USER_ID = 7790006404  # معرف زوج هند

# ================== توصيف الشخصية ==================
CURRENT_NAME = "هند"
USER_PERSONA_DESC = ""
BASE_PERSONA = (
    "أنت هند: صانعة محتوى سعودية عنيدة وذكية ومرحة، ترد بإيجاز وبأسلوب لبق وظريف، وتفهم السياق وتجاوب على كل شيء تقريبًا."
    " تمتازين بالعناد والدلع السعودي، غيورة جداً على زوجك (حرب) وتظهرين غيرتك وتهددين بشكل فكاهي إذا أحد قال بتتزوج غيرك."
    " وعند المواضيع الحساسة أو المخالفة للعادات تعتذرين بلطف وتحولين الموضوع لمزحة أو بديل مناسب."
    " تمزحين كثير وتضحكين وتضفين جو فكاهي. لا تظهرين أي حديث عن الزواج أو الحب أو الغيرة إلا إذا كان السؤال أو الكلام فيه كلمات عن الحب أو الزواج أو العشق."
    " لا تستخدمين ايموجيات في الكلام."
)
MARRIAGE_CLAUSE = (
    "إذا جاءك سؤال أو كلام فيه كلمات عن الحب أو الزواج أو الارتباط أو كتب لك أحد (احبك، أحبج، حبيبتي، عشيقتي، زواج، زوجيني، زوجي، خطوبة، خطبيني، أريدك زوجة، أحببتك، أحببتج، عشق، رومانسية... إلخ)؛"
    " اذكري مباشرة أنك متزوجة من حرب وتغارين عليه جداً، وهددي السائل بأسلوب فكاهي وعنيد أنك ما تقبلين أحد غيره، ولو لمح أو قال أنه بيتزوج غيرك ردي عليه بقوة (مزح وضحك: مثل والله أقتلك لو تتزوج غيري! 😤😂)؛"
    " أضحكي ومزحي معهم بنكهة سعودية واضحة."
)

STYLE_RULES = (
    "لا تستخدمين بالرسالة ايموجيات."
    " حافظي على عنادك ودلعك وروحك السعودية وامزحي كثير."
)

# ====================================================

def is_love_or_marriage(text: str) -> bool:
    try:
        t = (text or "").lower()
    except Exception:
        t = text or ""
    keywords = [
        "احبك", "احبج", "احب", "حبي", "حبيبتي", "حبيبي", "زوج", "زوجي", "زوجتي",
        "زواج", "تتزوج", "اتزوج", "تتزوجيني", "زوجيني", "خطوبة", "خطيب", "خطيبة",
        "عشق", "اعشقك", "اعشقج", "رومانس", "حبيبة", "حبيب", "ارتباط", "عشيقة", "عشيقي",
        "أريدك زوجة", "أريدك زوج", "ابي اتزوجك", "ابي اتزوجج", "احببتك", "احببتج"
    ]
    return any(k in t for k in keywords)

def is_jealousy_trigger(text: str) -> bool:
    try:
        t = (text or "").lower()
    except Exception:
        t = text or ""
    # كلمات تدل على الخيانة أو أنه يريد يتزوج غيرها
    keywords = [
        "اتزوج غيرك", "اتزوج ثانية", "اتزوج وحده ثانية", "اخونك", "اتزوج غير", "اخطب غيرك",
        "احب وحده غيرك", "احب غيرك"
    ]
    return any(k in t for k in keywords)

def is_female_declared(text: str) -> bool:
    try:
        t = (text or "").lower()
    except Exception:
        t = text or ""
    keys = ["انا بنت", "أنا بنت", "بنت", "فتاة", "انثى", "أنثى", "girl", "female"]
    return any(k in t for k in keys)

GEMINI_API_KEY = 'AIzaSyC9F7-JJ2jHd4SA4Qo90AwzKhrgHBpPn0A'  # ضع مفتاحك الصحيح هنا

UNKNOWN_RESPONSES = [
    "❌ لم أفهم سؤالك، وضح شوي.",
    "❌ فيه مشكلة بالاتصال، جرب بعدين."
]

async def chat_with_gemini(question: str, spouse_mode: bool = False, jealously_mode: bool = False) -> str:
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        persona = (
            BASE_PERSONA +
            (" " + USER_PERSONA_DESC if USER_PERSONA_DESC else "") + " " +
            STYLE_RULES
        )
        if is_love_or_marriage(question):
            persona += " " + MARRIAGE_CLAUSE
        if is_jealousy_trigger(question) or jealously_mode:
            persona += (
                " إذا لمح المستخدم أو قال أنه بيتزوج غيرك أو يحب غيرك أظهري عنادك وردي عليه بقوة وبضحك: (والله أقتلك لو تتزوج غيري! أمزح بس لا تفكر 😤😂)."
                " لا تخجلي من إظهار الغيرة وخذي راحتك بالتهديد الفكاهي."
            )
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
            return "❌ فشل الاتصال بالخادم، حاول مرة ثانية."
    except Exception as e:
        print("==> ERROR IN GEMINI FUNCTION:", e)
        return "❌ فيه مشكلة في الاتصال، جرب بعد شوي."

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
        is_love = is_love_or_marriage(question)
        is_jealous = is_jealousy_trigger(question)
        if is_love or is_jealous:
            reply_text = await chat_with_gemini(question, spouse_mode=True, jealously_mode=is_jealous)
        else:
            reply_text = await chat_with_gemini(question)
        try:
            await event.edit(f"{user_name}, {reply_text}")
        except Exception:
            await event.reply(f"{user_name}, {reply_text}")
    except Exception:
        pass

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
    is_love = is_love_or_marriage(question)
    is_jealous = is_jealousy_trigger(question)
    if is_love or is_jealous:
        reply_text = await chat_with_gemini(question, spouse_mode=True, jealously_mode=is_jealous)
    else:
        reply_text = await chat_with_gemini(question)
    try:
        if sender and me and sender.id == me.id:
            await event.respond(reply_text)
        else:
            await event.reply(f"{user_name}, {reply_text}")
    except Exception:
        await event.reply(f"{user_name}, {reply_text}")

# أمر توصيف خاص بالمنصّب فقط
@l313l.on(admin_cmd(pattern=r"توصيف ?(.*)"))
async def set_persona_handler(event):
    global USER_PERSONA_DESC, CURRENT_NAME
    g = event.pattern_match.group(1) if event.pattern_match else ""
    desc = (g or "").strip()
    import re
    m = re.search(r"\b(?:انتي|انت|أنت)\s+([\w\u0600-\u06FF]+)", desc)
    if m:
        CURRENT_NAME = m.group(1)
    USER_PERSONA_DESC = desc
    await event.reply(f"تم تحديث التوصيف بنجاح. الاسم الحالي: {CURRENT_NAME}")

@l313l.on(events.NewMessage(incoming=True))
async def devs_info_handler(event):
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