def rB_Pyro(string_session, logs):
    if not isinstance(string_session, str):
        raise ValueError("The given session must be a str or a Session instance.")
    print(f"Session created with: {string_session} and logs: {logs}")
    return {"session": string_session, "logs": logs}