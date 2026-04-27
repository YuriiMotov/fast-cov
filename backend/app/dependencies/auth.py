import hmac
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from app.config import get_settings

api_key_header = APIKeyHeader(name="token")


async def verify_api_key(token: Annotated[str, Depends(api_key_header)]) -> str:
    if not hmac.compare_digest(token, get_settings().api_key.get_secret_value()):
        raise HTTPException(status_code=403, detail="Invalid API key")
    return token
