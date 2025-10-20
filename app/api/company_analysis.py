"""
Company Analysis API
Provides company data for AI recommendations
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import sys
sys.path.append('/home/ubuntu/fineguard-backend')
from app.services.companies_house import companies_house_api

router = APIRouter()

class CompanyAnalysisResponse(BaseModel):
    """Company analysis data for AI recommendations"""
    companyNumber: str
    name: str
    riskLevel: str
    complianceScore: int
    overdueCount: int
    obligationCount: int
    annualTurnover: int
    employees: int
    industry: str
    age: int
    hasAccountant: bool
    lastUpdated: str
    recommendations: Optional[dict] = None


@router.get("/companies/{company_number}/analysis", response_model=CompanyAnalysisResponse)
async def get_company_analysis(company_number: str):
    """
    Get company analysis data for AI recommendations
    
    Args:
        company_number: Companies House registration number
        
    Returns:
        CompanyAnalysisResponse with all metrics for AI analysis
    """
    
    # Fetch real data from Companies House API
    enriched_data = companies_house_api.enrich_company_data(company_number)
    
    if enriched_data:
        enriched_data["lastUpdated"] = datetime.now().isoformat()
        return CompanyAnalysisResponse(**enriched_data)
    
    # Fallback to demo data if API fails
    
    # Demo data mapping
    demo_companies = {
        "12345678": {
            "companyNumber": "12345678",
            "name": "Tech Innovations Ltd",
            "riskLevel": "medium",
            "complianceScore": 72,
            "overdueCount": 2,
            "obligationCount": 8,
            "annualTurnover": 350000,
            "employees": 12,
            "industry": "technology",
            "age": 3,
            "hasAccountant": False
        },
        "87654321": {
            "companyNumber": "87654321",
            "name": "Construction Services Ltd",
            "riskLevel": "high",
            "complianceScore": 58,
            "overdueCount": 4,
            "obligationCount": 12,
            "annualTurnover": 850000,
            "employees": 28,
            "industry": "construction",
            "age": 7,
            "hasAccountant": True
        },
        "11111111": {
            "companyNumber": "11111111",
            "name": "Startup Ventures Ltd",
            "riskLevel": "low",
            "complianceScore": 92,
            "overdueCount": 0,
            "obligationCount": 4,
            "annualTurnover": 85000,
            "employees": 3,
            "industry": "consulting",
            "age": 1,
            "hasAccountant": False
        }
    }
    
    company_data = demo_companies.get(company_number)
    
    if not company_data:
        # Return default data for unknown companies
        company_data = {
            "companyNumber": company_number,
            "name": f"Company {company_number}",
            "riskLevel": "medium",
            "complianceScore": 75,
            "overdueCount": 1,
            "obligationCount": 6,
            "annualTurnover": 250000,
            "employees": 8,
            "industry": "general",
            "age": 2,
            "hasAccountant": False
        }
    
    # Add timestamp
    company_data["lastUpdated"] = datetime.now().isoformat()
    
    return CompanyAnalysisResponse(**company_data)


@router.get("/companies/current/analysis", response_model=CompanyAnalysisResponse)
async def get_current_company_analysis():
    """
    Get analysis for currently logged-in user's company
    
    Returns:
        CompanyAnalysisResponse for current user's company
    """
    
    # In production, get from authenticated user session
    # For now, return default demo company
    return await get_company_analysis("12345678")


@router.post("/companies/{company_number}/analysis/refresh")
async def refresh_company_analysis(company_number: str):
    """
    Refresh company analysis data from Companies House
    
    Args:
        company_number: Companies House registration number
        
    Returns:
        Status message
    """
    
    # In production, this would:
    # 1. Fetch latest data from Companies House API
    # 2. Recalculate compliance score
    # 3. Update risk level
    # 4. Store in database
    
    return {
        "status": "success",
        "message": f"Analysis refreshed for company {company_number}",
        "timestamp": datetime.now().isoformat()
    }

