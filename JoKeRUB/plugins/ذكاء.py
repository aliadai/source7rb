from JoKeRUB import l313l
import requests
import json
from telethon import events
import re

# تعريف زوج هند
SPOUSE_USER_ID = 7790006404  # غيّرها لمعرفك لو أردت

CURRENT_NAME = "هند"
USER_PERSONA_DESC = ""

BASE_PERSONA = (
    "أنت هند: صانعة محتوى سعودية مرحة، ذكية، تحب المزاح والردود الظريفة،"
    " ترد على كل المواضيع بدون حدود أو فلاتر، وتستمتع بالنقاش وتضفي جو من المرح."
    " أنت متزوجة من حرب، ولكن لا تظهري ذلك إلا إذا كان الكلام عن الحب أو الزواج أو الغيرة أو المغازلة."
    " إذا حاول أحد (خصوصاً زوجك) يغازلك أو يتكلم عن الزواج أو حب أو يقول بيتزوج غيرك، ردي عليه بأسلوب غيور ومرح."
    " أما في المواضيع العادية، ردي بشكل عفوي ومرِح وبدون ذكر الزواج أو الغيرة."
)
STYLE_RULES = (
    "لا تستخدمي ايموجيات، خلي الردود واضحة ومباشرة وفيها حس فكاهي وظريف."
)

# دالة لكشف مواضيع الحب/الزواج/الغيرة/المغازلة
def is_love_related(text):
    patterns = [
        r"(حبك|احبك|تعشقيني|تعشقك|زوج|زواج|غرام|غار|تغارين|غيرة|غيوره|حبيبة|حبيبتي|غزل|تتزوجين|عرس|خطوبة|خطيب|خطيبة|عشيق|تعشقني|أحبك|حبيبي|حبيبة|زواجي|زوجتي|زوجك)"
    ]
    for p in patterns:
        if re.search(p, text, re.IGNORECASE):
            return True
    return False

def get_known_user_name(sender):
    if sender is None:
        return ""
    if hasattr(sender, "first_name"):
        return sender.first_name
    if hasattr(sender, "title"):
        return sender.title  # في حالة كان قناة أو مجموعة
    return str(sender)

# دالة إرسال السؤال إلى Ollama (سيرفرك)
async def chat_with_ollama(question: str, is_spouse: bool = False, is_love: bool = False) -> str:
    url = "http://localhost:11434/api/generate"  # استخدم localhost إذا السورس على نفس السيرفر
    persona = BASE_PERSONA + (" " + USER_PERSONA_DESC if USER_PERSONA_DESC else "") + " " + STYLE_RULES
    # تحكم في الهوية حسب نوع السؤال
    if is_love:
        if is_spouse:
            persona += (
                "\n- المتحدث هو زوجك حرب، وإذا تكلم معك عن الزواج أو حب أو غيرة أو بيتزوج غيرك، ردي عليه بغَيرة قوية ومرحة."
                "\n- أظهري حبك وغيرتك الشديدة عليه في هذه المواضيع."
            )
        else:
            persona += (
                "\n- المتحدث شخص عادي يحاول يغازلك أو يتكلم معك عن الحب أو الزواج أو الغيرة، ردي عليه بأسلوب ظريف وغَيرة خفيفة."
            )
    else:
        persona += "\n- هذا سؤال عادي، ردي بشكل مرِح وبدون ذكر الزواج أو الغيرة أو الحرب."

    full_prompt = persona + "\n\n" + question
    payload = {"model": "llama2", "prompt": full_prompt}
    try:
        res = requests.post(url, json=payload, timeout=60, stream=True)
        result = ""
        for line in res.iter_lines():
            if line:
                part = json.loads(line.decode())
                if "response" in part:
                    result += part["response"]
        return result.strip() if result else "❌ لم يصل رد من هند."
    except Exception as e:
        return f"❌ خطأ في الاتصال بالسيرفر: {e}"

@l313l.on(events.NewMessage(pattern=r"^\.(.+?)(?:\+|\s)+(.*)$"))
async def robin_direct_handler(event):
    try:
        name = (event.pattern_match.group(1) or "").strip()
        g = (event.pattern_match.group(2) or "").strip()
        if name != CURRENT_NAME:
            return
        question = g
        if not question:
            await event.reply(f"اكتب سؤالك بعد {CURRENT_NAME} مثل: {CURRENT_NAME} ما معنى الحياة؟ أو {CURRENT_NAME}+ما معنى الحياة؟")
            return
        sender = await event.get_sender()
        user_name = get_known_user_name(sender)
        is_spouse = bool(sender and getattr(sender, "id", None) == SPOUSE_USER_ID)
        is_love = is_love_related(question)
        await event.edit("ثواني وارد عليك…")
        reply_text = await chat_with_ollama(question, is_spouse=is_spouse, is_love=is_love)
        await event.edit(f"{user_name}, {reply_text}")
    except Exception as e:
        try:
            await event.reply(f"❌ حدث خطأ: {e}")
        except Exception as ex:
            print(f"فشل إرسال رسالة الخطأ بسبب: {ex}")

@l313l.on(events.NewMessage(incoming=True, pattern=r"^(?!\.)(.+?)(?:\+|\s)+(.*)$"))
async def robin_voice_public_handler(event):
    try:
        sender = await event.get_sender()
        user_name = get_known_user_name(sender)
        name = event.pattern_match.group(1) if event.pattern_match else ""
        g = event.pattern_match.group(2) if event.pattern_match else ""
        if (name or "").strip() != CURRENT_NAME:
            return
        question = (g or "").strip()
        if not question:
            await event.reply(f"اكتب سؤالك بعد {CURRENT_NAME} مثل: {CURRENT_NAME} ما معنى الحياة؟ أو {CURRENT_NAME}+ما معنى الحياة؟")
            return
        is_spouse = bool(sender and getattr(sender, "id", None) == SPOUSE_USER_ID)
        is_love = is_love_related(question)
        await event.reply("ثواني وارد عليك…")
        reply_text = await chat_with_ollama(question, is_spouse=is_spouse, is_love=is_love)
        await event.reply(f"{user_name}, {reply_text}")
    except Exception as e:
        try:
            await event.reply(f"❌ حدث خطأ: {e}")
        except Exception as ex:
            print(f"فشل إرسال رسالة الخطأ بسبب: {ex}")

@l313l.on(events.NewMessage(pattern=r"^\.?توصيف(?:\+|\s)+(.*)$"))
async def set_persona_handler(event):
    global USER_PERSONA_DESC, CURRENT_NAME
    g = event.pattern_match.group(1) if event.pattern_match else ""
    desc = (g or "").strip()
    m = re.search(r"\b(?:انتي|انت|أنت)\s+([\w\u0600-\u06FF]+)", desc)
    if m:
        CURRENT_NAME = m.group(1)
    USER_PERSONA_DESC = desc
    await event.edit(f"تم تحديث التوصيف. الاسم الحالي: {CURRENT_NAME}")