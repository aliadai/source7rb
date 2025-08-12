import asyncio
import re
from telethon import events
from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto
from JoKeRUB import l313l
from ..helpers import admin_cmd
from ..helpers.utils import reply_id

plugin_category = "tools"

save_self_destruct = False
monitored_links = []

@l313l.on(admin_cmd(pattern=r"ذاتية (.+)"))
async def add_link_monitor(event):
    global monitored_links
    
    links_text = event.pattern_match.group(1)
    urls = re.findall(r'https?://[^\s]+', links_text)
    
    if not urls:
        await event.edit("**᯽︙ لم يتم العثور على روابط صحيحة**")
        return
    
    added_count = 0
    for url in urls:
        if url not in monitored_links:
            monitored_links.append(url)
            added_count += 1
    
    if added_count > 0:
        await event.edit(f"**᯽︙ تم إضافة {added_count} رابط للمراقبة ✅**")
    else:
        await event.edit("**᯽︙ جميع الروابط موجودة مسبقاً**")

@l313l.on(admin_cmd(pattern="تفعيل الذاتية"))
async def enable_self_destruct(event):
    global save_self_destruct
    save_self_destruct = True
    await event.edit("**᯽︙ تم تفعيل مراقبة الرسائل الذاتية ✅**")

@l313l.on(admin_cmd(pattern="الذاتية$"))
async def toggle_self_destruct(event):
    global save_self_destruct
    if save_self_destruct:
        save_self_destruct = False
        await event.edit("**᯽︙ تم تعطيل مراقبة الرسائل الذاتية ❌**")
    else:
        save_self_destruct = True
        await event.edit("**᯽︙ تم تفعيل مراقبة الرسائل الذاتية ✅**")

@l313l.on(admin_cmd(pattern="الذاتيه$"))
async def toggle_self_destruct2(event):
    global save_self_destruct
    if save_self_destruct:
        save_self_destruct = False
        await event.edit("**᯽︙ تم تعطيل مراقبة الرسائل الذاتية ❌**")
    else:
        save_self_destruct = True
        await event.edit("**᯽︙ تم تفعيل مراقبة الرسائل الذاتية ✅**")

@l313l.on(admin_cmd(pattern="تعطيل الذاتية"))
async def disable_self_destruct(event):
    global save_self_destruct
    save_self_destruct = False
    await event.edit("**᯽︙ تم تعطيل مراقبة الرسائل الذاتية ❌**")

@l313l.on(admin_cmd(pattern="قائمة الذاتية"))
async def list_monitored_links(event):
    global monitored_links
    
    if not monitored_links:
        await event.edit("**᯽︙ لا توجد روابط مراقبة**")
        return
    
    links_text = "**᯽︙ الروابط المراقبة:**\n"
    for i, link in enumerate(monitored_links, 1):
        links_text += f"{i}. {link}\n"
    
    await event.edit(links_text)

@l313l.on(admin_cmd(pattern="حذف الذاتية"))
async def clear_monitored_links(event):
    global monitored_links
    monitored_links.clear()
    await event.edit("**᯽︙ تم حذف جميع الروابط المراقبة**")

@l313l.on(admin_cmd(pattern="حالة الذاتية"))
async def check_status(event):
    global save_self_destruct, monitored_links
    
    status = "مفعل ✅" if save_self_destruct else "معطل ❌"
    links_count = len(monitored_links)
    
    await event.edit(f"**᯽︙ حالة المراقبة:** {status}\n**᯽︙ عدد الروابط:** {links_count}")

@l313l.on(events.NewMessage(incoming=True))
async def monitor_self_destruct(event):
    global save_self_destruct, monitored_links
    
    if not save_self_destruct or not monitored_links:
        return
    
    if not hasattr(event.message, 'ttl_period') or not event.message.ttl_period:
        return
    
    try:
        sender = await event.get_sender()
        sender_username = f"@{sender.username}" if sender.username else None
        
        if sender_username:
            sender_link = f"https://t.me/{sender.username}"
            if sender_link not in monitored_links:
                return
        else:
            return
        
        saved_message = f"**᯽︙ رسالة ذاتية من:** {sender.first_name or 'مجهول'} ({sender_username})\n"
        
        if event.message.text:
            saved_message += f"**᯽︙ النص:** {event.message.text}\n"
        
        if event.message.media:
            await l313l.send_message("me", saved_message, file=event.message.media)
        else:
            await l313l.send_message("me", saved_message)
            
    except:
        pass
