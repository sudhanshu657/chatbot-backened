def parse_command(user_message: str):
    msg = user_message.lower()

    if ("email" in msg or "emails" in msg) and ("read" in msg or "show" in msg or "get" in msg or "latest" in msg or "recent" in msg or "last" in msg):
        return {"action": "read"}

    if "delete" in msg or "remove" in msg:
        return {"action": "delete"}

    if "reply" in msg or "respond" in msg:
        return {"action": "reply"}

    return {"action": "unknown"}
