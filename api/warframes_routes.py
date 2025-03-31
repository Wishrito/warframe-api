from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from database import get_db
from models import Warframe
from schemas import WarframeResponse
from utils import is_browser

router = APIRouter()

@router.get("/", response_model=List[WarframeResponse])
def read_warframes(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Get User-Agent
    user_agent = request.headers.get("User-Agent", "")
    
    # Check if it's a browser
    if is_browser(user_agent):
        # Maybe apply different pagination for browsers
        if limit > 20:
            limit = 20  # Restrict page size for browsers to avoid large pages
    else:
        # API clients might have different rate limits or capabilities
        pass
    
    # Log the client type (in a real app, use proper logging)
    print(f"Request from {'browser' if is_browser(user_agent) else 'API client'}: {user_agent}")
    
    # Continue with the regular logic
    warframes = db.query(Warframe).offset(skip).limit(limit).all()
    return warframes
