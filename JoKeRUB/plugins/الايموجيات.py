from JoKeRUB import l313l
from ..helpers import admin_cmd
from .xtelethon import CustomParseMode
from .addons import process_custom_emojis_ids


@l313l.on(admin_cmd(outgoing=True, pattern="تجربة$"))
async def _(event):
    await event.edit(
        """
✧ `.م1` [⚙️](emoji/5971846335085678067)  
✧ `.م2` [📟](emoji/5260640681906419699)  
✧ `.م3` [⛳️](emoji/5264710717470158023)  
✧ `.م4` [🛠](emoji/5863945989127148135)  
✧ `.م5` [🎯](emoji/5397782960512444700)  
✧ `.م6` [💰](emoji/5213094908608392768)  
✧ `.م7` [🎲](emoji/5879623757923881824)  
✧ `.م8` [🧩](emoji/5429368540849260641)  
""",
        link_preview=None,
        parse_mode=CustomParseMode("markdown"),
    )


@l313l.on(admin_cmd(outgoing=True, pattern="ايدي_ايموجي(?:\s+.*)?"))
async def _(event):
    custom_emojis = await process_custom_emojis_ids(event)

    if custom_emojis:
        # نرسل كل سطر لوحده عشان التنسيق ما يخرب
        for line in custom_emojis:
            await event.client.send_message(
                event.chat_id,
                line,
                parse_mode=CustomParseMode("markdown"),
            )
    else:
        await event.edit("⌔︙ما لقيت اي ايموجي مخصص بالرسالة.")
