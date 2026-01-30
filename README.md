# Patient Encounter System – Backend (FastAPI + MySQL)

## 📌 Overview
The **Patient Encounter System** is a production-style backend application built using **FastAPI** and **SQLAlchemy ORM**.  
It manages patients, doctors, and appointments while enforcing real-world business rules such as uniqueness, validation, and scheduling constraints.

This project is designed as a **realistic backend system** with clean architecture, proper validation, database integrity, and automated tests.

---

## 🚀 Features
- Patient management with **unique email enforcement**
- Doctor management with active/inactive status
- Appointment scheduling with:
  - Future-only appointments
  - No overlapping appointments per doctor
- Proper request/response validation
- Clean error handling with correct HTTP status codes
- Automated testing using pytest

---

## 🛠 Tech Stack
- **Python** 3.10
- **FastAPI** – API framework
- **SQLAlchemy ORM** – Database interaction
- **MySQL** – Relational database
- **Poetry** – Dependency & environment management
- **Pytest** – Automated testing
- **Uvicorn** – ASGI server

---

## 🧱 Project Architecture
The project follows a clean, layered architecture:

src/patient_encounter_system/
├── main.py # FastAPI app entry point
├── database.py # DB engine, session, create_all
├── models/ # SQLAlchemy ORM models
├── schemas/ # Pydantic request/response schemas
├── routes/ # API routes
├── services/ # Business logic layer
tests/
├── test_patients.py
├── test_doctors.py
├── test_appointments.py


### Layer Responsibilities
- **Routes**: Handle HTTP requests & responses
- **Schemas**: Validate input/output data
- **Services**: Business rules and validations
- **Models**: Database mappings
- **Database**: Connection and session management

---

## 🗄 Database Design
- Uses a **shared MySQL database**
- Tables are created using `create_all()` for safe bootstrapping
- Database tables use **camelCase naming** (legacy/shared DB)
- Python models use **snake_case attributes**, explicitly mapped to camelCase DB columns
- **Alembic is configured but not used** to avoid impacting other users in the shared database

### Key Constraints
- `email` in patients table is **UNIQUE**
- Appointments enforce:
  - No overlapping times per doctor
  - Valid foreign key references
  - Future start times only

---

## ✅ Validation & Error Handling
- Email validation is done using **Pydantic `EmailStr`**
- Database constraint violations are converted into meaningful API errors
- Correct HTTP status codes are used:
  - `201 Created`
  - `400 Bad Request`
  - `404 Not Found`
  - `409 Conflict`

---

## ▶️ Running the Application

### 1️⃣ Install dependencies
```bash
poetry install
```

### 2️⃣ Start the server
```bash
poetry run uvicorn src.patient_encounter_system.main:app --reload
```

### 3️⃣ Open API documentation
```bash
http://127.0.0.1:8000/docs
```

## 🧪 Running Tests
All tests are written using pytest and run against the real application.
```bash
poetry run pytest -v
```
### Test coverage is above 90% and includes:

- Patient creation & duplicate handling
- Doctor creation & retrieval
- Appointment creation & conflict prevention
- Error and edge-case scenarios

## 🧠 Key Design Decisions

### Database-first integrity: Core rules enforced at DB level
### Service layer: Business logic kept independent of FastAPI
### Explicit column mapping: Supports legacy camelCase DB schema
### Poetry-managed environment: No manual virtual environments
### Shared DB safety: No destructive migrations

## 📖 Example Business Rules

- A patient email must be unique
- Appointments cannot be scheduled in the past
- Doctors cannot have overlapping appointments
- Inactive doctors cannot accept appointments

## 🎯 Conclusion

### This project demonstrates:

- Clean backend architecture
- Proper use of FastAPI & SQLAlchemy
- Real-world validation and constraints
- Test-driven confidence in functionality
- It is suitable for training, evaluation, and portfolio demonstration.

