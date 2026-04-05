from fastapi import Depends, HTTPException, Request
from firebase_admin import auth as firebase_auth
import firebase_admin

if not firebase_admin._apps:
    firebase_admin.initialize_app()


def _get_uid_from_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authorization header")
    token = auth_header.split("Bearer ")[1]
    try:
        decoded = firebase_auth.verify_id_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return decoded["uid"]


require_auth = Depends(_get_uid_from_token)
