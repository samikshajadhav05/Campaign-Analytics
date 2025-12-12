from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import os 

from database import create_db_and_tables, SessionLocal, Campaign

class CampaignSchema(BaseModel):
    id: int
    name: str
    status: str
    clicks: int
    cost: float
    impressions: int

    class Config:
        from_attributes = True 

app = FastAPI(title="Campaign Analytics API")
CORS_STRING = os.environ.get(
    "CORS_ORIGINS"
)
origins = [o.strip().rstrip('/') for o in CORS_STRING.split(',')]

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
    campaigns = db.query(Campaign).all()
    
    if not campaigns:
        raise HTTPException(status_code=404, detail="Campaign data not found. Ensure the SQL setup script has been run.")
    
    return campaigns
