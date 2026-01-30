from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    func,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.patient_encounter_system.database import Base


class Appointment(Base):
    __tablename__ = "parthGeraAppointments"

    id: Mapped[int] = mapped_column(primary_key=True)

    patient_id: Mapped[int] = mapped_column(
        ForeignKey("parthGeraPatients.id", ondelete="RESTRICT"),
        nullable=False,
    )

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("parthGeraDoctors.id", ondelete="RESTRICT"),
        nullable=False,
    )

    start_time: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        Index("ix_appointments_doctor_start", "doctor_id", "start_time"),
    )
