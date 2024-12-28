##Importing Pacakges
from enum import Enum
from typing import List,Optional
from pydantic import BaseModel,Field,validator

class Department(str,Enum):
    """Valid department categories"""
    PUBLIC_WORKS = "PUBLIC_WORKS"
    SANITATION = "SANITATION"
    PARKS_REC = "PARKS_REC"
    TRANSPORTATION = "TRANSPORTATION"
    PUBLIC_SAFETY = "PUBLIC_SAFETY"
    CODE_ENFORCEMENT = "CODE_ENFORCEMENT"
    UTILITIES = "UTILITIES"
    ENVIRONMENTAL = "ENVIRONMENTAL"
    HEALTH = "HEALTH"
    ANIMAL_CONTROL = "ANIMAL_CONTROL"

class RecommendedAction(BaseModel):
    """Represents a specific action needed to address the issue"""
    action: str = Field(..., description="Description of what needs to be done")
    priority: str = Field(..., description="Priority level of the action")
    timeframe: str = Field(..., description="When the action should be completed")
    departments: List[Department] = Field(..., description="Departments responsible for this action")
    
    @validator('priority')
    def validate_priority(cls, v):
        allowed = ['HIGH', 'MEDIUM', 'LOW']
        if v.upper() not in allowed:
            raise ValueError(f'Priority must be one of {allowed}')
        return v.upper()

class CommunityIssueAnalysis(BaseModel):
    """Main model for community issue analysis results"""
    issue_type: str = Field(..., description="Main category of the problem")
    severity: str = Field(..., description="Overall severity rating")
    urgency: str = Field(..., description="How quickly this needs attention")
    location_context: str = Field(..., description="Where this issue is located")
    safety_concerns: List[str] = Field(..., description="List of identified safety risks")
    community_impact: List[str] = Field(..., description="Ways this affects local residents")
    recommended_actions: List[RecommendedAction] = Field(..., description="List of actions needed to fix the issue")
    primary_department: Department = Field(..., description="Main department responsible for addressing this issue")
    additional_notes: Optional[str] = Field(None, description="Any other important observations")

    @validator('severity')
    def validate_severity(cls, v):
        allowed = ['HIGH', 'MEDIUM', 'LOW']
        if v.upper() not in allowed:
            raise ValueError(f'Severity must be one of {allowed}')
        return v.upper()

    @validator('urgency')
    def validate_urgency(cls, v):
        allowed = ['IMMEDIATE', 'SOON', 'ROUTINE']
        if v.upper() not in allowed:
            raise ValueError(f'Urgency must be one of {allowed}')
        return v.upper()