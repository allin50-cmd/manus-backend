"""
Database Models
SQLAlchemy models for FineGuard platform
"""

from .base import Base, engine, SessionLocal, get_db, init_db, drop_db
from .lead import Lead, LeadActivity, LeadStatus, LeadPriority, LeadSource
from .opportunity import Opportunity, OpportunityStage, OpportunityStatus
from .booking import Booking, BookingStatus, ConsultationType
from .user import User
from .company import Company
from .obligation import Obligation

__all__ = [
    # Base
    'Base',
    'engine',
    'SessionLocal',
    'get_db',
    'init_db',
    'drop_db',
    
    # Lead
    'Lead',
    'LeadActivity',
    'LeadStatus',
    'LeadPriority',
    'LeadSource',
    
    # Opportunity
    'Opportunity',
    'OpportunityStage',
    'OpportunityStatus',
    
    # Booking
    'Booking',
    'BookingStatus',
    'ConsultationType',
    
    # User and Company
    'User',
    'Company',
    'Obligation'
]

