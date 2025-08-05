def rB_Pyro(string_session, logs):
    print(f"Session created with: {string_session} and logs: {logs}")
    return {"session": string_session, "logs": logs}