from telethon import TelegramClient
from telethon.sessions import StringSession
from JoKeRUB.exampleconfig import APP_ID, APP_HASH, STRING_SESSION  # عدل المسار إذا لزم

def rB_Pyro(string_session, logs):
    if not isinstance(string_session, str):
        raise ValueError("The given session must be a str or a Session instance.")
    client = TelegramClient(
        StringSession(string_session),
        api_id=APP_ID,
        api_hash=APP_HASH
    )
    return client