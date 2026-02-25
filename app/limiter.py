from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request
from app.auth.auth import decode_access_token


def get_user_id_from_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.removeprefix("Bearer ").strip()
    payload = decode_access_token(token)
    if payload and "sub" in payload:
        return f"user:{payload['sub']}"
    return get_remote_address(request)


limiter = Limiter(key_func=get_remote_address)
user_limiter = Limiter(key_func=get_user_id_from_token)
