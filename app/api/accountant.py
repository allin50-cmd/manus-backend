"""
Accountant Services API
Endpoints for managing accountant services (AI and human)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

import sys
sys.path.append('/home/ubuntu/fineguard-backend')

from app.services.accountant_service import accountant_service, AccountantType, ServiceCategory, TaskPriority


router = APIRouter()


# Request/Response Models
class TaskRequest(BaseModel):
    taskId: str
    category: str
    priority: str = "medium"
    complexity: str = "medium"
    estimatedHours: float = 2.0
    description: str
    clientId: str


class AutomationRequest(BaseModel):
    type: str
    schedule: str
    config: Dict


# Endpoints

@router.get("/accountants")
async def get_accountants():
    """Get list of all accountants (AI and human)"""
    return {
        "status": "success",
        "accountants": accountant_service.accountants
    }


@router.get("/accountants/{accountant_id}")
async def get_accountant(accountant_id: str):
    """Get specific accountant details"""
    accountant = accountant_service._get_accountant(accountant_id)
    
    if not accountant:
        raise HTTPException(status_code=404, detail="Accountant not found")
    
    return {
        "status": "success",
        "accountant": accountant
    }


@router.get("/services")
async def get_services():
    """Get all available accounting services"""
    return {
        "status": "success",
        "services": accountant_service.get_available_services()
    }


@router.post("/tasks/assign")
async def assign_task(task: TaskRequest):
    """Assign task to best accountant (AI or human)"""
    
    task_data = task.dict()
    
    try:
        assignment = accountant_service.assign_task(task_data, prefer_ai=True)
        
        return {
            "status": "success",
            "assignment": assignment
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tasks/{task_id}/cost-comparison")
async def get_cost_comparison(task_id: str, task: TaskRequest):
    """Compare AI vs human cost for a task"""
    
    task_data = task.dict()
    
    try:
        comparison = accountant_service.get_cost_comparison(task_data)
        
        return {
            "status": "success",
            "comparison": comparison
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/team/capacity")
async def get_team_capacity():
    """Get current team capacity and utilization"""
    return {
        "status": "success",
        "capacity": accountant_service.get_team_capacity()
    }


@router.post("/automations")
async def create_automation(automation: AutomationRequest):
    """Create AI automation for recurring tasks"""
    
    try:
        result = accountant_service.create_ai_automation(
            automation.type,
            automation.config
        )
        
        return {
            "status": "success",
            "automation": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/automations")
async def get_automations():
    """Get all AI automations"""
    return {
        "status": "success",
        "automations": accountant_service.ai_automations
    }


@router.get("/assignments")
async def get_assignments():
    """Get all task assignments"""
    return {
        "status": "success",
        "assignments": accountant_service.assignments
    }


@router.get("/assignments/{assignment_id}")
async def get_assignment(assignment_id: str):
    """Get specific assignment details"""
    assignment = next(
        (a for a in accountant_service.assignments if a['assignmentId'] == assignment_id),
        None
    )
    
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    return {
        "status": "success",
        "assignment": assignment
    }

