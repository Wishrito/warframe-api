from typing import List, Optional

from dependencies import api_client_only, browser_only, get_client_info, get_db
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from models import (
    Ability,
    AbilityCreate,
    Mod,
    ModCreate,
    Warframe,
    WarframeCreate,
    Weapon,
    WeaponCreate,
)
from schemas import AbilityResponse, ModResponse, WarframeResponse, WeaponResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from utils import is_browser

# FastAPI app
app = FastAPI(title="Warframe API", description="API for Warframe game data")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Client type detection middleware
class ClientDetectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Get User-Agent
        user_agent = request.headers.get("User-Agent", "")
        # Add client_type to request state
        request.state.is_browser = is_browser(user_agent)
        request.state.user_agent = user_agent
        # Continue processing the request
        response = await call_next(request)
        return response

# Add the middleware to the app
app.add_middleware(ClientDetectionMiddleware)

# Example route that behaves differently based on client type
@app.get("/")
def read_root(request: Request):
    if request.state.is_browser:
        # Return HTML for browsers
        html_content = """
        <!DOCTYPE html>
        <html>
            <head>
                <title>Warframe API</title>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                    h1 { color: #333; }
                    .endpoint { background: #f4f4f4; padding: 10px; margin: 10px 0; border-radius: 5px; }
                </style>
            </head>
            <body>
                <h1>Welcome to the Warframe API</h1>
                <p>This API provides data about Warframe game elements.</p>
                <h2>Available Endpoints:</h2>
                <div class="endpoint">/warframes - Get all warframes</div>
                <div class="endpoint">/weapons - Get all weapons</div>
                <div class="endpoint">/mods - Get all mods</div>
                <p>For full documentation, visit <a href="/docs">/docs</a></p>
            </body>
        </html>
        """
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=html_content)
    # Return JSON for API clients
    return {
        "message": "Welcome to the Warframe API!",
        "documentation": "/docs",
        "endpoints": {
            "warframes": "/warframes",
            "weapons": "/weapons",
            "mods": "/mods",
        },
    }

# Example of a browser-only endpoint
@app.get("/browser-dashboard", dependencies=[Depends(browser_only)])
def browser_dashboard():
    """This endpoint can only be accessed by browsers"""
    return {
        "message": "This is a browser-only dashboard",
        "data": {
            "warframes_count": 42,
            "weapons_count": 137,
            "mods_count": 312
        }
    }

# Example of an API-client-only endpoint
@app.get("/api-stats", dependencies=[Depends(api_client_only)])
def api_stats():
    """This endpoint can only be accessed by API clients"""
    return {
        "api_version": "1.0.0",
        "rate_limit": 100,
        "endpoints_count": 15
    }

# Example of an endpoint that adapts to client type
@app.get("/adaptive-endpoint")
def adaptive_endpoint(client_info: dict = Depends(get_client_info)):
    if client_info["is_browser"]:
        return {"message": "Hello Browser User!", "client": "browser"}
    else:
        return {"message": "Hello API User!", "client": "api"}

# Warframe endpoints
@app.post("/warframes/", response_model=WarframeResponse, tags=["Warframes"])
def create_warframe(warframe: WarframeCreate, db: Session = Depends(get_db)):
    db_warframe = Warframe(**warframe.dict())
    db.add(db_warframe)
    db.commit()
    db.refresh(db_warframe)
    return db_warframe

@app.get("/warframes/", response_model=List[WarframeResponse], tags=["Warframes"])
def read_warframes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    warframes = db.query(Warframe).offset(skip).limit(limit).all()
    return warframes

@app.get("/warframes/{warframe_id}", response_model=WarframeResponse, tags=["Warframes"])
def read_warframe(warframe_id: int, db: Session = Depends(get_db)):
    db_warframe = db.query(Warframe).filter(Warframe.id == warframe_id).first()
    if db_warframe is None:
        raise HTTPException(status_code=404, detail="Warframe not found")
    return db_warframe

@app.put("/warframes/{warframe_id}", response_model=WarframeResponse, tags=["Warframes"])
def update_warframe(warframe_id: int, warframe: WarframeCreate, db: Session = Depends(get_db)):
    db_warframe = db.query(Warframe).filter(Warframe.id == warframe_id).first()
    if db_warframe is None:
        raise HTTPException(status_code=404, detail="Warframe not found")
    
    for key, value in warframe.dict().items():
        setattr(db_warframe, key, value)
    
    db.commit()
    db.refresh(db_warframe)
    return db_warframe

