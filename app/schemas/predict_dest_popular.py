from pydantic import BaseModel, Field

class PredictDestPopular(BaseModel):
    origin: str 
    dest: str 
    month: int 
    day_week: int 
    holiday: int = Field(..., ge=0, le=1, description="Must be 0 or 1")
    vacation: int = Field(..., ge=0, le=1, description="Must be 0 or 1")
    important_event: int = Field(..., ge=0, le=1, description="Must be 0 or 1")
    
