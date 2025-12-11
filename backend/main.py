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

app = FastAPI(title="Campaign Analytics API")

origins = [
    "http://localhost:3000",  
    "http://127.0.0.1:3000",
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

def populate_db(db: Session):
    """Inserts the 10 required sample campaigns if the table is empty."""
    if db.query(Campaign).count() > 0:
        return

    sample_campaigns = [
        Campaign(id=1, name='Summer Sale Q3 Launch', status='Active', clicks=1500, cost=45.99, impressions=10000),
        Campaign(id=2, name='Black Friday Retargeting', status='Paused', clicks=3200, cost=89.50, impressions=25000),
        Campaign(id=3, name='New User Acquisition', status='Active', clicks=850, cost=12.30, impressions=5000),
        Campaign(id=4, name='Holiday Promo 2025', status='Active', clicks=4500, cost=150.75, impressions=45000),
        Campaign(id=5, name='Brand Awareness Test A', status='Paused', clicks=120, cost=5.25, impressions=2000),
        Campaign(id=6, name='Spring Collection Beta', status='Active', clicks=210, cost=19.99, impressions=3000),
        Campaign(id=7, name='Clearance Flash Sale', status='Paused', clicks=5000, cost=200.00, impressions=60000),
        Campaign(id=8, name='Email List Growth Campaign', status='Active', clicks=900, cost=30.15, impressions=9000),
        Campaign(id=9, name='Social Media Engagement', status='Active', clicks=110, cost=8.80, impressions=1500),
        Campaign(id=10, name='Winter Catalog Pre-Order', status='Paused', clicks=700, cost=75.40, impressions=18000),
    ]
    
    db.add_all(sample_campaigns)
    db.commit()

@app.on_event("startup")
def on_startup():
    """Executed when the application starts."""
    create_db_and_tables() 
    
    db = SessionLocal()
    populate_db(db)
    db.close()

@app.get("/campaigns", response_model=List[CampaignSchema])
def read_campaigns(db: Session = Depends(get_db)):
    """
    Returns a JSON list of all marketing campaigns from the database.
    """
    campaigns = db.query(Campaign).all()
    
    if not campaigns:
        raise HTTPException(status_code=404, detail="Campaign data not found.")
    
    return campaigns