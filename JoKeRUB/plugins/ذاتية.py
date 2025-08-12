#all write Codes By Team 7rB  @RobinSource
#By Hussein @F_O_1
import asyncio
from telethon import events
from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto
from JoKeRUB import l313l
from ..helpers import admin_cmd
from ..helpers.utils import reply_id

plugin_category = "tools"

# متغير لحفظ حالة تفعيل/إلغاء تفعيل حفظ الرسائل الذاتية
save_self_destruct = False

@l313l.on(admin_cmd(pattern="الذاتية"))
async def toggle_self_destruct_save(event):
    """تفعيل/إلغاء تفعيل حفظ الرسائل الذاتية"""
    global save_self_destruct
    
    if save_self_destruct:
        save_self_destruct = False
        await event.edit("**᯽︙ تم إيقاف حفظ الرسائل الذاتية ❌**")
    else:
        save_self_destruct = True
        await event.edit("**᯽︙ تم تفعيل حفظ الرسائل الذاتية ✅**\n**᯽︙ سيتم حفظ جميع الرسائل الذاتية في الرسائل المحفوظة دون فتحها**")

@l313l.on(events.NewMessage(incoming=True))
async def save_self_destructing_messages(event):
    """حفظ الرسائل الذاتية عند وصولها"""
    global save_self_destruct
    
    # التحقق من أن الميزة مفعلة
    if not save_self_destruct:
        return
    
    # التحقق من أن الرسالة ذاتية التدمير
    if not hasattr(event.message, 'ttl_period') or not event.message.ttl_period:
        return
    
    try:
        # معلومات الرسالة
        sender = await event.get_sender()
        sender_name = sender.first_name if sender.first_name else "مجهول"
        sender_username = f"@{sender.username}" if sender.username else "بدون يوزر"
        chat = await event.get_chat()
        chat_title = chat.title if hasattr(chat, 'title') and chat.title else "محادثة خاصة"
        
        # إنشاء نص الرسالة المحفوظة
        saved_message = f"**᯽︙ رسالة ذاتية محفوظة**\n"
        saved_message += f"**᯽︙ من:** {sender_name} ({sender_username})\n"
        saved_message += f"**᯽︙ في:** {chat_title}\n"
        saved_message += f"**᯽︙ مدة التدمير:** {event.message.ttl_period} ثانية\n"
        saved_message += f"**᯽︙ التاريخ:** {event.message.date.strftime('%Y-%m-%d %H:%M:%S')}\n"
        saved_message += "**᯽︙ المحتوى:**\n"
        
        # إضافة نص الرسالة إن وجد
        if event.message.text:
            saved_message += f"{event.message.text}\n"
        
        # حفظ الرسالة في الرسائل المحفوظة
        if event.message.media:
            # إذا كانت الرسالة تحتوي على ميديا
            if isinstance(event.message.media, (MessageMediaPhoto, MessageMediaDocument)):
                await l313l.send_message(
                    "me",
                    saved_message,
                    file=event.message.media
                )
            else:
                await l313l.send_message("me", saved_message)
        else:
            # رسالة نصية فقط
            await l313l.send_message("me", saved_message)
            
    except Exception as e:
        # في حالة حدوث خطأ، نرسل إشعار للمستخدم
        try:
            await l313l.send_message(
                "me", 
                f"**᯽︙ خطأ في حفظ الرسالة الذاتية:**\n{str(e)}"
            )
        except:
            pass

@l313l.on(admin_cmd(pattern="حالة الذاتية"))
async def check_self_destruct_status(event):
    """التحقق من حالة تفعيل حفظ الرسائل الذاتية"""
    global save_self_destruct
    
    status = "مفعل ✅" if save_self_destruct else "معطل ❌"
    await event.edit(f"**᯽︙ حالة حفظ الرسائل الذاتية:** {status}")

# معلومات الأوامر
CMD_HELP.update({
    "الذاتية": """**اسم الإضافة:** الذاتية
**الوصف:** حفظ الرسائل الذاتية في الرسائل المحفوظة دون فتحها

**الأوامر:**
`.الذاتية` - تفعيل/إيقاف حفظ الرسائل الذاتية
`.حالة الذاتية` - عرض حالة تفعيل الميزة

**الاستخدام:**
عند تفعيل الأمر، سيتم حفظ جميع الرسائل الذاتية التي تصلك في الرسائل المحفوظة مع معلومات المرسل والتاريخ دون فتح الرسالة الأصلية.

**ملاحظة:** الميزة تعمل فقط عن طريق الراب (الرسائل الواردة)."""
})
