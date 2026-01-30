from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class AppointmentCreate(BaseModel):
    patient_id: int = Field(gt=0)
    doctor_id: int = Field(gt=0)
    start_time: datetime
    duration_minutes: int = Field(ge=15, le=180)

    @field_validator("start_time")
    @classmethod
    def validate_timezone(cls, value: datetime):
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError("start_time must be timezone-aware")
        return value


class AppointmentRead(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    start_time: datetime
    duration_minutes: int
    created_at: datetime

    class Config:
        from_attributes = True
