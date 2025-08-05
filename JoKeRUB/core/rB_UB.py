from telethon import TelegramClient

def rB_Pyro(string_session, logs):
    if not isinstance(string_session, str):
        raise ValueError("The given session must be a str or a Session instance.")
    client = TelegramClient(string_session, api_id=123456, api_hash='your_api_hash')
    return client