"""
Email Service
Handles sending booking confirmations and other emails
"""

from datetime import datetime
from typing import Dict, Optional
import json


class EmailService:
    """Service for sending emails"""
    
    def __init__(self):
        self.sent_emails = []  # In production, use actual email service
    
    def send_booking_confirmation(
        self,
        booking_data: Dict,
        to_email: str = None,
        recipient_email: str = None
    ) -> Dict:
        """
        Send booking confirmation email
        
        Args:
            booking_data: Booking details
            recipient_email: Recipient email address
            
        Returns:
            Dict with send status
        """
        
        # Handle both parameter names for backward compatibility
        email_address = to_email or recipient_email
        if not email_address:
            raise ValueError("Either to_email or recipient_email must be provided")
        
        # Extract booking details
        first_name = booking_data.get('firstName', '')
        last_name = booking_data.get('lastName', '')
        service_category = booking_data.get('serviceCategory', 'General Consultation')
        preferred_date = booking_data.get('preferredDate', '')
        preferred_time = booking_data.get('preferredTime', '')
        consultation_type = booking_data.get('consultationType', 'video')
        company = booking_data.get('company', '')
        
        # Generate email content
        email_subject = "Booking Confirmation - Devonshire Green Consultation"
        
        email_body = self._generate_confirmation_email(
            first_name=first_name,
            last_name=last_name,
            service_category=service_category,
            preferred_date=preferred_date,
            preferred_time=preferred_time,
            consultation_type=consultation_type,
            company=company
        )
        
        # In production, send via SMTP or email service (SendGrid, AWS SES, etc.)
        # For now, log the email
        email_record = {
            "to": email_address,
            "subject": email_subject,
            "body": email_body,
            "sent_at": datetime.now().isoformat(),
            "type": "booking_confirmation",
            "status": "sent"
        }
        
        self.sent_emails.append(email_record)
        
        print(f"📧 Email sent to {email_address}: {email_subject}")
        
        return {
            "status": "success",
            "message": f"Confirmation email sent to {email_address}",
            "email_id": len(self.sent_emails)
        }
    
    def _generate_confirmation_email(
        self,
        first_name: str,
        last_name: str,
        service_category: str,
        preferred_date: str,
        preferred_time: str,
        consultation_type: str,
        company: str
    ) -> str:
        """Generate HTML email content"""
        
        consultation_type_display = {
            'video': 'Video Call (Link will be sent 24h before)',
            'phone': 'Phone Call',
            'in-person': 'In-Person at our Westerham office'
        }.get(consultation_type, 'Video Call')
        
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }}
        .booking-details {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #22c55e; }}
        .detail-row {{ margin: 10px 0; }}
        .label {{ font-weight: bold; color: #16a34a; }}
        .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 2px solid #e5e7eb; color: #6b7280; font-size: 14px; }}
        .button {{ display: inline-block; background: #22c55e; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 Booking Confirmed!</h1>
            <p>Your consultation with Devonshire Green is scheduled</p>
        </div>
        
        <div class="content">
            <p>Dear {first_name} {last_name},</p>
            
            <p>Thank you for booking a consultation with <strong>Devonshire Green</strong>. We're excited to discuss how we can help {company if company else 'your business'} achieve its accounting and compliance goals.</p>
            
            <div class="booking-details">
                <h3 style="margin-top: 0; color: #16a34a;">📅 Consultation Details</h3>
                
                <div class="detail-row">
                    <span class="label">Service:</span> {service_category}
                </div>
                
                <div class="detail-row">
                    <span class="label">Date:</span> {preferred_date}
                </div>
                
                <div class="detail-row">
                    <span class="label">Time:</span> {preferred_time}
                </div>
                
                <div class="detail-row">
                    <span class="label">Type:</span> {consultation_type_display}
                </div>
                
                {f'<div class="detail-row"><span class="label">Company:</span> {company}</div>' if company else ''}
            </div>
            
            <h3>What happens next?</h3>
            <ol>
                <li><strong>Confirmation Call:</strong> Our team will contact you within 24 hours to confirm the details</li>
                <li><strong>Preparation:</strong> We'll send you a brief questionnaire to understand your needs better</li>
                <li><strong>Meeting Link:</strong> For video calls, you'll receive the meeting link 24 hours before the consultation</li>
                <li><strong>Consultation:</strong> Meet with our expert accountant to discuss your requirements</li>
            </ol>
            
            <h3>Need to make changes?</h3>
            <p>If you need to reschedule or have any questions, please contact us:</p>
            <ul>
                <li>📞 Phone: 01959 565 772 / 020 8464 0493</li>
                <li>📧 Email: admin@devonshiregreen.uk</li>
            </ul>
            
            <div style="text-align: center;">
                <a href="https://devonshiregreen.uk" class="button">Visit Our Website</a>
            </div>
            
            <div class="footer">
                <p><strong>Devonshire Green</strong><br>
                Lodges Wood Oast, Goodley Stock Road<br>
                Westerham, Kent TN16 1TW<br>
                Company Number: 11492554</p>
                
                <p style="font-size: 12px; color: #9ca3af;">
                    This email was sent to confirm your consultation booking. If you did not make this booking, please contact us immediately.
                </p>
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    def send_welcome_email(self, user_email: str, user_name: str) -> Dict:
        """Send welcome email to new users"""
        
        email_record = {
            "to": user_email,
            "subject": "Welcome to FineGuard!",
            "body": f"Welcome {user_name}! Thank you for joining FineGuard.",
            "sent_at": datetime.now().isoformat(),
            "type": "welcome",
            "status": "sent"
        }
        
        self.sent_emails.append(email_record)
        
        return {
            "status": "success",
            "message": f"Welcome email sent to {user_email}"
        }
    
    def send_reminder_email(
        self,
        user_email: str,
        booking_data: Dict,
        hours_before: int = 24
    ) -> Dict:
        """Send reminder email before consultation"""
        
        email_record = {
            "to": user_email,
            "subject": f"Reminder: Consultation in {hours_before} hours",
            "body": f"Your consultation is scheduled for {booking_data.get('preferredDate')} at {booking_data.get('preferredTime')}",
            "sent_at": datetime.now().isoformat(),
            "type": "reminder",
            "status": "sent"
        }
        
        self.sent_emails.append(email_record)
        
        return {
            "status": "success",
            "message": f"Reminder email sent to {user_email}"
        }
    
    def get_sent_emails(self) -> list:
        """Get list of sent emails (for testing/debugging)"""
        return self.sent_emails


# Singleton instance
email_service = EmailService()

