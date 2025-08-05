from pyrogram import Client

def rB_Pyro(string_session, logs):
    if not isinstance(string_session, str):
        raise ValueError("The given session must be a str or a Session instance.")
    app = Client(string_session, logger=logs)
    return app