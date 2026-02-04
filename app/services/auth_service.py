import os
from google_auth_oauthlib.flow import Flow
from ..core.config import settings

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
]

def create_oauth_flow():
    return Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri=f"{settings.BACKEND_URL}/auth/google/callback",
    )
