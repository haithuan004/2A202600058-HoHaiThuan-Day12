from fastapi import Header, HTTPException, Request
from .config import settings

async def verify_api_key(request: Request, x_api_key: str = Header(None, alias="X-API-Key")):
    if not x_api_key or x_api_key != settings.AGENT_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return "authorized"
