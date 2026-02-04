import base64
from googleapiclient.discovery import build


# Extract plain text body from Gmail payload
def extract_body(payload):
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                data = part["body"].get("data")
                if data:
                    return base64.urlsafe_b64decode(data).decode()

    if payload.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(
            payload["body"]["data"]
        ).decode()

    return ""


def fetch_last_emails(credentials, limit=5):
    service = build("gmail", "v1", credentials=credentials)

    results = service.users().messages().list(
        userId="me",
        maxResults=limit
    ).execute()

    messages = results.get("messages", [])

    emails = []

    for msg in messages:
        full_msg = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        headers = full_msg["payload"]["headers"]

        subject = next(
            (h["value"] for h in headers if h["name"] == "Subject"),
            "No Subject"
        )

        sender = next(
            (h["value"] for h in headers if h["name"] == "From"),
            "Unknown"
        )

        body = extract_body(full_msg["payload"])

        emails.append({
            "id": msg["id"],
            "subject": subject,
            "sender": sender,
            "body": body
        })

    return emails


def get_gmail_service(credentials):
    return build("gmail", "v1", credentials=credentials)


def send_email(credentials, to, subject, body):
    service = get_gmail_service(credentials)
    message = {
        "raw": base64.urlsafe_b64encode(
            f"To: {to}\nSubject: {subject}\n\n{body}".encode()
        ).decode()
    }
    service.users().messages().send(userId="me", body=message).execute()


def delete_email(credentials, email_id):
    service = get_gmail_service(credentials)
    service.users().messages().trash(userId="me", id=email_id).execute()