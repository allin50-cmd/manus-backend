"""
Accountant Services
Combines AI-powered automation with human accountant expertise
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from enum import Enum
import json


class AccountantType(str, Enum):
    """Types of accountants"""
    AI_ASSISTANT = "ai_assistant"
    JUNIOR_ACCOUNTANT = "junior_accountant"
    SENIOR_ACCOUNTANT = "senior_accountant"
    CHARTERED_ACCOUNTANT = "chartered_accountant"
    TAX_SPECIALIST = "tax_specialist"
    AUDIT_SPECIALIST = "audit_specialist"


class ServiceCategory(str, Enum):
    """Service categories"""
    BOOKKEEPING = "bookkeeping"
    TAX_RETURNS = "tax_returns"
    PAYROLL = "payroll"
    VAT = "vat"
    AUDIT = "audit"
    FINANCIAL_PLANNING = "financial_planning"
    COMPANY_SECRETARIAL = "company_secretarial"
    CONSULTING = "consulting"


class TaskPriority(str, Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class AccountantService:
    """Comprehensive accountant service combining AI and human expertise"""
    
    def __init__(self):
        self.accountants = self._initialize_accountants()
        self.tasks = []
        self.assignments = []
        self.ai_automations = []
    
    def _initialize_accountants(self) -> List[Dict]:
        """Initialize team of accountants"""
        return [
            # AI Assistant
            {
                "id": "AI-001",
                "name": "FineGuard AI Assistant",
                "type": AccountantType.AI_ASSISTANT,
                "specialties": ["bookkeeping", "data_entry", "categorization", "reconciliation"],
                "availability": "24/7",
                "capacity": 1000,  # tasks per day
                "cost_per_hour": 0,  # Free
                "accuracy": 98.5,
                "speed_multiplier": 10.0
            },
            
            # Junior Accountants
            {
                "id": "JA-001",
                "name": "Sarah Mitchell",
                "type": AccountantType.JUNIOR_ACCOUNTANT,
                "specialties": ["bookkeeping", "payroll", "data_entry"],
                "availability": "Mon-Fri 9am-5pm",
                "capacity": 20,
                "cost_per_hour": 35,
                "accuracy": 95.0,
                "speed_multiplier": 1.0,
                "email": "sarah.mitchell@devonshiregreen.uk",
                "phone": "01959 565 772"
            },
            {
                "id": "JA-002",
                "name": "James Thompson",
                "type": AccountantType.JUNIOR_ACCOUNTANT,
                "specialties": ["vat", "bookkeeping", "reconciliation"],
                "availability": "Mon-Fri 9am-5pm",
                "capacity": 20,
                "cost_per_hour": 35,
                "accuracy": 94.5,
                "speed_multiplier": 1.0,
                "email": "james.thompson@devonshiregreen.uk",
                "phone": "01959 565 772"
            },
            
            # Senior Accountants
            {
                "id": "SA-001",
                "name": "Michael Roberts",
                "type": AccountantType.SENIOR_ACCOUNTANT,
                "specialties": ["tax_returns", "financial_planning", "consulting"],
                "availability": "Mon-Fri 9am-6pm",
                "capacity": 15,
                "cost_per_hour": 75,
                "accuracy": 98.0,
                "speed_multiplier": 1.5,
                "qualifications": ["ACCA", "15 years experience"],
                "email": "michael.roberts@devonshiregreen.uk",
                "phone": "01959 565 772"
            },
            {
                "id": "SA-002",
                "name": "Emma Williams",
                "type": AccountantType.SENIOR_ACCOUNTANT,
                "specialties": ["payroll", "company_secretarial", "compliance"],
                "availability": "Mon-Fri 9am-6pm",
                "capacity": 15,
                "cost_per_hour": 75,
                "accuracy": 97.5,
                "speed_multiplier": 1.5,
                "qualifications": ["CIMA", "12 years experience"],
                "email": "emma.williams@devonshiregreen.uk",
                "phone": "01959 565 772"
            },
            
            # Chartered Accountants
            {
                "id": "CA-001",
                "name": "David Patterson",
                "type": AccountantType.CHARTERED_ACCOUNTANT,
                "specialties": ["audit", "financial_planning", "consulting", "tax_planning"],
                "availability": "Mon-Fri 9am-7pm",
                "capacity": 10,
                "cost_per_hour": 150,
                "accuracy": 99.5,
                "speed_multiplier": 2.0,
                "qualifications": ["FCA", "25 years experience", "Partner"],
                "email": "david.patterson@devonshiregreen.uk",
                "phone": "01959 565 772"
            },
            
            # Tax Specialist
            {
                "id": "TS-001",
                "name": "Rachel Green",
                "type": AccountantType.TAX_SPECIALIST,
                "specialties": ["tax_returns", "tax_planning", "inheritance_tax", "capital_gains"],
                "availability": "Mon-Fri 9am-6pm",
                "capacity": 12,
                "cost_per_hour": 120,
                "accuracy": 99.0,
                "speed_multiplier": 1.8,
                "qualifications": ["CTA", "ATT", "18 years experience"],
                "email": "rachel.green@devonshiregreen.uk",
                "phone": "01959 565 772"
            },
            
            # Audit Specialist
            {
                "id": "AS-001",
                "name": "Thomas Brown",
                "type": AccountantType.AUDIT_SPECIALIST,
                "specialties": ["audit", "compliance", "risk_assessment", "internal_controls"],
                "availability": "Mon-Fri 9am-6pm",
                "capacity": 8,
                "cost_per_hour": 130,
                "accuracy": 99.8,
                "speed_multiplier": 1.7,
                "qualifications": ["ACA", "20 years experience"],
                "email": "thomas.brown@devonshiregreen.uk",
                "phone": "01959 565 772"
            }
        ]
    
    def assign_task(
        self,
        task_data: Dict,
        prefer_ai: bool = True
    ) -> Dict:
        """
        Intelligently assign task to best accountant (AI or human)
        
        Args:
            task_data: Task information
            prefer_ai: Whether to prefer AI when possible
            
        Returns:
            Assignment details
        """
        
        category = task_data.get('category')
        priority = task_data.get('priority', TaskPriority.MEDIUM)
        complexity = task_data.get('complexity', 'medium')  # low/medium/high
        
        # Determine if AI can handle this
        ai_suitable = self._is_ai_suitable(category, complexity, priority)
        
        if ai_suitable and prefer_ai:
            # Assign to AI
            accountant = self._get_accountant("AI-001")
        else:
            # Assign to human accountant
            accountant = self._find_best_accountant(category, priority, complexity)
        
        # Create assignment
        assignment = {
            "assignmentId": f"ASSIGN-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "taskId": task_data.get('taskId'),
            "accountantId": accountant['id'],
            "accountantName": accountant['name'],
            "accountantType": accountant['type'],
            "category": category,
            "priority": priority,
            "assignedAt": datetime.now().isoformat(),
            "estimatedCompletion": self._estimate_completion(accountant, task_data),
            "estimatedCost": self._estimate_cost(accountant, task_data),
            "status": "assigned"
        }
        
        self.assignments.append(assignment)
        
        print(f"📋 Task assigned to {accountant['name']} ({accountant['type']})")
        print(f"   Category: {category}")
        print(f"   Priority: {priority}")
        print(f"   Est. Completion: {assignment['estimatedCompletion']}")
        print(f"   Est. Cost: £{assignment['estimatedCost']}")
        
        return assignment
    
    def _is_ai_suitable(
        self,
        category: str,
        complexity: str,
        priority: str
    ) -> bool:
        """Determine if AI can handle this task"""
        
        # AI-suitable categories
        ai_categories = [
            ServiceCategory.BOOKKEEPING,
            ServiceCategory.PAYROLL,
            ServiceCategory.VAT
        ]
        
        # AI can handle low-medium complexity, non-urgent tasks
        if category in ai_categories:
            if complexity in ['low', 'medium'] and priority != TaskPriority.URGENT:
                return True
        
        return False
    
    def _find_best_accountant(
        self,
        category: str,
        priority: str,
        complexity: str
    ) -> Dict:
        """Find best human accountant for task"""
        
        # Filter by specialty
        candidates = [
            acc for acc in self.accountants
            if acc['type'] != AccountantType.AI_ASSISTANT
            and category in acc.get('specialties', [])
        ]
        
        if not candidates:
            # Fallback to senior accountants
            candidates = [
                acc for acc in self.accountants
                if acc['type'] in [AccountantType.SENIOR_ACCOUNTANT, AccountantType.CHARTERED_ACCOUNTANT]
            ]
        
        # Score candidates
        scored = []
        for acc in candidates:
            score = 0
            
            # Specialty match
            if category in acc.get('specialties', []):
                score += 50
            
            # Accuracy
            score += acc.get('accuracy', 0)
            
            # Availability (simplified)
            score += acc.get('capacity', 0) * 0.5
            
            # Complexity match
            if complexity == 'high' and acc['type'] in [AccountantType.CHARTERED_ACCOUNTANT, AccountantType.TAX_SPECIALIST, AccountantType.AUDIT_SPECIALIST]:
                score += 30
            elif complexity == 'medium' and acc['type'] in [AccountantType.SENIOR_ACCOUNTANT, AccountantType.CHARTERED_ACCOUNTANT]:
                score += 20
            
            scored.append((score, acc))
        
        # Return highest scored
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1] if scored else self.accountants[1]  # Fallback to first human
    
    def _get_accountant(self, accountant_id: str) -> Optional[Dict]:
        """Get accountant by ID"""
        for acc in self.accountants:
            if acc['id'] == accountant_id:
                return acc
        return None
    
    def _estimate_completion(self, accountant: Dict, task_data: Dict) -> str:
        """Estimate task completion time"""
        
        base_hours = task_data.get('estimatedHours', 2)
        speed_multiplier = accountant.get('speed_multiplier', 1.0)
        
        actual_hours = base_hours / speed_multiplier
        
        completion_time = datetime.now() + timedelta(hours=actual_hours)
        
        return completion_time.isoformat()
    
    def _estimate_cost(self, accountant: Dict, task_data: Dict) -> float:
        """Estimate task cost"""
        
        base_hours = task_data.get('estimatedHours', 2)
        hourly_rate = accountant.get('cost_per_hour', 0)
        
        return round(base_hours * hourly_rate, 2)
    
    def get_available_services(self) -> List[Dict]:
        """Get all available accounting services"""
        
        return [
            {
                "category": "Bookkeeping",
                "services": [
                    "Transaction recording",
                    "Bank reconciliation",
                    "Accounts payable/receivable",
                    "Financial statements",
                    "Month-end close"
                ],
                "aiSupported": True,
                "humanReview": True,
                "startingPrice": 150,
                "frequency": "monthly"
            },
            {
                "category": "Tax Returns",
                "services": [
                    "Personal tax returns",
                    "Corporate tax returns",
                    "Tax planning",
                    "HMRC correspondence",
                    "Tax investigations"
                ],
                "aiSupported": False,
                "humanReview": True,
                "startingPrice": 250,
                "frequency": "annual"
            },
            {
                "category": "Payroll",
                "services": [
                    "Payroll processing",
                    "RTI submissions",
                    "PAYE/NI calculations",
                    "Pension auto-enrolment",
                    "P60/P45 generation"
                ],
                "aiSupported": True,
                "humanReview": True,
                "startingPrice": 100,
                "frequency": "monthly"
            },
            {
                "category": "VAT",
                "services": [
                    "VAT returns",
                    "VAT registration",
                    "Making Tax Digital compliance",
                    "VAT planning",
                    "VAT investigations"
                ],
                "aiSupported": True,
                "humanReview": True,
                "startingPrice": 120,
                "frequency": "quarterly"
            },
            {
                "category": "Audit",
                "services": [
                    "Statutory audit",
                    "Internal audit",
                    "Compliance audit",
                    "Risk assessment",
                    "Audit reports"
                ],
                "aiSupported": False,
                "humanReview": True,
                "startingPrice": 1500,
                "frequency": "annual"
            },
            {
                "category": "Financial Planning",
                "services": [
                    "Business planning",
                    "Cash flow forecasting",
                    "Investment advice",
                    "Retirement planning",
                    "Estate planning"
                ],
                "aiSupported": False,
                "humanReview": True,
                "startingPrice": 500,
                "frequency": "as_needed"
            },
            {
                "category": "Company Secretarial",
                "services": [
                    "Company formation",
                    "Annual returns",
                    "Statutory registers",
                    "Board minutes",
                    "Companies House filings"
                ],
                "aiSupported": True,
                "humanReview": True,
                "startingPrice": 200,
                "frequency": "annual"
            },
            {
                "category": "Consulting",
                "services": [
                    "Business consulting",
                    "Mergers & acquisitions",
                    "Exit strategies",
                    "Restructuring",
                    "Due diligence"
                ],
                "aiSupported": False,
                "humanReview": True,
                "startingPrice": 1000,
                "frequency": "project_based"
            }
        ]
    
    def create_ai_automation(
        self,
        automation_type: str,
        config: Dict
    ) -> Dict:
        """
        Create AI automation for recurring tasks
        
        Args:
            automation_type: Type of automation
            config: Automation configuration
            
        Returns:
            Automation details
        """
        
        automation = {
            "automationId": f"AUTO-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "type": automation_type,
            "config": config,
            "status": "active",
            "createdAt": datetime.now().isoformat(),
            "lastRun": None,
            "nextRun": self._calculate_next_run(config.get('schedule')),
            "tasksCompleted": 0,
            "errorCount": 0,
            "accuracy": 0.0
        }
        
        self.ai_automations.append(automation)
        
        print(f"🤖 AI Automation created: {automation_type}")
        print(f"   Next run: {automation['nextRun']}")
        
        return automation
    
    def _calculate_next_run(self, schedule: str) -> str:
        """Calculate next automation run time"""
        
        schedule_map = {
            "daily": timedelta(days=1),
            "weekly": timedelta(weeks=1),
            "monthly": timedelta(days=30),
            "quarterly": timedelta(days=90)
        }
        
        delta = schedule_map.get(schedule, timedelta(days=1))
        next_run = datetime.now() + delta
        
        return next_run.isoformat()
    
    def get_team_capacity(self) -> Dict:
        """Get current team capacity and utilization"""
        
        total_capacity = sum(acc.get('capacity', 0) for acc in self.accountants)
        ai_capacity = self.accountants[0].get('capacity', 0)  # AI assistant
        human_capacity = total_capacity - ai_capacity
        
        # Calculate utilization (simplified)
        current_tasks = len(self.assignments)
        utilization = (current_tasks / total_capacity * 100) if total_capacity > 0 else 0
        
        return {
            "totalCapacity": total_capacity,
            "aiCapacity": ai_capacity,
            "humanCapacity": human_capacity,
            "currentTasks": current_tasks,
            "utilization": round(utilization, 2),
            "availableSlots": total_capacity - current_tasks,
            "teamSize": len(self.accountants),
            "aiAccountants": 1,
            "humanAccountants": len(self.accountants) - 1
        }
    
    def get_cost_comparison(self, task_data: Dict) -> Dict:
        """Compare cost of AI vs human accountant for a task"""
        
        # AI cost
        ai_accountant = self._get_accountant("AI-001")
        ai_cost = self._estimate_cost(ai_accountant, task_data)
        ai_time = self._estimate_completion(ai_accountant, task_data)
        
        # Human cost
        human_accountant = self._find_best_accountant(
            task_data.get('category'),
            task_data.get('priority', TaskPriority.MEDIUM),
            task_data.get('complexity', 'medium')
        )
        human_cost = self._estimate_cost(human_accountant, task_data)
        human_time = self._estimate_completion(human_accountant, task_data)
        
        savings = human_cost - ai_cost
        savings_percentage = (savings / human_cost * 100) if human_cost > 0 else 0
        
        return {
            "ai": {
                "cost": ai_cost,
                "completionTime": ai_time,
                "accountant": ai_accountant['name']
            },
            "human": {
                "cost": human_cost,
                "completionTime": human_time,
                "accountant": human_accountant['name']
            },
            "savings": round(savings, 2),
            "savingsPercentage": round(savings_percentage, 2),
            "recommendation": "ai" if ai_cost < human_cost and self._is_ai_suitable(
                task_data.get('category'),
                task_data.get('complexity', 'medium'),
                task_data.get('priority', TaskPriority.MEDIUM)
            ) else "human"
        }


# Singleton instance
accountant_service = AccountantService()

