from datetime import date, datetime, time

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from src.patient_encounter_system.database import SessionLocal
from src.patient_encounter_system.models.appointment import Appointment
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
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.get(
    "/{appointment_id}",
    response_model=AppointmentRead,
    status_code=status.HTTP_200_OK,
)
def get_appointment_by_id(
    appointment_id: int,
    db: Session = Depends(get_db),
):
    appointment = db.get(Appointment, appointment_id)

    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found",
        )

    return appointment


@router.get(
    "",
    response_model=list[AppointmentRead],
    status_code=status.HTTP_200_OK,
)
def get_appointments_by_date(
    appointment_date: date,
    doctor_id: int | None = None,
    db: Session = Depends(get_db),
):
    """
    Get all appointments for a given date.
    Optionally filter by doctor_id.
    """

    start_dt = datetime.combine(appointment_date, time.min)
    end_dt = datetime.combine(appointment_date, time.max)

    conditions = [
        Appointment.start_time >= start_dt,
        Appointment.start_time <= end_dt,
    ]

    if doctor_id is not None:
        conditions.append(Appointment.doctor_id == doctor_id)

    stmt = select(Appointment).where(and_(*conditions))

    appointments = db.execute(stmt).scalars().all()

    return appointments
