"""
Lead Model
Database model for CRM leads
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .base import Base


class LeadStatus(str, enum.Enum):
    """Lead status enum"""
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL_SENT = "proposal_sent"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"


class LeadPriority(str, enum.Enum):
    """Lead priority enum"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class LeadSource(str, enum.Enum):
    """Lead source enum"""
    AI_RECOMMENDATION = "ai_recommendation"
    BOOKING_FORM = "booking_form"
    WEBSITE_CONTACT = "website_contact"
    REFERRAL = "referral"
    DIRECT = "direct"


class Lead(Base):
    """Lead model"""
    __tablename__ = "leads"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(String, unique=True, index=True, nullable=False)
    
    # Source and status
    source = Column(Enum(LeadSource), nullable=False)
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW, nullable=False)
    priority = Column(Enum(LeadPriority), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Company information
    company_number = Column(String, index=True)
    company_name = Column(String, nullable=False)
    industry = Column(String)
    annual_turnover = Column(Float)
    employees = Column(Integer)
    
    # Contact information
    contact_email = Column(String, index=True, nullable=False)
    contact_phone = Column(String)
    contact_first_name = Column(String)
    contact_last_name = Column(String)
    
    # Lead scoring and metrics
    lead_score = Column(Integer, default=0)
    potential_value = Column(Float, default=0.0)
    
    # AI insights
    ai_confidence = Column(Integer)
    risk_level = Column(String)
    compliance_score = Column(Integer)
    
    # Services and recommendations
    recommended_services = Column(JSON)  # List of service names
    
    # Tracking
    touchpoints = Column(Integer, default=0)
    last_contact_date = Column(DateTime)
    next_follow_up_date = Column(DateTime)
    
    # Relationships
    activities = relationship("LeadActivity", back_populates="lead", cascade="all, delete-orphan")
    opportunities = relationship("Opportunity", back_populates="lead")
    
    # Opportunity reference (if converted)
    opportunity_id = Column(String)
    
    def __repr__(self):
        return f"<Lead {self.lead_id}: {self.company_name} ({self.status})>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "leadId": self.lead_id,
            "source": self.source.value if self.source else None,
            "status": self.status.value if self.status else None,
            "priority": self.priority.value if self.priority else None,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
            "companyNumber": self.company_number,
            "companyName": self.company_name,
            "industry": self.industry,
            "annualTurnover": self.annual_turnover,
            "employees": self.employees,
            "contactEmail": self.contact_email,
            "contactPhone": self.contact_phone,
            "contactFirstName": self.contact_first_name,
            "contactLastName": self.contact_last_name,
            "leadScore": self.lead_score,
            "potentialValue": self.potential_value,
            "aiConfidence": self.ai_confidence,
            "riskLevel": self.risk_level,
            "complianceScore": self.compliance_score,
            "recommendedServices": self.recommended_services,
            "touchpoints": self.touchpoints,
            "lastContactDate": self.last_contact_date.isoformat() if self.last_contact_date else None,
            "nextFollowUpDate": self.next_follow_up_date.isoformat() if self.next_follow_up_date else None,
            "opportunityId": self.opportunity_id
        }


class LeadActivity(Base):
    """Lead activity model"""
    __tablename__ = "lead_activities"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(String, unique=True, index=True, nullable=False)
    
    # Foreign key to lead
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    
    # Activity details
    activity_type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    activity_metadata = Column(JSON)  # Renamed from 'metadata' (reserved keyword)
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    lead = relationship("Lead", back_populates="activities")
    
    def __repr__(self):
        return f"<LeadActivity {self.activity_id}: {self.activity_type}>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "activityId": self.activity_id,
            "leadId": self.lead_id,
            "activityType": self.activity_type,
            "description": self.description,
            "metadata": self.activity_metadata,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }

