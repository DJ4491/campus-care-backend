from jose import jwk, jwt
from jose.utils import base64url_decode
import httpx
from typing import Any
from typing import Dict, Any, Optional
from app.core.config import settings
from fastapi import HTTPException, status

_jwks_cache: Optional[Dict[str, Any]] = None


async def fetch_jwks() -> Dict[str, Any]:
    global _jwks_cache

    if _jwks_cache is not None:
        return _jwks_cache

    async with httpx.AsyncClient() as client:
        r = await client.get(settings.JWKS_URL)
        r.raise_for_status()
        _jwks_cache = r.json()

    return _jwks_cache


async def verify_jwt(token: str) -> dict[str, Any]:
    # Parse header to get 'kid'
    headers = jwt.get_unverified_header(token)
    kid = headers.get("kid")
    jwks = await fetch_jwks()
    keys = jwks.get("keys", [])
    key_data = next((k for k in keys if k.get("kid") == kid), None)
    if key_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token (kid)."
        )

    # Construct public key
    public_key = jwk.construct(key_data)
    message, encoded_sig = token.rsplit(".", 1)
    decoded_sig = base64url_decode(encoded_sig.encode("utf-8"))

    if not public_key.verify(message.encode("utf-8"), decoded_sig):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token (signature).",
        )

    # Validate claims (simple)
    payload = jwt.get_unverified_claims(token)
    # candidate checks: exp, aud, iss
    if payload.get("aud") != settings.AUDIENCE or payload.get("iss") != settings.ISSUER:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token (claims)."
        )
    return payload
