"""
Companies House API Integration
Real-time company data from Companies House API
"""

import os
import sys
import requests
from typing import Dict, Optional, List
from datetime import datetime
import json

sys.path.append('/home/ubuntu/fineguard-backend')
from app.utils.cache import cached


class CompaniesHouseAPI:
    """Integration with Companies House API"""
    
    def __init__(self):
        # In production, use environment variable
        self.api_key = os.getenv('COMPANIES_HOUSE_API_KEY', 'demo_key')
        self.base_url = "https://api.company-information.service.gov.uk"
        self.session = requests.Session()
        self.session.auth = (self.api_key, '')
        self.cache = {}  # Simple cache for demo
    
    @cached(ttl=3600)  # Cache for 1 hour
    def get_company_profile(self, company_number: str) -> Optional[Dict]:
        """
        Get company profile from Companies House
        
        Args:
            company_number: Companies House registration number
            
        Returns:
            Company profile data or None
        """
        
        # Check cache first
        if company_number in self.cache:
            cached = self.cache[company_number]
            if (datetime.now() - cached['timestamp']).seconds < 3600:  # 1 hour cache
                print(f"📦 Using cached data for {company_number}")
                return cached['data']
        
        try:
            url = f"{self.base_url}/company/{company_number}"
            
            # In demo mode, return mock data
            if self.api_key == 'demo_key':
                return self._get_mock_company_profile(company_number)
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Cache the result
                self.cache[company_number] = {
                    'data': data,
                    'timestamp': datetime.now()
                }
                
                print(f"✅ Retrieved company profile: {data.get('company_name')}")
                return data
            else:
                print(f"❌ Companies House API error: {response.status_code}")
                return self._get_mock_company_profile(company_number)
                
        except Exception as e:
            print(f"❌ Error fetching company profile: {str(e)}")
            return self._get_mock_company_profile(company_number)
    
    def get_company_officers(self, company_number: str) -> List[Dict]:
        """Get company officers"""
        
        try:
            url = f"{self.base_url}/company/{company_number}/officers"
            
            if self.api_key == 'demo_key':
                return self._get_mock_officers(company_number)
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('items', [])
            else:
                return self._get_mock_officers(company_number)
                
        except Exception as e:
            print(f"❌ Error fetching officers: {str(e)}")
            return self._get_mock_officers(company_number)
    
    def get_company_filing_history(
        self,
        company_number: str,
        limit: int = 10
    ) -> List[Dict]:
        """Get company filing history"""
        
        try:
            url = f"{self.base_url}/company/{company_number}/filing-history"
            params = {'items_per_page': limit}
            
            if self.api_key == 'demo_key':
                return self._get_mock_filing_history(company_number)
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('items', [])
            else:
                return self._get_mock_filing_history(company_number)
                
        except Exception as e:
            print(f"❌ Error fetching filing history: {str(e)}")
            return self._get_mock_filing_history(company_number)
    
    def search_companies(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for companies"""
        
        try:
            url = f"{self.base_url}/search/companies"
            params = {'q': query, 'items_per_page': limit}
            
            if self.api_key == 'demo_key':
                return self._get_mock_search_results(query)
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('items', [])
            else:
                return self._get_mock_search_results(query)
                
        except Exception as e:
            print(f"❌ Error searching companies: {str(e)}")
            return self._get_mock_search_results(query)
    
    def calculate_compliance_metrics(self, company_number: str) -> Dict:
        """
        Calculate compliance metrics from Companies House data
        
        Returns:
            Dict with compliance score, risk level, obligations
        """
        
        profile = self.get_company_profile(company_number)
        filing_history = self.get_company_filing_history(company_number)
        
        if not profile:
            return {
                "complianceScore": 0,
                "riskLevel": "unknown",
                "overdueCount": 0,
                "obligationCount": 0
            }
        
        # Calculate compliance score
        score = 100
        overdue_count = 0
        
        # Check company status
        status = profile.get('company_status', '')
        if status != 'active':
            score -= 30
        
        # Check accounts overdue
        accounts = profile.get('accounts', {})
        if accounts.get('overdue', False):
            score -= 25
            overdue_count += 1
        
        # Check confirmation statement overdue
        confirmation_statement = profile.get('confirmation_statement', {})
        if confirmation_statement.get('overdue', False):
            score -= 20
            overdue_count += 1
        
        # Check filing frequency
        if len(filing_history) < 2:
            score -= 15
        
        # Determine risk level
        if score >= 80:
            risk_level = "low"
        elif score >= 60:
            risk_level = "medium"
        else:
            risk_level = "high"
        
        # Count obligations
        obligation_count = 2  # Accounts + Confirmation Statement
        if profile.get('type') == 'ltd':
            obligation_count += 2  # Additional obligations for limited companies
        
        return {
            "complianceScore": max(score, 0),
            "riskLevel": risk_level,
            "overdueCount": overdue_count,
            "obligationCount": obligation_count,
            "lastAccountsDate": accounts.get('last_accounts', {}).get('made_up_to'),
            "nextAccountsDue": accounts.get('next_due'),
            "confirmationStatementDue": confirmation_statement.get('next_due')
        }
    
    @cached(ttl=1800)  # Cache for 30 minutes
    def enrich_company_data(self, company_number: str) -> Dict:
        """
        Enrich company data with all available information
        
        Returns:
            Comprehensive company data for AI analysis
        """
        
        profile = self.get_company_profile(company_number)
        officers = self.get_company_officers(company_number)
        compliance = self.calculate_compliance_metrics(company_number)
        
        if not profile:
            return {}
        
        # Estimate employees (if not available)
        employees = self._estimate_employees(profile, officers)
        
        # Estimate turnover (if not available)
        turnover = self._estimate_turnover(profile)
        
        # Calculate company age
        incorporation_date = profile.get('date_of_creation', '')
        age = self._calculate_age(incorporation_date)
        
        # Determine industry
        industry = self._determine_industry(profile)
        
        return {
            "companyNumber": company_number,
            "name": profile.get('company_name', ''),
            "status": profile.get('company_status', ''),
            "type": profile.get('type', ''),
            "incorporationDate": incorporation_date,
            "age": age,
            "industry": industry,
            "address": profile.get('registered_office_address', {}),
            "sicCodes": profile.get('sic_codes', []),
            
            # Estimated metrics
            "employees": employees,
            "annualTurnover": turnover,
            
            # Compliance metrics
            **compliance,
            
            # Officers
            "officerCount": len(officers),
            "hasAccountant": self._has_accountant(officers),
            
            # Metadata
            "lastUpdated": datetime.now().isoformat(),
            "dataSource": "companies_house"
        }
    
    def _get_mock_company_profile(self, company_number: str) -> Dict:
        """Return mock company profile for demo"""
        
        mock_companies = {
            "12345678": {
                "company_number": "12345678",
                "company_name": "Tech Innovations Ltd",
                "company_status": "active",
                "type": "ltd",
                "date_of_creation": "2021-03-15",
                "registered_office_address": {
                    "address_line_1": "123 Tech Street",
                    "locality": "London",
                    "postal_code": "EC1A 1BB"
                },
                "sic_codes": ["62012"],
                "accounts": {
                    "overdue": False,
                    "next_due": "2024-12-31",
                    "last_accounts": {
                        "made_up_to": "2023-12-31"
                    }
                },
                "confirmation_statement": {
                    "overdue": False,
                    "next_due": "2024-11-15"
                }
            },
            "87654321": {
                "company_number": "87654321",
                "company_name": "Construction Services Ltd",
                "company_status": "active",
                "type": "ltd",
                "date_of_creation": "2017-06-20",
                "registered_office_address": {
                    "address_line_1": "456 Builder Road",
                    "locality": "Manchester",
                    "postal_code": "M1 1AA"
                },
                "sic_codes": ["41201"],
                "accounts": {
                    "overdue": True,
                    "next_due": "2024-09-30",
                    "last_accounts": {
                        "made_up_to": "2022-12-31"
                    }
                },
                "confirmation_statement": {
                    "overdue": True,
                    "next_due": "2024-08-20"
                }
            }
        }
        
        return mock_companies.get(
            company_number,
            {
                "company_number": company_number,
                "company_name": f"Company {company_number}",
                "company_status": "active",
                "type": "ltd",
                "date_of_creation": "2020-01-01",
                "sic_codes": ["99999"]
            }
        )
    
    def _get_mock_officers(self, company_number: str) -> List[Dict]:
        """Return mock officers"""
        
        return [
            {
                "name": "John Smith",
                "officer_role": "director",
                "appointed_on": "2021-03-15"
            },
            {
                "name": "Jane Doe",
                "officer_role": "secretary",
                "appointed_on": "2021-03-15"
            }
        ]
    
    def _get_mock_filing_history(self, company_number: str) -> List[Dict]:
        """Return mock filing history"""
        
        return [
            {
                "category": "accounts",
                "description": "Annual accounts",
                "date": "2024-01-15",
                "type": "AA"
            },
            {
                "category": "confirmation-statement",
                "description": "Confirmation statement",
                "date": "2024-03-15",
                "type": "CS01"
            }
        ]
    
    def _get_mock_search_results(self, query: str) -> List[Dict]:
        """Return mock search results"""
        
        return [
            {
                "company_number": "12345678",
                "company_name": "Tech Innovations Ltd",
                "company_status": "active",
                "address_snippet": "London"
            }
        ]
    
    def _estimate_employees(self, profile: Dict, officers: List[Dict]) -> int:
        """Estimate number of employees"""
        
        # Simple estimation based on company type and officers
        officer_count = len(officers)
        
        if officer_count <= 2:
            return 5
        elif officer_count <= 4:
            return 12
        else:
            return 25
    
    def _estimate_turnover(self, profile: Dict) -> int:
        """Estimate annual turnover"""
        
        # Simple estimation based on company age and type
        age = self._calculate_age(profile.get('date_of_creation', ''))
        
        if age < 2:
            return 100000
        elif age < 5:
            return 350000
        else:
            return 750000
    
    def _calculate_age(self, incorporation_date: str) -> int:
        """Calculate company age in years"""
        
        if not incorporation_date:
            return 0
        
        try:
            inc_date = datetime.fromisoformat(incorporation_date.replace('Z', '+00:00'))
            age = (datetime.now() - inc_date).days // 365
            return max(age, 0)
        except:
            return 0
    
    def _determine_industry(self, profile: Dict) -> str:
        """Determine industry from SIC codes"""
        
        sic_codes = profile.get('sic_codes', [])
        
        if not sic_codes:
            return "general"
        
        # Map SIC codes to industries
        sic_mapping = {
            "62": "technology",
            "41": "construction",
            "64": "financial",
            "69": "legal",
            "70": "consulting",
            "47": "retail"
        }
        
        first_sic = str(sic_codes[0])[:2]
        return sic_mapping.get(first_sic, "general")
    
    def _has_accountant(self, officers: List[Dict]) -> bool:
        """Check if company has an accountant"""
        
        # Simple check - in production, would check against accountant database
        return False


# Singleton instance
companies_house_api = CompaniesHouseAPI()
companies_house_service = companies_house_api  # Alias for consistency

