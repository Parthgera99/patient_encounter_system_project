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
    start_time,
    duration_minutes: int,
) -> bool:
    # Normalize incoming time to UTC
    if start_time.tzinfo is None or start_time.utcoffset() is None:
        start_utc = start_time.replace(tzinfo=timezone.utc)
    else:
        start_utc = start_time.astimezone(timezone.utc)

    end_utc = start_utc + timedelta(minutes=duration_minutes)

    # Fetch existing appointments for the doctor
    existing = db.execute(
        select(Appointment.start_time, Appointment.duration_minutes)
        .where(Appointment.doctor_id == doctor_id)
    ).all()

    for appt_start, appt_duration in existing:
        # Normalize DB time to UTC
        if appt_start.tzinfo is None or appt_start.utcoffset() is None:
            appt_start_utc = appt_start.replace(tzinfo=timezone.utc)
        else:
            appt_start_utc = appt_start.astimezone(timezone.utc)

        appt_end_utc = appt_start_utc + timedelta(minutes=appt_duration)

        # 🔑 Canonical overlap check
        if start_utc < appt_end_utc and end_utc > appt_start_utc:
            return True

    return False




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
