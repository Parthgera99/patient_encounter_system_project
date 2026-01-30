from fastapi import FastAPI

from src.patient_encounter_system.database import create_tables

app = FastAPI(title="Medical Encounter Management System")


@app.on_event("startup")
def on_startup():
    create_tables()
