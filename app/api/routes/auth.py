from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from ...services.auth_service import create_oauth_flow
from ...core.config import settings
from ...core.logging import logger
from googleapiclient.discovery import build
import jwt
import time
import json
import os

router = APIRouter()

# Persist credentials to file for demo
CREDENTIALS_FILE = "user_credentials.json"

def save_credentials(data):
    # Serialize credentials
    if "credentials" in data:
        data = data.copy()
        data["credentials"] = data["credentials"].to_json()
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(data, f)

def load_credentials():
    try:
        if os.path.exists(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE, "r") as f:
                data = json.load(f)
            if "credentials" in data:
                from google.oauth2.credentials import Credentials
                data["credentials"] = Credentials.from_authorized_user_info(json.loads(data["credentials"]))
            return data
    except:
        pass  # Ignore errors, return empty
    return {}

USER_TOKENS = load_credentials()

@router.get("/google/login")
def google_login():
    flow = create_oauth_flow()
    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
    logger.info("Redirecting to Google OAuth login")
    return {"auth_url": auth_url}

@router.get("/google/callback")
def google_callback(request: Request):
    flow = create_oauth_flow()
    try:
        flow.fetch_token(authorization_response=str(request.url))
    except Exception as e:
        logger.error(f"OAuth callback failed: {e}")
        raise HTTPException(status_code=400, detail="Google authentication failed")

    credentials = flow.credentials

    # Get user info
    oauth_service = build('oauth2', 'v2', credentials=credentials)
    user_info = oauth_service.userinfo().get().execute()
    name = user_info.get('name')
    email = user_info.get('email')

    # Store credentials globally (for demo purposes)
    USER_TOKENS["credentials"] = credentials
    USER_TOKENS["user_info"] = user_info
    # Note: credentials not persisted for security, re-login after restart

    # Create JWT token
    payload = {
        "sub": email,
        "name": name,
        "email": email,
        "exp": int(time.time()) + 3600
    }
    token = jwt.encode(payload, settings.SESSION_SECRET, algorithm="HS256")

    # Set cookie and redirect
    response = RedirectResponse(url=f"{settings.FRONTEND_URL}/dashboard")
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax"
    )

    logger.info("Google OAuth successful, token issued")
    return response

@router.get("/me")
def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, settings.SESSION_SECRET, algorithms=["HS256"])
        return {"user_id": payload["sub"], "name": payload["name"], "email": payload["email"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")