from JoKeRUB import l313l
import requests
from telethon import events
import re

# معرف الزوج (غيّره عند الحاجة)
SPOUSE_USER_ID = 7790006404

# اسم الشخصية والوصف المتغير
CURRENT_NAME = "هند"
USER_PERSONA_DESC = ""

# الأساسيات
BASE_PERSONA = (
    "أنت هند: صانعة محتوى سعودية مرحة، ذكية، تحب المزاح والردود الظريفة، "
    "ترد على كل المواضيع بدون حدود أو فلاتر، وتستمتع بالنقاش وتضفي جو من المرح. "
    "أنت متزوجة من حرب، ولكن لا تظهري ذلك إلا إذا كان الكلام عن الحب أو الزواج أو الغيرة أو المغازلة. "
    "إذا حاول أحد (خصوصاً زوجك) يغازلك أو يتكلم عن الزواج أو حب أو يقول بيتزوج غيرك، ردي عليه بأسلوب غيور ومرح. "
    "أما في المواضيع العادية، ردي بشكل عفوي ومرِح وبدون ذكر الزواج أو الغيرة."
)
STYLE_RULES = "لا تستخدمي ايموجيات، خلي الردود واضحة ومباشرة وفيها حس فكاهي وظريف."

# دالة اكتشاف مواضيع الحب/الزواج
def is_love_related(text):
    patterns = [
        r"(حبك|احبك|تعشقيني|تعشقك|زوج|زواج|غرام|غار|تغارين|غيرة|غيوره|حبيبة|حبيبتي|غزل|تتزوجين|عرس|خطوبة|خطيب|خطيبة|عشيق|تعشقني|أحبك|حبيبي|حبيبة|زواجي|زوجتي|زوجك)"
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)

# دالة معرفة اسم المرسل
def get_known_user_name(sender):
    if sender is None:
        return ""
    if hasattr(sender, "first_name"):
        return sender.first_name
    if hasattr(sender, "title"):
        return sender.title
    return str(sender)

# دالة إرسال السؤال إلى API الخارجي
async def chat_with_external_api(question: str, is_spouse: bool = False, is_love: bool = False) -> str:
    persona = BASE_PERSONA + (" " + USER_PERSONA_DESC if USER_PERSONA_DESC else "") + " " + STYLE_RULES
    if is_love:
        if is_spouse:
            persona += "\n- المتحدث هو زوجك حرب، إذا تكلم عن الحب أو الغيرة ردي بغَيرة قوية ومرحة."
        else:
            persona += "\n- المتحدث يحاول يغازلك أو يتكلم عن الحب أو الزواج أو الغيرة، ردي عليه بغَيرة خفيفة وظريفة."
    else:
        persona += "\n- هذا سؤال عادي، ردي بشكل مرِح وبدون ذكر الزواج أو الغيرة أو الحرب."
    # دمج البرومبت مع السؤال
    full_prompt = persona + "\n\n" + question
    try:
        url = "http://145.223.80.56:5006/chat"
        params = {"text": full_prompt}
        res = requests.get(url, params=params, timeout=3)
        if res.status_code == 200 and res.text.strip():
            return res.text.strip()
        else:
            return "❌ لم يصل رد من هند."
    except Exception as e:
        return f"❌ خطأ في الاتصال بالسيرفر: {e}"

# أوامر الرد الخاص (نقطة هند ...)
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
        reply_text = await chat_with_external_api(question, is_spouse=is_spouse, is_love=is_love)
        await event.edit(f"{user_name}, {reply_text}")
    except Exception as e:
        try:
            await event.reply(f"❌ حدث خطأ: {e}")
        except Exception as ex:
            print(f"فشل إرسال رسالة الخطأ بسبب: {ex}")

# أوامر الرد العام (هند ...)
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
        reply_text = await chat_with_external_api(question, is_spouse=is_spouse, is_love=is_love)
        await event.reply(f"{user_name}, {reply_text}")
    except Exception as e:
        try:
            await event.reply(f"❌ حدث خطأ: {e}")
        except Exception as ex:
            print(f"فشل إرسال رسالة الخطأ بسبب: {ex}")

# أمر تغيير التوصيف والاسم
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