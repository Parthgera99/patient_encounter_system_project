from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class PatientCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=20)


class PatientRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
