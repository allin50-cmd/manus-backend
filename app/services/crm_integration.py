"""
CRM Integration Service
Links accounting service recommendations to CRM for lead tracking
"""

from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class LeadStatus(str, Enum):
    """Lead status enum"""
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL_SENT = "proposal_sent"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"


class LeadSource(str, Enum):
    """Lead source enum"""
    AI_RECOMMENDATION = "ai_recommendation"
    BOOKING_FORM = "booking_form"
    WEBSITE_CONTACT = "website_contact"
    REFERRAL = "referral"
    DIRECT = "direct"


class CRMIntegration:
    """Service for CRM integration and lead management"""
    
    def __init__(self):
        self.leads = []  # In production, use actual CRM API
        self.activities = []
        self.opportunities = []
    
    def create_lead_from_ai_recommendation(
        self,
        company_data: Dict,
        recommendations: List[Dict],
        user_email: str
    ) -> Dict:
        """
        Create CRM lead from AI recommendation
        
        Args:
            company_data: Company information
            recommendations: AI recommendations
            user_email: User email address
            
        Returns:
            Created lead details
        """
        
        # Calculate lead score based on recommendations
        lead_score = self._calculate_lead_score(company_data, recommendations)
        
        # Determine priority
        priority = self._determine_priority(lead_score, recommendations)
        
        # Extract recommended services
        services = [rec['service'] for rec in recommendations]
        
        # Calculate potential value
        potential_value = self._calculate_potential_value(
            company_data,
            recommendations
        )
        
        # Create lead
        lead = {
            "leadId": f"LEAD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "source": LeadSource.AI_RECOMMENDATION,
            "status": LeadStatus.NEW,
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat(),
            
            # Company info
            "companyNumber": company_data.get('companyNumber'),
            "companyName": company_data.get('name'),
            "industry": company_data.get('industry'),
            "annualTurnover": company_data.get('annualTurnover'),
            "employees": company_data.get('employees'),
            
            # Contact info
            "email": user_email,
            "contactEmail": user_email,  # Alias for compatibility
            
            # Lead details
            "leadScore": lead_score,
            "priority": priority,
            "recommendedServices": services,
            "potentialValue": potential_value,
            
            # AI insights
            "aiConfidence": self._get_overall_confidence(recommendations),
            "riskLevel": company_data.get('riskLevel'),
            "complianceScore": company_data.get('complianceScore'),
            
            # Tracking
            "touchpoints": 0,
            "lastContactDate": None,
            "nextFollowUpDate": self._calculate_follow_up_date(priority)
        }
        
        self.leads.append(lead)
        
        # Create initial activity
        self._log_activity(
            lead_id=lead['leadId'],
            activity_type="lead_created",
            description=f"Lead created from AI recommendation with {len(services)} services",
            metadata={
                "services": services,
                "confidence": lead['aiConfidence'],
                "score": lead_score
            }
        )
        
        print(f"📊 CRM Lead created: {lead['leadId']}")
        print(f"   Company: {lead['companyName']}")
        print(f"   Score: {lead_score}/100")
        print(f"   Priority: {priority}")
        print(f"   Services: {', '.join(services)}")
        print(f"   Potential Value: £{potential_value:,}/year")
        
        return lead
    
    def create_lead_from_booking(
        self,
        booking_data: Dict
    ) -> Dict:
        """
        Create CRM lead from booking
        
        Args:
            booking_data: Booking information
            
        Returns:
            Created lead details
        """
        
        lead = {
            "leadId": f"LEAD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "source": LeadSource.BOOKING_FORM,
            "status": LeadStatus.CONTACTED,  # Already contacted via booking
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat(),
            
            # Contact info
            "firstName": booking_data.get('firstName'),
            "lastName": booking_data.get('lastName'),
            "email": booking_data.get('email'),
            "phone": booking_data.get('phone'),
            "companyName": booking_data.get('company'),
            
            # Booking details
            "serviceCategory": booking_data.get('serviceCategory'),
            "packageInterest": booking_data.get('packageInterest'),
            "consultationDate": booking_data.get('preferredDate'),
            "consultationTime": booking_data.get('preferredTime'),
            "consultationType": booking_data.get('consultationType'),
            
            # Lead scoring
            "leadScore": 75,  # High score for active booking
            "priority": "high",
            
            # Tracking
            "touchpoints": 1,
            "lastContactDate": datetime.now().isoformat(),
            "nextFollowUpDate": booking_data.get('preferredDate'),
            
            # Additional context
            "currentAccountant": booking_data.get('currentAccountant', False),
            "annualTurnover": booking_data.get('annualTurnover'),
            "employees": booking_data.get('employees'),
            "message": booking_data.get('message')
        }
        
        self.leads.append(lead)
        
        # Log activity
        self._log_activity(
            lead_id=lead['leadId'],
            activity_type="booking_received",
            description=f"Consultation booked for {booking_data.get('serviceCategory')}",
            metadata={
                "date": booking_data.get('preferredDate'),
                "time": booking_data.get('preferredTime'),
                "type": booking_data.get('consultationType')
            }
        )
        
        print(f"📊 CRM Lead created from booking: {lead['leadId']}")
        print(f"   Contact: {lead['firstName']} {lead['lastName']}")
        print(f"   Service: {lead['serviceCategory']}")
        print(f"   Consultation: {lead['consultationDate']} at {lead['consultationTime']}")
        
        return lead
    
    def update_lead_status(
        self,
        lead_id: str,
        new_status: LeadStatus,
        notes: Optional[str] = None
    ) -> Dict:
        """Update lead status"""
        
        lead = self._find_lead(lead_id)
        if not lead:
            return {"error": "Lead not found"}
        
        old_status = lead['status']
        lead['status'] = new_status
        lead['updatedAt'] = datetime.now().isoformat()
        
        # Log activity
        self._log_activity(
            lead_id=lead_id,
            activity_type="status_changed",
            description=f"Status changed from {old_status} to {new_status}",
            metadata={"old_status": old_status, "new_status": new_status, "notes": notes}
        )
        
        return lead
    
    def create_opportunity(
        self,
        lead_id: str,
        package: str,
        value: float,
        probability: int
    ) -> Dict:
        """
        Create sales opportunity from lead
        
        Args:
            lead_id: Lead ID
            package: Package name (Starter/Professional/Enterprise)
            value: Annual contract value
            probability: Win probability (0-100)
            
        Returns:
            Created opportunity
        """
        
        lead = self._find_lead(lead_id)
        if not lead:
            return {"error": "Lead not found"}
        
        opportunity = {
            "opportunityId": f"OPP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "leadId": lead_id,
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat(),
            
            # Opportunity details
            "package": package,
            "annualValue": value,
            "probability": probability,
            "expectedValue": value * (probability / 100),
            
            # Timeline
            "stage": "proposal",
            "expectedCloseDate": self._calculate_close_date(),
            
            # Company info from lead
            "companyName": lead.get('companyName'),
            "contactEmail": lead.get('email'),
            
            # Status
            "status": "open"
        }
        
        self.opportunities.append(opportunity)
        
        # Update lead
        lead['opportunityId'] = opportunity['opportunityId']
        lead['status'] = 'proposal_sent'  # Use string instead of enum
        lead['updatedAt'] = datetime.now().isoformat()
        
        # Log activity
        self._log_activity(
            lead_id=lead_id,
            activity_type="opportunity_created",
            description=f"Opportunity created: {package} package (£{value:,}/year)",
            metadata={
                "package": package,
                "value": value,
                "probability": probability
            }
        )
        
        print(f"💰 Opportunity created: {opportunity['opportunityId']}")
        print(f"   Package: {package}")
        print(f"   Value: £{value:,}/year")
        print(f"   Probability: {probability}%")
        print(f"   Expected: £{opportunity['expectedValue']:,.0f}/year")
        
        return opportunity
    
    def get_lead_pipeline(self) -> Dict:
        """Get lead pipeline summary"""
        
        pipeline = {
            "total_leads": len(self.leads),
            "by_status": {},
            "by_priority": {},
            "total_potential_value": 0,
            "top_leads": []
        }
        
        # Count by status
        for lead in self.leads:
            status = lead.get('status', 'unknown')
            pipeline['by_status'][status] = pipeline['by_status'].get(status, 0) + 1
            
            priority = lead.get('priority', 'unknown')
            pipeline['by_priority'][priority] = pipeline['by_priority'].get(priority, 0) + 1
            
            pipeline['total_potential_value'] += lead.get('potentialValue', 0)
        
        # Get top leads
        sorted_leads = sorted(
            self.leads,
            key=lambda x: x.get('leadScore', 0),
            reverse=True
        )
        pipeline['top_leads'] = sorted_leads[:10]
        
        return pipeline
    
    def get_opportunities_pipeline(self) -> Dict:
        """Get opportunities pipeline summary"""
        
        pipeline = {
            "total_opportunities": len(self.opportunities),
            "total_value": sum(opp.get('annualValue', 0) for opp in self.opportunities),
            "total_expected_value": sum(opp.get('expectedValue', 0) for opp in self.opportunities),
            "by_package": {},
            "by_stage": {}
        }
        
        for opp in self.opportunities:
            package = opp.get('package', 'unknown')
            pipeline['by_package'][package] = pipeline['by_package'].get(package, 0) + 1
            
            stage = opp.get('stage', 'unknown')
            pipeline['by_stage'][stage] = pipeline['by_stage'].get(stage, 0) + 1
        
        return pipeline
    
    def _calculate_lead_score(
        self,
        company_data: Dict,
        recommendations: List[Dict]
    ) -> int:
        """Calculate lead score (0-100)"""
        
        score = 0
        
        # Company size (0-30 points)
        turnover = company_data.get('annualTurnover', 0)
        if turnover > 1000000:
            score += 30
        elif turnover > 500000:
            score += 25
        elif turnover > 250000:
            score += 20
        elif turnover > 100000:
            score += 15
        else:
            score += 10
        
        # Number of employees (0-20 points)
        employees = company_data.get('employees', 0)
        if employees > 50:
            score += 20
        elif employees > 20:
            score += 15
        elif employees > 10:
            score += 12
        elif employees > 5:
            score += 8
        else:
            score += 5
        
        # Compliance issues (0-20 points)
        compliance_score = company_data.get('complianceScore', 100)
        if compliance_score < 60:
            score += 20  # High need
        elif compliance_score < 75:
            score += 15
        elif compliance_score < 85:
            score += 10
        else:
            score += 5
        
        # Number of recommendations (0-15 points)
        num_recs = len(recommendations)
        score += min(num_recs * 3, 15)
        
        # High priority recommendations (0-15 points)
        high_priority = sum(1 for rec in recommendations if rec.get('priority') == 'high')
        score += min(high_priority * 5, 15)
        
        return min(score, 100)
    
    def _determine_priority(
        self,
        lead_score: int,
        recommendations: List[Dict]
    ) -> str:
        """Determine lead priority"""
        
        high_priority_recs = sum(1 for rec in recommendations if rec.get('priority') == 'high')
        medium_priority_recs = sum(1 for rec in recommendations if rec.get('priority') == 'medium')
        
        if lead_score >= 75 or high_priority_recs >= 2:
            return "high"
        elif lead_score >= 45 or medium_priority_recs >= 1:
            return "medium"
        else:
            return "low"
    
    def _calculate_potential_value(
        self,
        company_data: Dict,
        recommendations: List[Dict]
    ) -> float:
        """Calculate potential annual contract value"""
        
        # Base package value
        turnover = company_data.get('annualTurnover', 0)
        employees = company_data.get('employees', 0)
        
        if turnover > 1000000 or employees > 50:
            base_value = 9588  # Enterprise package
        elif turnover > 250000 or employees > 10:
            base_value = 3588  # Professional package
        else:
            base_value = 1188  # Starter package
        
        # Add value for additional services
        num_services = len(recommendations)
        additional_value = (num_services - 1) * 500  # £500 per additional service
        
        return base_value + max(additional_value, 0)
    
    def _get_overall_confidence(self, recommendations: List[Dict]) -> int:
        """Get overall AI confidence from recommendations"""
        
        if not recommendations:
            return 0
        
        confidences = [rec.get('confidence', 0) for rec in recommendations]
        return int(sum(confidences) / len(confidences))
    
    def _calculate_follow_up_date(self, priority: str) -> str:
        """Calculate next follow-up date based on priority"""
        
        from datetime import timedelta
        
        if priority == "high":
            days = 1
        elif priority == "medium":
            days = 3
        else:
            days = 7
        
        follow_up = datetime.now() + timedelta(days=days)
        return follow_up.isoformat()
    
    def _calculate_close_date(self) -> str:
        """Calculate expected close date"""
        
        from datetime import timedelta
        
        close_date = datetime.now() + timedelta(days=30)
        return close_date.isoformat()
    
    def _find_lead(self, lead_id: str) -> Optional[Dict]:
        """Find lead by ID"""
        
        for lead in self.leads:
            if lead.get('leadId') == lead_id:
                return lead
        return None
    
    def _log_activity(
        self,
        lead_id: str,
        activity_type: str,
        description: str,
        metadata: Optional[Dict] = None
    ):
        """Log CRM activity"""
        
        activity = {
            "activityId": f"ACT-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            "leadId": lead_id,
            "type": activity_type,
            "description": description,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.activities.append(activity)
        
        # Update lead touchpoints
        lead = self._find_lead(lead_id)
        if lead:
            lead['touchpoints'] = lead.get('touchpoints', 0) + 1
            lead['lastContactDate'] = datetime.now().isoformat()
    
    def get_lead_activities(self, lead_id: str) -> List[Dict]:
        """Get all activities for a lead"""
        
        return [
            activity for activity in self.activities
            if activity.get('leadId') == lead_id
        ]
    
    def get_pipeline_analytics(self) -> Dict:
        """Get pipeline analytics and metrics"""
        
        total_leads = len(self.leads)
        total_opportunities = len(self.opportunities)
        
        # Calculate conversion rate
        conversion_rate = (total_opportunities / total_leads * 100) if total_leads > 0 else 0
        
        # Calculate win rate
        won_opps = [o for o in self.opportunities if o.get('status') == 'won']
        closed_opps = [o for o in self.opportunities if o.get('status') in ['won', 'lost']]
        win_rate = (len(won_opps) / len(closed_opps) * 100) if len(closed_opps) > 0 else 0
        
        # Calculate pipeline value
        pipeline_value = sum(o.get('annualValue', 0) for o in self.opportunities if o.get('status') == 'open')
        expected_value = sum(o.get('expectedValue', 0) for o in self.opportunities if o.get('status') == 'open')
        
        # Calculate average deal size
        avg_deal_size = (sum(o.get('annualValue', 0) for o in won_opps) / len(won_opps)) if won_opps else 0
        
        # Calculate average lead score
        avg_lead_score = (sum(l.get('leadScore', 0) for l in self.leads) / total_leads) if total_leads > 0 else 0
        
        return {
            "totalLeads": total_leads,
            "totalOpportunities": total_opportunities,
            "conversionRate": round(conversion_rate, 2),
            "winRate": round(win_rate, 2),
            "pipelineValue": round(pipeline_value, 2),
            "expectedValue": round(expected_value, 2),
            "avgDealSize": round(avg_deal_size, 2),
            "avgLeadScore": round(avg_lead_score, 2),
            "wonOpportunities": len(won_opps),
            "lostOpportunities": len([o for o in self.opportunities if o.get('status') == 'lost']),
            "openOpportunities": len([o for o in self.opportunities if o.get('status') == 'open'])
        }


# Singleton instance
crm_integration = CRMIntegration()

