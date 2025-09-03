from pydantic import BaseModel, Field

class PlanOutput(BaseModel):
    outline: str = Field(description="The outline of the report")
    
class GetHumanInTheLoopInput(BaseModel):
    """Input for getting more information"""
    questions: str

class GetHumanInTheLoopOutput(BaseModel):
    """Response for getting more information"""
    answer: str
    
class GetPlanInput(BaseModel):
    """Input for getting a plan"""
    instructions_for_plan: str

class GetPlanOutput(BaseModel):
    """Response for getting a plan"""
    plan: str
