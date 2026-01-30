from datetime import datetime, timedelta, timezone

from sqlalchemy import func
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.patient_encounter_system.models.appointment import Appointment
from src.patient_encounter_system.models.doctor import Doctor
from src.patient_encounter_system.schemas.appointment import AppointmentCreate


def _ensure_future(start_time: datetime) -> None:
    now = datetime.now(timezone.utc)
    if start_time <= now:
        raise ValueError("Appointment must be scheduled in the future")


def _ensure_doctor_active(db: Session, doctor_id: int) -> None:
    doctor = db.get(Doctor, doctor_id)
    if not doctor:
        raise ValueError("Doctor not found")
    if not doctor.is_active:
        raise ValueError("Doctor is inactive and cannot accept appointments")


def _has_overlap(
    db: Session,
    doctor_id: int,
    start_time: datetime,
    duration_minutes: int,
) -> bool:
    end_time = start_time + timedelta(minutes=duration_minutes)

    stmt = (
        select(Appointment.id)
        .where(
            Appointment.doctor_id == doctor_id,
            Appointment.start_time < end_time,
            Appointment.start_time
            + func.interval(Appointment.duration_minutes, "MINUTE")
            > start_time,
        )
        .limit(1)
    )

    return db.execute(stmt).first() is not None



def create_appointment(
    db: Session,
    data: AppointmentCreate,
) -> Appointment:
    # 1. Future check
    _ensure_future(data.start_time)

    # 2. Doctor active check
    _ensure_doctor_active(db, data.doctor_id)

    # 3. Overlap check
    if _has_overlap(
        db,
        data.doctor_id,
        data.start_time,
        data.duration_minutes,
    ):
        raise ValueError("Doctor already has an overlapping appointment")

    appointment = Appointment(
        patient_id=data.patient_id,
        doctor_id=data.doctor_id,
        start_time=data.start_time,
        duration_minutes=data.duration_minutes,
    )

    db.add(appointment)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # Handles duplicate (unique constraint) safely
        raise ValueError("Duplicate appointment is not allowed")

    db.refresh(appointment)
    return appointment
