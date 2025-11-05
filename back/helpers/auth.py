from datetime import datetime, timedelta, timezone
import hashlib
import hmac
from typing import Any, Optional
import os
import jwt
import secrets
import uuid

ACCESS_SECRET_KEY = os.getenv("JWT_ACCESS_SECRET_KEY", "supersecretkey1")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_EXPIRE_MINUTES", 8))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("JWT_REFRESH_EXPIRE_DAYS", 7))
PEPPER = os.getenv("REFRESH_TOKEN_PEPPER").encode()


def _create_token(data: dict, secret: str, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, secret, algorithm=ALGORITHM)

def create_access_token(data: dict) -> str:
    return _create_token(
        data=data,
        secret=ACCESS_SECRET_KEY,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

def create_refresh_token(user_id: int, sid: Optional[str] = None, device_name: Optional[str] = None) -> dict[str,Any]:
    token = secrets.token_urlsafe(32)
    token_hash = hash_token(token)
    return {
        "token": token,
        "token_hash": token_hash,
        "user_id": user_id,
        "sid" : sid or str(uuid.uuid4()),
        "issued_at": datetime.now(timezone.utc),
        "expires_at": datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_MINUTES),
        "revoked": False,
        "device_name": device_name
        } 


def hash_token(token:str)->str:
    return hmac.new(PEPPER, token.encode(), hashlib.sha256).hexdigest()


def decode_access_token(token: str) -> dict|None:
    try:
        return jwt.decode(token, ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

