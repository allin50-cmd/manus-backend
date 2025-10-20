"""
Booking Model
Database model for consultation bookings
"""

from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
import enum

from .base import Base


class BookingStatus(str, enum.Enum):
    """Booking status enum"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ConsultationType(str, enum.Enum):
    """Consultation type enum"""
    PHONE = "phone"
    VIDEO = "video"
    IN_PERSON = "in_person"


class Booking(Base):
    """Booking model"""
    __tablename__ = "bookings"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(String, unique=True, index=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Contact information
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    phone = Column(String)
    company = Column(String)
    
    # Booking details
    service_category = Column(String, nullable=False)
    package_interest = Column(String)
    consultation_type = Column(Enum(ConsultationType), nullable=False)
    
    # Schedule
    preferred_date = Column(DateTime, nullable=False)
    preferred_time = Column(String, nullable=False)
    
    # Status
    status = Column(Enum(BookingStatus), default=BookingStatus.CONFIRMED, nullable=False)
    
    # Additional info
    current_accountant = Column(Integer, default=0)  # SQLite doesn't have boolean
    annual_turnover = Column(String)
    employees = Column(Integer)
    message = Column(String)
    
    # CRM integration
    crm_lead_id = Column(String)
    
    def __repr__(self):
        return f"<Booking {self.booking_id}: {self.first_name} {self.last_name}>"
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "bookingId": self.booking_id,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "company": self.company,
            "serviceCategory": self.service_category,
            "packageInterest": self.package_interest,
            "consultationType": self.consultation_type.value if self.consultation_type else None,
            "preferredDate": self.preferred_date.isoformat() if self.preferred_date else None,
            "preferredTime": self.preferred_time,
            "status": self.status.value if self.status else None,
            "currentAccountant": bool(self.current_accountant),
            "annualTurnover": self.annual_turnover,
            "employees": self.employees,
            "message": self.message,
            "crmLeadId": self.crm_lead_id
        }

