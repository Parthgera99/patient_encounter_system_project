from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.appointment import Appointment
from src.models.doctor import Doctor
from src.schemas.appointment import AppointmentCreate


def _to_naive_utc(dt):
    """
    Convert aware datetime to naive UTC.
    Leave naive datetimes unchanged.
    """
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


def _ensure_future(start_time: datetime) -> None:
    start_time = _to_naive_utc(start_time)
    now = datetime.utcnow()  # naive UTC

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
    # Normalize incoming time
    start_time = _to_naive_utc(start_time)
    new_end = start_time + timedelta(minutes=duration_minutes)

    stmt = select(Appointment).where(Appointment.doctor_id == doctor_id)

    existing_appointments = db.execute(stmt).scalars().all()

    for appt in existing_appointments:
        existing_start = _to_naive_utc(appt.start_time)
        existing_end = existing_start + timedelta(minutes=appt.duration_minutes)

        if existing_start < new_end and existing_end > start_time:
            return True

    return False


def create_appointment(db: Session, data: AppointmentCreate) -> Appointment:
    start_time = _to_naive_utc(data.start_time)

    _ensure_future(start_time)
    _ensure_doctor_active(db, data.doctor_id)

    if _has_overlap(
        db,
        data.doctor_id,
        start_time,
        data.duration_minutes,
    ):
        raise ValueError("Doctor already has an appointment at this time")

    appointment = Appointment(
        patient_id=data.patient_id,
        doctor_id=data.doctor_id,
        start_time=start_time,
        duration_minutes=data.duration_minutes,
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment
