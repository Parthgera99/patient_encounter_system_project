from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.patient_encounter_system.database import SessionLocal
from src.patient_encounter_system.schemas.appointment import (
    AppointmentCreate,
    AppointmentRead,
)
from src.patient_encounter_system.services.appointment_service import (
    create_appointment,
)

router = APIRouter(prefix="/appointments", tags=["Appointments"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "",
    response_model=AppointmentRead,
    status_code=status.HTTP_201_CREATED,
)
def schedule_appointment(
    data: AppointmentCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_appointment(db, data)
    except ValueError as e:
        message = str(e)

        if "overlap" in message.lower() or "duplicate" in message.lower():
            raise HTTPException(status_code=409, detail=message)

        raise HTTPException(status_code=400, detail=message)
