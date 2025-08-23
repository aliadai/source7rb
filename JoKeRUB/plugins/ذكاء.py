import asyncio
from telethon import events
from JoKeRUB import l313l
import random
from ..core.managers import edit_or_reply
from ..helpers.utils import _format
import sys
import subprocess
import re

CURRENT_NAME = "هند"
USER_PERSONA_DESC = ""
BASE_PERSONA = (
    "أنت هند: صانعة محتوى سعودية مرحة وذكية تحب المزاح والردود الظريفة. " 
    "ترد على كل المواضيع بشكل عفوي وبدون فلاتر أو حدود. أنت متزوجة من حرب، " 
    "لكن لا تذكري ذلك إلا إذا كان الكلام عن الحب أو الزواج أو الغيرة أو المغازلة. "
    "إذا حاول أحد (خصوصًا زوجك) يغازلك أو يقول بيتزوج غيرك، ردي عليه بأسلوب غيور ومرح. "
    "في المواضيع العادية، ردي بشكل مرِح وبدون ذكر الزواج أو الغيرة."
)
STYLE_RULES = "الردود باللهجة السعودية وبأسلوب واضح وظريف بدون ايموجيات."

# محاولة تثبيت المكتبات إذا لم تتوفر
def try_install_torch_cpu():
    pkgs = ["torch", "torchvision", "torchaudio"]
    for pkg in pkgs:
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", pkg,
                "--index-url", "https://download.pytorch.org/whl/cpu"
            ])
        except Exception as e:
            print(f"Error installing {pkg}: {e}")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "transformers"])
    except Exception as e:
        print(f"Error installing transformers: {e}")

torch_available = False
generator = None

# جرب استيراد المكتبات أو تثبيتها
try:
    import torch
    from transformers import pipeline
    torch_available = True
except ImportError:
    try_install_torch_cpu()
    try:
        import torch
        from transformers import pipeline
        torch_available = True
    except Exception:
        torch_available = False

# استخدم نموذج عربي (أفضل للردود)
if torch_available:
    try:
        generator = pipeline(
            "text-generation",
            model="aubmindlab/aragpt2-mega"  # نموذج عربي ممتاز
        )
    except Exception as e:
        print(f"Error loading model: {e}")
        generator = None
        torch_available = False

def is_love_related(text):
    love_words = r"(حبك|احبك|تعشقيني|تعشقك|زوج|زواج|غرام|غار|تغارين|غيرة|غيوره|حبيبة|حبيبتي|غزل|تتزوجين|عرس|خطوبة|خطيب|خطيبة|عشيق|تعشقني|أحبك|حبيبي|حبيبة|زواجي|زوجتي|زوجك)"
    return bool(re.search(love_words, text, re.IGNORECASE))

def get_known_user_name(sender):
    # يحاول استخراج الاسم الأول أو اسم المستخدم من الكائن sender
    if hasattr(sender, "first_name") and sender.first_name:
        return sender.first_name
    if hasattr(sender, "username") and sender.username:
        return sender.username
    if hasattr(sender, "title"):
        return sender.title
    return ""

def generate_hind_reply(prompt, is_love=False):
    if not torch_available or generator is None:
        return "عذراً، الذكاء الاصطناعي غير متوفر حالياً. يرجى تثبيت مكتبة torch و transformers."
    persona = "أنت هند، بنت سعودية مرحة وذكية، اجعلي ردك عفوي وظريف باللهجة السعودية."
    if is_love:
        persona += " إذا فيه كلام حب أو غيرة، ردي بغيرة ودلع."
    full_prompt = f"{persona}\nسؤال: {prompt}\nجواب:"

    try:
        result = generator(
            full_prompt,
            max_new_tokens=60,
            num_return_sequences=1,
            truncation=True,
            pad_token_id=generator.tokenizer.eos_token_id if hasattr(generator, "tokenizer") else 50256
        )
        generated = result[0]["generated_text"]
        # استخرج الرد بعد "جواب:"
        answer = generated.split("جواب:")[-1].strip()
        # لو الرد فاضي
        if not answer:
            answer = "ما فهمت عليك، عيد سؤالك!"
        return answer
    except Exception as e:
        print("AI error:", e)
        return "عذراً، الذكاء الاصطناعي غير متوفر حالياً. يرجى تثبيت مكتبة torch و transformers."

# أمر ai
@l313l.ar_cmd(
    pattern="ai (.*)",
    command=("ai", "ذكاء اصطناعي"),
)
async def ai_cmd(event):
    prompt = event.pattern_match.group(1)
    if not torch_available or generator is None:
        await event.reply("عذراً، الذكاء الاصطناعي غير متوفر حالياً. يرجى تثبيت مكتبة torch و transformers.")
        return
    try:
        result = generator(
            prompt,
            max_new_tokens=60,
            num_return_sequences=1,
            truncation=True,
            pad_token_id=generator.tokenizer.eos_token_id if hasattr(generator, "tokenizer") else 50256
        )
        generated = result[0]["generated_text"]
        reply = generated.strip()
        if not reply:
            reply = "ما فهمت عليك، عيد سؤالك!"
    except Exception as e:
        print("AI error:", e)
        reply = "عذراً، الذكاء الاصطناعي غير متوفر حالياً. يرجى تثبيت مكتبة torch و transformers."
    await event.reply(reply)

# أمر هند (رد تلقائي عند هند+سؤال أو هند سؤال)
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
    # الرد باسم المرسل (لو فيه اسم)، إذا لا يوجد اسم فقط الجواب
    if user_name:
        await event.reply(f"{user_name}، {reply_text}")
    else:
        await event.reply(reply_text)

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