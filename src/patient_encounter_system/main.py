from fastapi import FastAPI

from src.patient_encounter_system.database import create_tables
from src.patient_encounter_system.routes import patients, doctors, appointments

app = FastAPI(title="Medical Encounter Management System")


@app.on_event("startup")
def on_startup():
    create_tables()


app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)


@app.get("/health")
def health():
    return {"status": "ok"}
