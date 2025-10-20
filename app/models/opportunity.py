"""
Opportunity Model
Database model for sales opportunities
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .base import Base


class OpportunityStage(str, enum.Enum):
    """Opportunity stage enum"""
    DISCOVERY = "discovery"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"


class OpportunityStatus(str, enum.Enum):
    """Opportunity status enum"""
    OPEN = "open"
    WON = "won"
    LOST = "lost"


class Opportunity(Base):
    """Opportunity model"""
    __tablename__ = "opportunities"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    opportunity_id = Column(String, unique=True, index=True, nullable=False)
    
    # Foreign key to lead
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Opportunity details
    package = Column(String, nullable=False)  # Starter, Professional, Enterprise
    annual_value = Column(Float, nullable=False)
    probability = Column(Integer, nullable=False)  # 0-100
    expected_value = Column(Float, nullable=False)
    
    # Stage and status
    stage = Column(Enum(OpportunityStage), default=OpportunityStage.PROPOSAL, nullable=False)
    status = Column(Enum(OpportunityStatus), default=OpportunityStatus.OPEN, nullable=False)
    
    # Timeline
    expected_close_date = Column(DateTime)
    actual_close_date = Column(DateTime)
    
    # Company info (denormalized for quick access)
    company_name = Column(String)
    contact_email = Column(String)
    
    # Relationship
    lead = relationship("Lead", back_populates="opportunities")
    
    def __repr__(self):
        return f"<Opportunity {self.opportunity_id}: {self.package} - £{self.annual_value}>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "opportunityId": self.opportunity_id,
            "leadId": self.lead_id,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
            "package": self.package,
            "annualValue": self.annual_value,
            "probability": self.probability,
            "expectedValue": self.expected_value,
            "stage": self.stage.value if self.stage else None,
            "status": self.status.value if self.status else None,
            "expectedCloseDate": self.expected_close_date.isoformat() if self.expected_close_date else None,
            "actualCloseDate": self.actual_close_date.isoformat() if self.actual_close_date else None,
            "companyName": self.company_name,
            "contactEmail": self.contact_email
        }

