import os
from fastapi import Header, HTTPException

EXPECTED_TOKEN = os.getenv("API_TOKEN", "your-secret-api-token-here")

def verify_token(x_api_token: str = Header(..., alias="x-api-token")):
    if x_api_token != EXPECTED_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Token."
        )
    return True
