
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.database import get_db
from app.models.company import Company
from typing import List

router = APIRouter()

class CompanyCreate(BaseModel):
    company_number: str
    company_name: str
    status: str = "Active"
    registered_address: str = ""

class CompanyResponse(BaseModel):
    id: int
    company_number: str
    company_name: str
    status: str
    registered_address: str
    compliance_score: float
    risk_level: str
    
    class Config:
        from_attributes = True

@router.post("/", response_model=CompanyResponse)
async def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = Company(**company.dict(), user_id=1)  # TODO: Get from auth
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@router.get("/", response_model=List[CompanyResponse])
async def get_companies(db: Session = Depends(get_db)):
    companies = db.query(Company).all()
    return companies

@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company
