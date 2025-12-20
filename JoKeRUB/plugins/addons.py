
from telethon.tl.types import MessageEntityCustomEmoji

async def process_custom_emojis_ids(event):
    message_text = event.message.message
    custom_emojis = []
    
    if event.entities:
        # List to keep track of processed offsets to avoid duplicate processing
        processed_offsets = set()
        
        # Iterate through all message entities
        for entity in event.entities:
            if isinstance(entity, MessageEntityCustomEmoji):
                if entity.offset not in processed_offsets:
                    try:
                        # Extract emoji and its ID from the message
                        emoji = message_text[entity.offset:entity.offset + entity.length]
                        emoji_id = entity.document_id
                        
                        # Ensure emoji and emoji_id are valid
                        if emoji and emoji_id:
                            custom_emojis.append(f"Custom Emoji ID: {emoji_id} | Emoji: {emoji} FOR: [{emoji}](emoji/{emoji_id})")
                            # Mark this offset as processed
                            processed_offsets.add(entity.offset)
                    except Exception as e:
                        print(f"Error processing emoji: {e}")
    
    return custom_emojis

