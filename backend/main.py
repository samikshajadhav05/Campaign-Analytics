from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from .database import create_db_and_tables, SessionLocal, Campaign

class CampaignSchema(BaseModel):
    id: int
    name: str
    status: str
    clicks: int
    cost: float
    impressions: int

    class Config:
        from_attributes = True

app = FastAPI(title="Grippi Campaign Analytics API")

origins = [
    "http://localhost:3000",  
    "https://your-vercel-frontend.vercel.app", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/campaigns", response_model=List[CampaignSchema])
def read_campaigns(db: Session = Depends(get_db)):
    """
    Returns a JSON list of all marketing campaigns.
    """
    campaigns = db.query(Campaign).all()
    
    if not campaigns:
        raise HTTPException(status_code=404, detail="Campaign data not found. Please run the SQL setup script.")
    
    return campaigns