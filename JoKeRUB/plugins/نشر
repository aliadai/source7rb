# Plugin: انشر
# Provides a publishing command `.انشر` and a stop command `وكف نشر`
# Usage examples:
# - Reply to a message then: .انشر 8 9 @groupusername -> will publish the replied message 8 times with 9s delay to @groupusername
# - In current chat without reply: .انشر 8 9 احبك -> will publish the text "احبك" 8 times with 9s delay in the current chat
# - Stop all publishing/repeating: وكف نشر

import asyncio
import re
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl import functions, types

from JoKeRUB import l313l
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus

# Local stop flag for this plugin's loops
_publish_running = True

async def _resolve_chat_id(client, identifier):
    """Accept @username, t.me link, -100id or numeric id and return entity id."""
    ident = identifier.strip()
    if ident.startswith("https://t.me/"):
        ident = ident.replace("https://t.me/", "@").strip()
    if ident.startswith("-100"):
        try:
            return int(ident)
        except Exception:
            pass
    try:
        entity = await client.get_entity(ident)
        return entity.id
    except Exception:
        return None

async def _publish_loop(client, chat_id, message, count, delay):
    global _publish_running
    _publish_running = True
    # mark global var so other modules can stop too
    addgvar("spamwork", True)
    try:
        for _ in range(count):
            # Check global and local stop flags
            if gvarstatus("spamwork") is None or not _publish_running:
                break
            if message and getattr(message, "media", None):
                await client.send_file(chat_id, message.media, caption=message.text)
            else:
                text = message.text if hasattr(message, "text") and message.text else str(message)
                await client.send_message(chat_id, text)
            await asyncio.sleep(delay)
    finally:
        # do not clear spamwork here; other operations may still use it
        pass

@l313l.ar_cmd(pattern="^(?:\.|)?(?:انشر|نشر)(?:\s|$)(.*)")
async def publish_handler(event):
    """
    Patterns supported:
    - Reply + targets: انشر <count> <seconds> <target...>
    - Reply only (no targets): انشر <count> <seconds>
    - No reply (current chat): انشر <count> <seconds> <message text>
    - No reply (targets + message): انشر <count> <seconds> <target...> <message text>
      مثال: .نشر 5 6 -1002813200347 احبك
    """
    try:
        # Extract the rest of the text after command
        args_text = event.text.split(maxsplit=1)
        args_text = args_text[1] if len(args_text) > 1 else ""
        if not args_text:
            return await edit_delete(event, "⌔∮ يجب استخدام كتابة صحيحة: انشر <عدد> <ثواني> [نص/اهداف]", 7)
        parts = re.split(r"\s+", args_text, maxsplit=2)
        if len(parts) < 2:
            return await edit_delete(event, "⌔∮ يجب استخدام كتابة صحيحة: انشر <عدد> <ثواني> [نص/اهداف]", 7)
        count = int(parts[0])
        seconds = int(parts[1])
        tail = parts[2] if len(parts) > 2 else ""
    except Exception:
        return await edit_delete(event, "⌔∮ يجب استخدام كتابة صحيحة: انشر <عدد> <ثواني> [نص/اهداف]", 7)

    reply = await event.get_reply_message()

    # Determine mode
    # 1) If replying and tail provided -> treat tail as space-separated targets
    # 2) If replying and no tail -> publish replied message in current chat
    # 3) If not replying -> treat tail (or empty) as message text in current chat

    client = event.client

    if reply:
        if tail:
            # Targets mode: can be multiple usernames/links/ids
            targets = tail.split()
            ok = 0
            bad = []
            await event.delete()
            for t in targets:
                chat_id = await _resolve_chat_id(client, t)
                if chat_id is None:
                    bad.append(t)
                    continue
                await _publish_loop(client, chat_id, reply, count, seconds)
                ok += 1
                # small pause between different targets
                await asyncio.sleep(1)
            if bad and ok:
                return await edit_or_reply(event, f"**᯽︙ تم النشر بنجاح في {ok} هدف ✅**\n**᯽︙ تعذر النشر في:** `{', '.join(bad)}`")
            elif ok:
                return  # done silently
            else:
                return await edit_or_reply(event, "**᯽︙ تعذر العثور على أي هدف صالح للنشر**")
        else:
            # Current chat, replied content
            await event.delete()
            await _publish_loop(client, event.chat_id, reply, count, seconds)
            return
    else:
        # No reply -> tail can be either plain message (current chat)
        # or one/more targets followed by a message to send to those targets.
        if not tail:
            return await edit_delete(
                event,
                "⌔∮ لا يوجد رد على رسالة ولا نص لإرساله.\n"
                "- للارسال نص هنا: انشر <عدد> <ثواني> <نص>\n"
                "- للارسال الى هدف: انشر <عدد> <ثواني> <@يوزر/رابط/-100/ID> <نص>",
                9,
            )

        def _is_target(token: str) -> bool:
            token = token.strip()
            return (
                token.startswith("@")
                or token.startswith("https://t.me/")
                or token.startswith("-100")
                or token.isdigit()
            )

        tokens = tail.split()
        if _is_target(tokens[0]):
            # collect consecutive targets at the beginning
            i = 0
            targets = []
            while i < len(tokens) and _is_target(tokens[i]):
                targets.append(tokens[i])
                i += 1
            message_text = " ".join(tokens[i:]).strip()
            if not message_text:
                return await edit_delete(
                    event,
                    "⌔∮ يرجى إضافة نص بعد الأهداف لإرساله.\n"
                    "مثال: .نشر 5 6 @group1 @group2 رسالة الاختبار",
                    9,
                )
            await event.delete()
            ok = 0
            bad = []
            for t in targets:
                chat_id = await _resolve_chat_id(client, t)
                if chat_id is None:
                    bad.append(t)
                    continue
                await _publish_loop(client, chat_id, message_text, count, seconds)
                ok += 1
                await asyncio.sleep(1)
            if bad and ok:
                return await edit_or_reply(
                    event,
                    f"**᯽︙ تم النشر بنجاح في {ok} هدف ✅**\n**᯽︙ تعذر النشر في:** `{', '.join(bad)}`",
                )
            elif ok:
                return
            else:
                return await edit_or_reply(event, "**᯽︙ تعذر العثور على أي هدف صالح للنشر**")
        else:
            # plain message in current chat
            await event.delete()
            await _publish_loop(client, event.chat_id, tail, count, seconds)
            return

@l313l.ar_cmd(pattern="^(?:\.|)?وكف نشر$")
async def stop_publish_handler(event):
    global _publish_running
    _publish_running = False
    # clear global spamwork to signal other modules too
    delgvar("spamwork")
    await edit_or_reply(event, "**🛑 تم إيقاف جميع عمليات النشر بنجاح ✅**")
