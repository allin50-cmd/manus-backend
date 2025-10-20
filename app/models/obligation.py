
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.sql import func
from app.db.database import Base

class Obligation(Base):
    __tablename__ = "obligations"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    title = Column(String, nullable=False)
    description = Column(String)
    due_date = Column(DateTime)
    status = Column(String, default="PENDING")
    potential_penalty = Column(Float, default=0.0)
    is_overdue = Column(Boolean, default=False)
    days_overdue = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
