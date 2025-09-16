import asyncio
import re
from telethon import events
from telethon.tl.types import PeerUser
from JoKeRUB import l313l
from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.utils import admin_cmd
import requests
from bs4 import BeautifulSoup

GEMINI_API_KEY = 'AIzaSyC9F7-JJ2jHd4SA4Qo90AwzKhrgHBpPn0A'

# متغير لحفظ حالة الذكاء الاصطناعي
AI_ENABLED = False

# قاعدة بيانات بسيطة لحفظ حالة الذكاء لكل مستخدم
AI_USERS = {}

def get_ai_response(message_text):
    """
    دالة للحصول على رد من الذكاء الاصطناعي
    """
    # فحص اذا كان السؤال عن معلومات المتجر
    store_keywords = ["متجر", "خدمات", "اسعار", "تفعيل", "نجوم", "تعزيزات", "ارقام", "وهمية", "مميز", "شحن", "DA", "تواصل", "قناة", "دولار"]
    if any(keyword in message_text for keyword in store_keywords):
        return get_store_info_response(message_text)
    
    # شخصية تجارية عراقية
    persona = (
        "انت شخص تجاري عراقي محترف اسمك عبود. ترد بلهجة عراقية بسيطة وواضحة. "
        "تتكلم بشكل مهني ومفيد. لا تستخدم تعبيرات او ايموجي. "
        "اجوبتك قصيرة ومباشرة. تساعد الناس في اعمالهم وتجارتهم المشروعة فقط. "
        "اذا احد طلب منك شي غير قانوني او اختراق او معلومات شخصية، ترفض بأدب وتقول انك ما تقدر تساعد بهيچ شغلات."
    )

    try:
        # استخدام Gemini API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": f"{persona}\n\n{message_text}"
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 1,
                "topP": 1,
                "maxOutputTokens": 100,
                "stopSequences": []
            }
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']['parts'][0]['text']
                return content.strip()
    except Exception as e:
        print(f"خطأ في Gemini API: {e}")
    
    # ردود احتياطية بلهجة عراقية تجارية
    backup_responses = [
        "شلونك اخي، شنو تحتاج؟",
        "اهلا وسهلا، كيف اقدر اساعدك؟",
        "تفضل اخي، شنو المطلوب؟",
        "مرحبا، شنو الموضوع؟",
        "اهلين، كيف الحال؟",
        "تسلم اخي، شنو تريد؟",
        "اهلا بيك، شلون اقدر افيدك؟",
        "عيني عبود، فتحت الرابط وشفت الرسالة. بس تدري عيني، هاي المعلومات ما نكدر نوصلها ولا نتكشفها. هاي خصوصية ناس ومسؤوليتنا نحافظ عليها. اذا عندك شي تحتاج مساعدة فيه، احنا موجودين.",
        "عيني، هذا الرقم تقدر تتفرمت بي جواله وما نقدر نوصلها ولا تتكشفها. هاي خصوصية ناس ومسؤوليتنا نحافظ عليها. اذا عندك شغلة ثانية نقدر نساعدك فيها.",
        "اخي الكريم، هاي المعلومات شخصية ومحمية قانونياً. ما نقدر نساعدك بهيچ شغلات. لو تحتاج مساعدة بشي ثاني، تفضل.",
        "عبود، هذا شغل خصوصية وما يجوز نتدخل بيه. اذا تحتاج مساعدة بشي مشروع وقانوني، احنا موجودين لخدمتك."
    ]
    
    import random
    return random.choice(backup_responses)

def get_store_info_response(message_text):
    """
    دالة للرد على الاستفسارات عن معلومات المتجر
    """
    store_info = """اهلا وسهلا بيك اخي

متجر DA - متخصصين بخدمات التلجرام جميعها والاهم التعزيزات

خدماتنا:
• تفعيل مميز: 3 شهور ب 14$ | 6 شهور ب 18$ | سنة كاملة ب 32$
• شحن النجوم: كل 100 نجمة ب 1.8 دولار
• التعزيزات السنوية: كل 10 تعزيزات ب 2.5 دولار او 200 نجمة
• الارقام الوهمية: كل رقم ب 1 دولار او 100 نجمة
• حسابات محذوفة

معلومات التواصل:
• القناة: @rsss0
• التواصل المباشر: @abod9d
• الايميل: tzzzzioni@gmail.com
• متوفرين 24 ساعة باليوم

السرعة والثقة دائما بالاعلى عندنا"""
    
    return store_info

