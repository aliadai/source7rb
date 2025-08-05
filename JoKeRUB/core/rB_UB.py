from telethon import TelegramClient
from telethon.sessions import StringSession
from .. import Config  # أو عدّل الاستيراد حسب مكان ملف Config

def rB_Pyro(string_session, logs):
    if not isinstance(string_session, str):
        raise ValueError("The given session must be a str or a Session instance.")
    client = TelegramClient(
        StringSession(string_session),
        api_id=Config.API_ID,
        api_hash=Config.API_HASH
    )
    return client