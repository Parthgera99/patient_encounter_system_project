from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database import SessionLocal
from src.models.patient import Patient
from src.schemas.patient import PatientCreate, PatientRead

router = APIRouter(prefix="/patients", tags=["Patients"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "",
    response_model=PatientRead,
    status_code=status.HTTP_201_CREATED,
)
def create_patient(data: PatientCreate, db: Session = Depends(get_db)):
    patient = Patient(**data.model_dump())
    db.add(patient)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Patient with this email already exists",
        )

    db.refresh(patient)
    return patient


@router.get(
    "/{patient_id}",
    response_model=PatientRead,
)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