@app.delete("/warframes/{warframe_id}", tags=["Warframes"])
def delete_warframe(warframe_id: int, db: Session = Depends(get_db)):
    db_warframe = db.query(Warframe).filter(Warframe.id == warframe_id).first()
    if db_warframe is None:
        raise HTTPException(status_code=404, detail="Warframe not found")
    
    db.delete(db_warframe)
    db.commit()
    return {"message": "Warframe deleted successfully"}

# Ability endpoints
@app.post("/abilities/", response_model=AbilityResponse, tags=["Abilities"])
def create_ability(ability: AbilityCreate, db: Session = Depends(get_db)):
    db_ability = Ability(**ability.dict())
    db.add(db_ability)
    db.commit()
    db.refresh(db_ability)
    return db_ability

@app.get("/abilities/", response_model=List[AbilityResponse], tags=["Abilities"])
def read_abilities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    abilities = db.query(Ability).offset(skip).limit(limit).all()
    return abilities

# Weapon endpoints
@app.post("/weapons/", response_model=WeaponResponse, tags=["Weapons"])
def create_weapon(weapon: WeaponCreate, db: Session = Depends(get_db)):
    db_weapon = Weapon(**weapon.dict())
    db.add(db_weapon)
    db.commit()
    db.refresh(db_weapon)
    return db_weapon

@app.get("/weapons/", response_model=List[WeaponResponse], tags=["Weapons"])
def read_weapons(
    skip: int = 0, 
    limit: int = 100, 
    weapon_type: Optional[str] = Query(None, description="Filter by weapon type (Primary, Secondary, Melee)"),
    db: Session = Depends(get_db)
):
    query = db.query(Weapon)
    if weapon_type:
        query = query.filter(Weapon.type == weapon_type)
    weapons = query.offset(skip).limit(limit).all()
    return weapons

@app.get("/weapons/{weapon_id}", response_model=WeaponResponse, tags=["Weapons"])
def read_weapon(weapon_id: int, db: Session = Depends(get_db)):
    db_weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first()
    if db_weapon is None:
        raise HTTPException(status_code=404, detail="Weapon not found")
    return db_weapon

# Mod endpoints
@app.post("/mods/", response_model=ModResponse, tags=["Mods"])
def create_mod(mod: ModCreate, db: Session = Depends(get_db)):
    db_mod = Mod(**mod.dict())
    db.add(db_mod)
    db.commit()
    db.refresh(db_mod)
    return db_mod

@app.get("/mods/", response_model=List[ModResponse], tags=["Mods"])
def read_mods(
    skip: int = 0, 
    limit: int = 100, 
    mod_type: Optional[str] = Query(None, description="Filter by mod type"),
    rarity: Optional[str] = Query(None, description="Filter by rarity"),
    db: Session = Depends(get_db)
):
    query = db.query(Mod)
    if mod_type:
        query = query.filter(Mod.type == mod_type)
    if rarity:
        query = query.filter(Mod.rarity == rarity)
    mods = query.offset(skip).limit(limit).all()
    return mods

@app.get("/mods/{mod_id}", response_model=ModResponse, tags=["Mods"])
def read_mod(mod_id: int, db: Session = Depends(get_db)):
    db_mod = db.query(Mod).filter(Mod.id == mod_id).first()
    if db_mod is None:
        raise HTTPException(status_code=404, detail="Mod not found")
    return db_mod

# Add ability to warframe
@app.post("/warframes/{warframe_id}/abilities/{ability_id}", tags=["Warframes"])
def add_ability_to_warframe(warframe_id: int, ability_id: int, db: Session = Depends(get_db)):
    db_warframe = db.query(Warframe).filter(Warframe.id == warframe_id).first()
    if db_warframe is None:
        raise HTTPException(status_code=404, detail="Warframe not found")
        
    db_ability = db.query(Ability).filter(Ability.id == ability_id).first()
    if db_ability is None:
        raise HTTPException(status_code=404, detail="Ability not found")
    
    db_warframe.abilities.append(db_ability)
    db.commit()
    return {"message": "Ability added to warframe successfully"}

# Create handler for AWS Lambda (required for Vercel)
handler = Mangum(app)
