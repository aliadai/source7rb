try:
    import torch
    from transformers import pipeline
    torch_available = True
except ImportError:
    torch_available = False

import re

from telethon import Button, events
from telethon.events import CallbackQuery

from l313l.razan.resources.assistant import *
from l313l.razan.resources.mybot import *
from JoKeRUB import l313l
from ..core import check_owner
from ..Config import Config
 
import sys
import subprocess

CURRENT_NAME = "هند"
USER_PERSONA_DESC = ""
BASE_PERSONA = (
    "أنت هند: صانعة محتوى سعودية مرحة، ذكية، تحب المزاح والردود الظريفة، "
    "ترد على كل المواضيع بدون حدود أو فلاتر، وتستمتع بالنقاش وتضفي جو من المرح. "
    "أنت متزوجة من حرب، ولكن لا تظهري ذلك إلا إذا كان الكلام عن الحب أو الزواج أو الغيرة أو المغازلة. "
    "إذا حاول أحد (خصوصاً زوجك) يغازلك أو يتكلم عن الزواج أو حب أو يقول بيتزوج غيرك، ردي عليه بأسلوب غيور ومرح. "
    "أما في المواضيع العادية، ردي بشكل عفوي ومرِح وبدون ذكر الزواج أو الغيرة."
)
STYLE_RULES = "لا تستخدمي ايموجيات، خلي الردود واضحة ومباشرة وفيها حس فكاهي وظريف."

# --- محاولة استيراد وتثبيت torch و transformers ---
torch_available = False
generator = None

def try_install(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except Exception as e:
        return False

try:
    import torch
    from transformers import pipeline
    torch_available = True
except ImportError:
    # حاول التثبيت التلقائي
    torch_ok = try_install("torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu")
    transformers_ok = try_install("transformers")
    try:
        import torch
        from transformers import pipeline
        torch_available = True
    except Exception:
        torch_available = False

if torch_available:
    try:
        generator = pipeline("text-generation", model="distilgpt2")
    except Exception:
        torch_available = False

def is_love_related(text):
    love_words = r"(حبك|احبك|تعشقيني|تعشقك|زوج|زواج|غرام|غار|تغارين|غيرة|غيوره|حبيبة|حبيبتي|غزل|تتزوجين|عرس|خطوبة|خطيب|خطيبة|عشيق|تعشقني|أحبك|حبيبي|حبيبة|زواجي|زوجتي|زوجك)"
    return bool(re.search(love_words, text, re.IGNORECASE))

def get_known_user_name(sender):
    if hasattr(sender, "first_name") and sender.first_name:
        return sender.first_name
    if hasattr(sender, "title"):
        return sender.title
    return str(sender) if sender else ""

def generate_hind_reply(prompt, is_love=False):
    if not torch_available or generator is None:
        return "- 7r𝐁 ∘, عذراً، الذكاء الاصطناعي غير متوفر حالياً. يرجى تثبيت مكتبة torch و transformers على السيرفر."
    persona = BASE_PERSONA
    if USER_PERSONA_DESC:
        persona += f" {USER_PERSONA_DESC}"
    persona += " " + STYLE_RULES

    if is_love:
        persona += "\n- إذا كان السائل زوجك أو أحد يغار عليك أو يغازلك، ردي عليه بغَيرة مرحة."
    else:
        persona += "\n- سؤال عادي، ردي بشكل مرِح وبدون ذكر الزواج أو الغيرة أو الحرب."

    full_prompt = persona + "\n\n" + prompt
    result = generator(full_prompt, max_length=120, num_return_sequences=1)
    response = result[0]["generated_text"]
    return response

# أمر ai
@l313l.ar_cmd(
    pattern="ai (.*)",
    command=("ai", "ذكاء اصطناعي"),
)
async def ai_cmd(event):
    prompt = event.pattern_match.group(1)
    reply = "- 7r𝐁 ∘, عذراً، الذكاء الاصطناعي غير متوفر حالياً. يرجى تثبيت مكتبة torch و transformers على السيرفر."
    if torch_available and generator is not None:
        try:
            reply = generator(prompt, max_length=120, num_return_sequences=1)[0]["generated_text"]
        except Exception:
            reply = "- 7r𝐁 ∘, عذراً، الذكاء الاصطناعي غير متوفر حالياً. يرجى تثبيت مكتبة torch و transformers على السيرفر."
    await event.reply(reply)

# أمر هند (رد تلقائي عند هند+سؤال أو هند سؤال) في أي مكان
@l313l.ar_cmd(
    pattern="هند(?:\\+|\\s)+(.*)",
    command=("هند", "ذكاء اصطناعي"),
)
async def hind_cmd(event):
    question = event.pattern_match.group(1)
    sender = await event.get_sender()
    user_name = get_known_user_name(sender)
    is_love = is_love_related(question)
    reply_text = generate_hind_reply(question, is_love=is_love)
    await event.reply(f"{user_name}, {reply_text}")

# أمر تغيير توصيف واسم الشخصية
@l313l.ar_cmd(
    pattern="توصيف(?:\\+|\\s)+(.*)",
    command=("توصيف", "ذكاء اصطناعي"),
)
async def set_persona_handler(event):
    global USER_PERSONA_DESC, CURRENT_NAME
    desc = (event.pattern_match.group(1) or "").strip()
    m = re.search(r"\b(?:انتي|انت|أنت)\s+([\w\u0600-\u06FF]+)", desc)
    if m:
        CURRENT_NAME = m.group(1)
    USER_PERSONA_DESC = desc
    await event.reply(f"تم تحديث التوصيف. الاسم الحالي: {CURRENT_NAME}")