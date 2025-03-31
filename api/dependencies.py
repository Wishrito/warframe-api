from fastapi import HTTPException, Request

from utils import is_browser
from database import SessionLocal

def browser_only(request: Request):
    """Dependency that only allows browser requests"""
    user_agent = request.headers.get("User-Agent", "")
    if not is_browser(user_agent):
        raise HTTPException(status_code=403, detail="This endpoint is only available for browsers")
    return True

def api_client_only(request: Request):
    """Dependency that only allows API client requests"""
    user_agent = request.headers.get("User-Agent", "")
    if is_browser(user_agent):
        raise HTTPException(status_code=403, detail="This endpoint is only available for API clients")
    return True

def get_client_info(request: Request):
    """Dependency that provides client information"""
    user_agent = request.headers.get("User-Agent", "")
    return {
        "is_browser": is_browser(user_agent),
        "user_agent": user_agent
    }


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
