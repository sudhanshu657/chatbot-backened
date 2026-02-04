from fastapi import APIRouter, HTTPException
from .auth import USER_TOKENS
from ...services.gmail_service import get_gmail_service, fetch_last_emails, delete_email, send_email
from ...services.ai_service import summarize_email

router = APIRouter()



@router.get("/emails-with-summary")
def emails_with_summary():
    creds = USER_TOKENS.get("credentials")
    if not creds:
        raise HTTPException(status_code=401, detail="No credentials")

    emails = fetch_last_emails(creds, 5)

    for email in emails:
        email["summary"] = summarize_email(
            email["subject"],
            email["body"]
        )

    return emails


@router.get("/test-emails")
def test_emails():
    creds = USER_TOKENS.get("credentials")
    if not creds:
        raise HTTPException(status_code=401, detail="No credentials")
    emails = fetch_last_emails(creds, 5)
    return emails

@router.get("/last")
def get_last_emails_route():
    if "credentials" not in USER_TOKENS:
        raise HTTPException(status_code=401, detail="User not authenticated")
    return fetch_last_emails(USER_TOKENS["credentials"])

@router.delete("/{email_id}")
def delete_email_route(email_id: str):
    if "credentials" not in USER_TOKENS:
        raise HTTPException(status_code=401, detail="User not authenticated")
    service = get_gmail_service(USER_TOKENS["credentials"])
    delete_email(service, email_id)
    return {"status": "Email deleted"}

@router.post("/send")
def send_email_route(payload: dict):
    if "credentials" not in USER_TOKENS:
        raise HTTPException(status_code=401, detail="User not authenticated")
    service = get_gmail_service(USER_TOKENS["credentials"])
    send_email(service, payload["to"], payload["subject"], payload["body"])
    return {"status": "Email sent"}
