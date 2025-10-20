
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.database import get_db
from app.models.obligation import Obligation
from typing import List
from datetime import datetime

router = APIRouter()

class ObligationCreate(BaseModel):
    company_id: int
    title: str
    description: str = ""
    due_date: datetime
    potential_penalty: float = 0.0

class ObligationResponse(BaseModel):
    id: int
    company_id: int
    title: str
    description: str
    due_date: datetime
    status: str
    potential_penalty: float
    is_overdue: bool
    days_overdue: int
    
    class Config:
        from_attributes = True

@router.post("/", response_model=ObligationResponse)
async def create_obligation(obligation: ObligationCreate, db: Session = Depends(get_db)):
    db_obligation = Obligation(**obligation.dict())
    db.add(db_obligation)
    db.commit()
    db.refresh(db_obligation)
    return db_obligation

@router.get("/", response_model=List[ObligationResponse])
async def get_obligations(db: Session = Depends(get_db)):
    obligations = db.query(Obligation).all()
    return obligations
