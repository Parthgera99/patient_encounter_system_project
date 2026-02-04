from fastapi import FastAPI

from src.database import create_tables
from src.routes import appointments, doctors, patients

app = FastAPI(title="Medical Encounter Management System")

create_tables()


app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)


@app.get("/health")
def health():
    return {"status": "ok"}
