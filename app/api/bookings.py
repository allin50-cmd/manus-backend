"""
Bookings API
Handles consultation booking requests
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import sys
sys.path.append('/home/ubuntu/fineguard-backend')

from app.services.email_service import email_service
from app.services.crm_integration import crm_integration

router = APIRouter()


class BookingRequest(BaseModel):
    """Booking request model"""
    # Personal Info
    firstName: str
    lastName: str
    email: EmailStr
    phone: str
    company: Optional[str] = None
    
    # Service Selection
    serviceCategory: str
    specificService: Optional[str] = None
    packageInterest: Optional[str] = None
    
    # Booking Details
    preferredDate: str
    preferredTime: str
    consultationType: str  # video, phone, in-person
    
    # Additional Info
    message: Optional[str] = None
    currentAccountant: bool = False
    annualTurnover: Optional[str] = None
    employees: Optional[str] = None


class BookingResponse(BaseModel):
    """Booking response model"""
    bookingId: str
    status: str
    message: str
    confirmationEmailSent: bool
    bookingDetails: dict


@router.post("/bookings", response_model=BookingResponse)
async def create_booking(booking: BookingRequest):
    """
    Create a new consultation booking
    
    Args:
        booking: Booking request data
        
    Returns:
        BookingResponse with confirmation details
    """
    
    # Generate booking ID
    booking_id = f"BK-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Prepare booking data
    booking_data = booking.dict()
    booking_data['bookingId'] = booking_id
    booking_data['createdAt'] = datetime.now().isoformat()
    booking_data['status'] = 'confirmed'
    
    # In production, save to database
    # For now, just log it
    print(f"📅 New booking created: {booking_id}")
    print(f"   Client: {booking.firstName} {booking.lastName}")
    print(f"   Email: {booking.email}")
    print(f"   Service: {booking.serviceCategory}")
    print(f"   Date: {booking.preferredDate} at {booking.preferredTime}")
    
    # Create CRM lead from booking
    crm_lead = crm_integration.create_lead_from_booking(booking_data)
    booking_data['crmLeadId'] = crm_lead.get('leadId')
    
    # Send confirmation email
    email_result = email_service.send_booking_confirmation(
        booking_data=booking_data,
        recipient_email=booking.email
    )
    
    confirmation_sent = email_result.get('status') == 'success'
    
    # Prepare response
    return BookingResponse(
        bookingId=booking_id,
        status="confirmed",
        message=f"Your consultation has been booked for {booking.preferredDate} at {booking.preferredTime}",
        confirmationEmailSent=confirmation_sent,
        bookingDetails={
            "bookingId": booking_id,
            "date": booking.preferredDate,
            "time": booking.preferredTime,
            "type": booking.consultationType,
            "service": booking.serviceCategory,
            "email": booking.email
        }
    )


@router.get("/bookings/{booking_id}")
async def get_booking(booking_id: str):
    """
    Get booking details
    
    Args:
        booking_id: Booking ID
        
    Returns:
        Booking details
    """
    
    # In production, fetch from database
    # For now, return demo data
    
    return {
        "bookingId": booking_id,
        "status": "confirmed",
        "message": "Booking found",
        "details": {
            "bookingId": booking_id,
            "createdAt": datetime.now().isoformat()
        }
    }


@router.put("/bookings/{booking_id}/reschedule")
async def reschedule_booking(booking_id: str, new_date: str, new_time: str):
    """
    Reschedule a booking
    
    Args:
        booking_id: Booking ID
        new_date: New preferred date
        new_time: New preferred time
        
    Returns:
        Updated booking details
    """
    
    # In production:
    # 1. Fetch booking from database
    # 2. Update date and time
    # 3. Send rescheduling confirmation email
    
    return {
        "bookingId": booking_id,
        "status": "rescheduled",
        "message": f"Booking rescheduled to {new_date} at {new_time}",
        "newDate": new_date,
        "newTime": new_time
    }


@router.delete("/bookings/{booking_id}")
async def cancel_booking(booking_id: str):
    """
    Cancel a booking
    
    Args:
        booking_id: Booking ID
        
    Returns:
        Cancellation confirmation
    """
    
    # In production:
    # 1. Fetch booking from database
    # 2. Mark as cancelled
    # 3. Send cancellation confirmation email
    
    return {
        "bookingId": booking_id,
        "status": "cancelled",
        "message": "Booking cancelled successfully"
    }


@router.get("/bookings/user/{user_email}")
async def get_user_bookings(user_email: str):
    """
    Get all bookings for a user
    
    Args:
        user_email: User email address
        
    Returns:
        List of user bookings
    """
    
    # In production, fetch from database
    # For now, return empty list
    
    return {
        "email": user_email,
        "bookings": [],
        "total": 0
    }

