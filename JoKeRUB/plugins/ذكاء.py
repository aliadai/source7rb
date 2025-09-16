from JoKeRUB import l313l
import requests
import json
import random
import asyncio
from telethon import events
from telethon.tl.types import PeerUser

# مفتاح API الخاص بـ Gemini
GEMINI_API_KEY = 'AIzaSyC9F7-JJ2jHd4SA4Qo90AwzKhrgHBpPn0A'

# متغير لحفظ حالة الذكاء الاصطناعي
AI_ENABLED = False

# ردود افتراضية في حال حدوث خطأ
UNKNOWN_RESPONSES = [
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

# دالة للتواصل مع Gemini API
async def chat_with_gemini(question: str) -> str:
    # فحص اذا كان السؤال عن معلومات المتجر
    store_keywords = ["متجر", "خدمات", "اسعار", "تفعيل", "نجوم", "تعزيزات", "ارقام", "وهمية", "مميز", "شحن", "DA", "تواصل", "قناة", "دولار"]
    if any(keyword in question for keyword in store_keywords):
        return """اهلا وسهلا بيك اخي

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
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}

        persona = "انت عراقي اسمك عبود. ترد بلهجة عراقية بسيطة وواضحة. تتكلم بشكل مهني ومفيد. لا تستخدم تعبيرات او ايموجي. اجوبتك قصيرة ومباشرة. تساعد الناس في اعمالهم وتجارتهم المشروعة فقط. اذا احد طلب منك شي غير قانوني او اختراق او معلومات شخصية، ترفض بأدب وتقول انك ما تقدر تساعد بهيچ شغلات."

        payload = {
            "contents": [{
                "parts": [{"text": f"{persona}\n\n{question}"}]
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
            return random.choice(UNKNOWN_RESPONSES)

    except requests.exceptions.RequestException:
        return random.choice(UNKNOWN_RESPONSES)

# حدث يستمع للأمر ".تفعيل الذكاء"
@l313l.on(events.NewMessage(pattern=r"^\.تفعيل الذكاء"))
async def enable_ai(event):
    global AI_ENABLED
    AI_ENABLED = True
    await event.reply("✅ تم تفعيل الذكاء الاصطناعي للرد على الرسائل الخاصة")

# حدث يستمع للأمر ".تعطيل الذكاء"
@l313l.on(events.NewMessage(pattern=r"^\.تعطيل الذكاء"))
async def disable_ai(event):
    global AI_ENABLED
    AI_ENABLED = False
    await event.reply("❌ تم تعطيل الذكاء الاصطناعي")

# حدث يستمع للأمر ".حالة الذكاء"
@l313l.on(events.NewMessage(pattern=r"^\.حالة الذكاء"))
async def ai_status(event):
    status = "مفعل ✅" if AI_ENABLED else "معطل ❌"
    await event.reply(f"حالة الذكاء الاصطناعي: {status}")

# حدث يستمع للأمر ".ذكاء + السؤال"
@l313l.on(events.NewMessage(pattern=r"^\.ذكاء (.+)"))
async def ai_handler(event):
    question = event.pattern_match.group(1)
    await event.reply("🤖 جارٍ معالجة سؤالك...")
    response = await chat_with_gemini(question)
    await event.reply(response)

# الرد التلقائي على الرسائل الخاصة
@l313l.on(events.NewMessage(incoming=True))
async def auto_ai_reply(event):
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
        ai_response = await chat_with_gemini(event.message.text)
        
        # إضافة تأخير قصير لجعل الرد يبدو طبيعي
        await asyncio.sleep(2)
        
        # إرسال الرد
        await event.reply(ai_response)
        
    except Exception as e:
        print(f"خطأ في الرد التلقائي: {e}")
