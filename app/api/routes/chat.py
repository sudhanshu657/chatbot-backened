from fastapi import APIRouter, HTTPException
from .auth import USER_TOKENS
from ...services.gmail_service import get_gmail_service, fetch_last_emails, delete_email, send_email
from ...services.ai_service import summarize_email, generate_reply
from ...utils.command_parser import parse_command



router = APIRouter()

@router.post("/")
def chat(payload: dict):
    user_message = payload.get("message", "").strip()
    if "credentials" not in USER_TOKENS:
        raise HTTPException(status_code=401, detail="User not authenticated")

    credentials = USER_TOKENS["credentials"]

    # Check for confirmation
    pending = USER_TOKENS.get("pending")
    if pending and user_message.lower() in ["yes", "confirm", "send"]:
        if pending["type"] == "reply":
            try:
                send_email(credentials, pending["to"], pending["subject"], pending["reply"])
                USER_TOKENS["pending"] = None
                return {"reply": "Reply sent successfully!"}
            except Exception as e:
                return {"reply": f"Failed to send reply: {str(e)}"}
        elif pending["type"] == "delete":
            try:
                delete_email(credentials, pending["email_id"])
                USER_TOKENS["pending"] = None
                return {"reply": "Email deleted successfully!"}
            except Exception as e:
                return {"reply": f"Failed to delete email: {str(e)}"}

    command = parse_command(user_message)

    if command["action"] == "read":
        emails = fetch_last_emails(credentials)
        response_lines = []
        for idx, email in enumerate(emails, start=1):
            summary = summarize_email(email["subject"], email["body"])
            response_lines.append(
                f"{idx}. From: {email['sender']}\nSubject: {email['subject']}\nSummary: {summary}"
            )
        return {"reply": "\n\n".join(response_lines), "emails": emails}

    elif command["action"] == "reply":
        emails = fetch_last_emails(credentials)
        if emails:
            email = emails[0]
            reply_text = generate_reply(email["subject"], email["body"])
            # Extract recipient from sender (simple: assume reply to sender)
            to = email["sender"].split("<")[-1].strip(">")
            subject = f"Re: {email['subject']}"
            USER_TOKENS["pending"] = {
                "type": "reply",
                "to": to,
                "subject": subject,
                "reply": reply_text
            }
            return {"reply": f"Suggested reply to '{email['subject']}':\n\n{reply_text}\n\nType 'yes' to send."}
        return {"reply": "No emails found to reply to."}

    elif command["action"] == "delete":
        emails = fetch_last_emails(credentials)
        if emails:
            email = emails[0]
            USER_TOKENS["pending"] = {
                "type": "delete",
                "email_id": email["id"]
            }
            return {"reply": f"Are you sure you want to delete '{email['subject']}'? Type 'yes' to confirm."}
        return {"reply": "No emails found to delete."}

    return {"reply": "I didn't understand that. Try 'read latest emails', 'reply to email', or 'delete email'."}