@l313l.on(admin_cmd(pattern=r"تفعيل الذكاء"))
async def enable_ai(event):
    """
    أمر تفعيل الذكاء الاصطناعي
    """
    global AI_ENABLED
    AI_ENABLED = True
    await edit_or_reply(event, "✅ تم تفعيل الذكاء الاصطناعي للرد على الرسائل الخاصة")

@l313l.on(admin_cmd(pattern=r"تعطيل الذكاء"))
async def disable_ai(event):
    """
    أمر تعطيل الذكاء الاصطناعي
    """
    global AI_ENABLED
    AI_ENABLED = False
    await edit_or_reply(event, "❌ تم تعطيل الذكاء الاصطناعي")

@l313l.on(admin_cmd(pattern=r"حالة الذكاء"))
async def ai_status(event):
    """
    أمر معرفة حالة الذكاء الاصطناعي
    """
    status = "مفعل ✅" if AI_ENABLED else "معطل ❌"
    await edit_or_reply(event, f"حالة الذكاء الاصطناعي: {status}")

@l313l.on(events.NewMessage(incoming=True))
async def auto_ai_reply(event):
    """
    الرد التلقائي بالذكاء الاصطناعي على الرسائل الخاصة فقط
    """
    global AI_ENABLED
    
    # التحقق من أن الذكاء مفعل
    if not AI_ENABLED:
        return
    
    # التحقق من أن الرسالة في الخاص وليس في مجموعة
    if not isinstance(event.peer_id, PeerUser):
        return
    
    # التحقق من أن الرسالة ليست من البوت نفسه
    if event.sender_id == l313l.uid:
        return
    
    # التحقق من أن الرسالة تحتوي على نص
    if not event.message.text:
        return
    
    # تجاهل الأوامر (الرسائل التي تبدأ بنقطة أو رمز)
    if event.message.text.startswith(('.', '/', '!', '#')):
        return
    
    try:
        # الحصول على رد من الذكاء الاصطناعي
        ai_response = get_ai_response(event.message.text)
        
        # إضافة تأخير قصير لجعل الرد يبدو طبيعي
        await asyncio.sleep(2)
        
        # إرسال الرد
        await event.reply(ai_response)
        
    except Exception as e:
        print(f"خطأ في الرد التلقائي: {e}")

# أوامر إضافية للتحكم في الذكاء
@l313l.on(admin_cmd(pattern=r"ذكاء ?(.*)"))
async def manual_ai(event):
    """
    أمر للحصول على رد من الذكاء الاصطناعي يدوياً
    """
    question = event.pattern_match.group(1)
    if not question:
        await edit_or_reply(event, "يرجى كتابة سؤال بعد الأمر")
        return
    
    try:
        response = get_ai_response(question)
        await edit_or_reply(event, response)
    except Exception as e:
        await edit_or_reply(event, f"خطأ: {str(e)}")

# أمر مخفي للذكاء بدون كتابة "ذكاء" - فقط في الخاص
@l313l.on(admin_cmd(pattern=r"(.+)", outgoing=True))
async def hidden_ai(event):
    """
    رد تلقائي على أي رسالة من المالك في الخاص فقط
    """
    global AI_ENABLED
    
    # التحقق من أن الذكاء مفعل
    if not AI_ENABLED:
        return
    
    # التحقق من أن الرسالة في الخاص وليس في مجموعة أو قناة
    if not isinstance(event.peer_id, PeerUser):
        return
    
    # تجاهل الأوامر المعروفة
    message_text = event.message.text
    if message_text.startswith(('.تفعيل', '.تعطيل', '.حالة', '.ذكاء')):
        return
    
    try:
        response = get_ai_response(message_text)
        await edit_or_reply(event, response)
    except Exception as e:
        print(f"خطأ في الرد المخفي: {e}")

# معلومات الإضافة
CMD_HELP.update({
    "ذكاء_تجاري": """**اسم الإضافة:** الذكاء الاصطناعي التجاري
**الوصف:** ذكاء اصطناعي يرد تلقائياً على الرسائل الخاصة بلهجة عراقية تجارية

**الأوامر:**
  •  `.تفعيل الذكاء`
**الاستخدام:** تفعيل الرد التلقائي للذكاء الاصطناعي

  •  `.تعطيل الذكاء`
**الاستخدام:** تعطيل الرد التلقائي للذكاء الاصطناعي

  •  `.حالة الذكاء`
**الاستخدام:** معرفة حالة الذكاء الاصطناعي (مفعل أم معطل)

  •  `.ذكاء [السؤال]`
**الاستخدام:** الحصول على رد من الذكاء الاصطناعي يدوياً

**ملاحظة:** الذكاء يرد فقط على الرسائل الخاصة وليس في المجموعات"""
})
