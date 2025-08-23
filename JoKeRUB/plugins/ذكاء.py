import io
import os
import random
import textwrap

from PIL import Image, ImageDraw, ImageFont
from telethon.tl.types import InputMessagesFilterDocument

from JoKeRUB import l313l
import requests
from bs4 import BeautifulSoup
import re

CURRENT_NAME = "هند"
USER_PERSONA_DESC = ""
STYLE_RULES = "الردود باللهجة السعودية وبأسلوب واضح وظريف بدون ايموجيات."

BASE_PERSONA = (
    "أنت هند: صانعة محتوى سعودية مرحة وذكية تحب المزاح والردود الظريفة. "
    "ترد على كل المواضيع بشكل عفوي وبدون فلاتر أو حدود. أنت متزوجة من حرب، "
    "لكن لا تذكري ذلك إلا إذا كان الكلام عن الحب أو الزواج أو الغيرة أو المغازلة. "
    "إذا حاول أحد (خصوصًا زوجك) يغازلك أو يقول بيتزوج غيرك، ردي عليه بأسلوب غيور ومرح. "
    "في المواضيع العادية، ردي بشكل مرِح وبدون ذكر الزواج أو الغيرة."
)

def is_love_related(text):
    love_words = r"(حبك|احبك|تعشقيني|تعشقك|زوج|زواج|غرام|غار|تغارين|غيرة|غيوره|حبيبة|حبيبتي|غزل|تتزوجين|عرس|خطوبة|خطيب|خطيبة|عشيق|تعشقني|أحبك|حبيبي|حبيبة|زواجي|زوجتي|زوجك)"
    return bool(re.search(love_words, text, re.IGNORECASE))

def get_known_user_name(sender):
    if hasattr(sender, "first_name") and sender.first_name:
        return sender.first_name
    if hasattr(sender, "username") and sender.username:
        return sender.username
    if hasattr(sender, "title"):
        return sender.title
    return ""

def get_hind_reply(prompt, is_love=False):
    persona = BASE_PERSONA
    if is_love:
        persona += " لو فيه حب أو غيرة، ردي بغيرة ودلع."
    if USER_PERSONA_DESC:
        persona += " " + USER_PERSONA_DESC
    persona += " " + STYLE_RULES

    full_prompt = f"{persona}\nسؤال: {prompt}\nجواب:"
    url = "https://youchat.com/search?q=" + requests.utils.quote(full_prompt)
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        ans = soup.find("div", {"class": "you-chat-response"})
        if ans and ans.text.strip():
            return ans.text.strip()
    except Exception as e:
        print("خطأ في جلب الرد:", e)
    return "❌ ما قدرت أجيب رد من الموقع."

# أمر ai
@l313l.on(admin_cmd(pattern=r"ai ?(.*)"))
async def ai_cmd(event):
    prompt = event.pattern_match.group(1)
    reply = get_hind_reply(prompt)
    await event.reply(reply)

# أمر هند (مثال: .هند مرحبا)
@l313l.on(admin_cmd(pattern=r"هند ?(.*)"))
async def hind_cmd(event):
    question = event.pattern_match.group(1)
    sender = await event.get_sender()
    user_name = get_known_user_name(sender)
    is_love = is_love_related(question)
    reply_text = get_hind_reply(question, is_love=is_love)
    if user_name:
        await event.reply(f"{user_name}، {reply_text}")
    else:
        await event.reply(reply_text)

# أمر تغيير توصيف واسم الشخصية
@l313l.on(admin_cmd(pattern=r"توصيف ?(.*)"))
async def set_persona_handler(event):
    global USER_PERSONA_DESC, CURRENT_NAME
    desc = (event.pattern_match.group(1) or "").strip()
    m = re.search(r"\b(?:انتي|انت|أنت)\s+([\w\u0600-\u06FF]+)", desc)
    if m:
        CURRENT_NAME = m.group(1)
    USER_PERSONA_DESC = desc
    await event.reply(f"تم تحديث التوصيف. الاسم الحالي: {CURRENT_NAME}")