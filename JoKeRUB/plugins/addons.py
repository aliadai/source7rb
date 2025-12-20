from JoKeRUB import l313l
from telethon.tl.types import MessageEntityCustomEmoji


async def process_custom_emojis_ids(event):
    """استخراج الايموجيات المخصصة من الرسالة وإرجاعها كنصوص منسّقة."""

    message_text = event.message.message
    custom_emojis = []

    if event.entities:
        # تجنّب تكرار نفس الاوفست أكثر من مرة
        processed_offsets = set()

        for entity in event.entities:
            if isinstance(entity, MessageEntityCustomEmoji):
                if entity.offset not in processed_offsets:
                    try:
                        # قصّ الايموجي من النص بحسب الطول والاوفست
                        emoji = message_text[entity.offset : entity.offset + entity.length]
                        emoji_id = entity.document_id

                        if emoji and emoji_id:
                            # تنسيق عربي قريب من أسلوب باقي السورس
                            custom_emojis.append(
                                f"⌔︙ايدي الايموجي : `{emoji_id}` | الايموجي : {emoji} \n"
                                f"⌔︙رابطه : [{emoji}](emoji/{emoji_id})"
                            )
                            processed_offsets.add(entity.offset)
                    except Exception as e:
                        print(f"Error processing emoji: {e}")

    return custom_emojis