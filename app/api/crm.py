"""
CRM API
Endpoints for CRM lead and opportunity management
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict
from datetime import datetime
import sys
sys.path.append('/home/ubuntu/fineguard-backend')

from app.services.crm_integration import crm_integration, LeadStatus
from app.services.companies_house import companies_house_api

router = APIRouter()


class CreateLeadFromAIRequest(BaseModel):
    """Request to create lead from AI recommendation"""
    companyNumber: str
    userEmail: EmailStr
    recommendations: List[Dict]


class UpdateLeadStatusRequest(BaseModel):
    """Request to update lead status"""
    status: LeadStatus
    notes: Optional[str] = None


class CreateOpportunityRequest(BaseModel):
    """Request to create opportunity"""
    package: str  # Starter, Professional, Enterprise
    annualValue: float
    probability: int  # 0-100


@router.post("/crm/leads/from-ai")
async def create_lead_from_ai(request: CreateLeadFromAIRequest):
    """
    Create CRM lead from AI recommendation
    
    Args:
        request: Lead creation request with company data and recommendations
        
    Returns:
        Created lead details
    """
    
    # Get company data from Companies House
    company_data = companies_house_api.enrich_company_data(request.companyNumber)
    
    if not company_data:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Create CRM lead
    lead = crm_integration.create_lead_from_ai_recommendation(
        company_data=company_data,
        recommendations=request.recommendations,
        user_email=request.userEmail
    )
    
    return {
        "status": "success",
        "message": "Lead created successfully",
        "lead": lead
    }


@router.get("/crm/leads/{lead_id}")
async def get_lead(lead_id: str):
    """
    Get lead details
    
    Args:
        lead_id: Lead ID
        
    Returns:
        Lead details
    """
    
    lead = crm_integration._find_lead(lead_id)
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Get activities
    activities = crm_integration.get_lead_activities(lead_id)
    
    return {
        "lead": lead,
        "activities": activities
    }


@router.put("/crm/leads/{lead_id}/status")
async def update_lead_status(lead_id: str, request: UpdateLeadStatusRequest):
    """
    Update lead status
    
    Args:
        lead_id: Lead ID
        request: Status update request
        
    Returns:
        Updated lead
    """
    
    lead = crm_integration.update_lead_status(
        lead_id=lead_id,
        new_status=request.status,
        notes=request.notes
    )
    
    if "error" in lead:
        raise HTTPException(status_code=404, detail=lead["error"])
    
    return {
        "status": "success",
        "message": "Lead status updated",
        "lead": lead
    }


@router.post("/crm/leads/{lead_id}/opportunity")
async def create_opportunity(lead_id: str, request: CreateOpportunityRequest):
    """
    Create sales opportunity from lead
    
    Args:
        lead_id: Lead ID
        request: Opportunity creation request
        
    Returns:
        Created opportunity
    """
    
    opportunity = crm_integration.create_opportunity(
        lead_id=lead_id,
        package=request.package,
        value=request.annualValue,
        probability=request.probability
    )
    
    if "error" in opportunity:
        raise HTTPException(status_code=404, detail=opportunity["error"])
    
    return {
        "status": "success",
        "message": "Opportunity created",
        "opportunity": opportunity
    }


@router.get("/crm/pipeline")
async def get_pipeline():
    """
    Get CRM pipeline summary
    
    Returns:
        Pipeline metrics and top leads
    """
    
    lead_pipeline = crm_integration.get_lead_pipeline()
    opp_pipeline = crm_integration.get_opportunities_pipeline()
    
    return {
        "leads": lead_pipeline,
        "opportunities": opp_pipeline,
        "summary": {
            "total_leads": lead_pipeline['total_leads'],
            "total_opportunities": opp_pipeline['total_opportunities'],
            "total_potential_value": lead_pipeline['total_potential_value'],
            "total_pipeline_value": opp_pipeline['total_value'],
            "expected_revenue": opp_pipeline['total_expected_value']
        }
    }


@router.get("/crm/leads")
async def get_all_leads(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    limit: int = 50
):
    """
    Get all leads with optional filters
    
    Args:
        status: Filter by status
        priority: Filter by priority
        limit: Maximum number of results
        
    Returns:
        List of leads
    """
    
    leads = crm_integration.leads
    
    # Apply filters
    if status:
        leads = [l for l in leads if l.get('status') == status]
    
    if priority:
        leads = [l for l in leads if l.get('priority') == priority]
    
    # Sort by lead score
    leads = sorted(leads, key=lambda x: x.get('leadScore', 0), reverse=True)
    
    # Limit results
    leads = leads[:limit]
    
    return {
        "total": len(leads),
        "leads": leads
    }


@router.get("/crm/opportunities")
async def get_all_opportunities(
    status: Optional[str] = None,
    package: Optional[str] = None
):
    """
    Get all opportunities with optional filters
    
    Args:
        status: Filter by status
        package: Filter by package
        
    Returns:
        List of opportunities
    """
    
    opportunities = crm_integration.opportunities
    
    # Apply filters
    if status:
        opportunities = [o for o in opportunities if o.get('status') == status]
    
    if package:
        opportunities = [o for o in opportunities if o.get('package') == package]
    
    # Sort by expected value
    opportunities = sorted(
        opportunities,
        key=lambda x: x.get('expectedValue', 0),
        reverse=True
    )
    
    return {
        "total": len(opportunities),
        "opportunities": opportunities
    }


@router.get("/crm/analytics")
async def get_crm_analytics():
    """
    Get CRM analytics and metrics
    
    Returns:
        Analytics data
    """
    
    leads = crm_integration.leads
    opportunities = crm_integration.opportunities
    
    # Calculate metrics
    total_leads = len(leads)
    total_opportunities = len(opportunities)
    
    # Conversion rate
    conversion_rate = (total_opportunities / total_leads * 100) if total_leads > 0 else 0
    
    # Average lead score
    avg_lead_score = sum(l.get('leadScore', 0) for l in leads) / total_leads if total_leads > 0 else 0
    
    # Win rate (for demo, assume 30%)
    win_rate = 30.0
    
    # Average deal size
    avg_deal_size = sum(o.get('annualValue', 0) for o in opportunities) / total_opportunities if total_opportunities > 0 else 0
    
    # Pipeline velocity (days to close)
    pipeline_velocity = 30  # Demo value
    
    return {
        "metrics": {
            "total_leads": total_leads,
            "total_opportunities": total_opportunities,
            "conversion_rate": round(conversion_rate, 2),
            "average_lead_score": round(avg_lead_score, 1),
            "win_rate": win_rate,
            "average_deal_size": round(avg_deal_size, 2),
            "pipeline_velocity_days": pipeline_velocity
        },
        "trends": {
            "leads_this_month": total_leads,  # Demo
            "opportunities_this_month": total_opportunities,
            "revenue_this_month": sum(o.get('annualValue', 0) for o in opportunities if o.get('status') == 'won')
        }
    }

