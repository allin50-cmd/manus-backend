
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from app.db.database import Base

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    company_number = Column(String, unique=True, index=True)
    company_name = Column(String, nullable=False)
    status = Column(String)
    registered_address = Column(String)
    compliance_score = Column(Float, default=0.0)
    risk_level = Column(String, default="MEDIUM")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
