from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.patient_encounter_system.database import SessionLocal
from src.patient_encounter_system.models.doctor import Doctor
from src.patient_encounter_system.schemas.doctor import DoctorCreate, DoctorRead

router = APIRouter(prefix="/doctors", tags=["Doctors"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "",
    response_model=DoctorRead,
    status_code=status.HTTP_201_CREATED,
)
def create_doctor(data: DoctorCreate, db: Session = Depends(get_db)):
    doctor = Doctor(**data.model_dump())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


@router.get(
    "/{doctor_id}",
    response_model=DoctorRead,
)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor
