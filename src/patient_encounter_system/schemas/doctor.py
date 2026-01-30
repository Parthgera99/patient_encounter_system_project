from pydantic import BaseModel, Field
from datetime import datetime


class DoctorCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=150)
    specialization: str = Field(min_length=1, max_length=100)


class DoctorRead(BaseModel):
    id: int
    full_name: str
    specialization: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
