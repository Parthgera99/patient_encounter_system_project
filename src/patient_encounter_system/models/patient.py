from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from src.patient_encounter_system.database import Base


class Patient(Base):
    __tablename__ = "parthGeraPatients"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(
        "firstName", String(100), nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        "lastName", String(100), nullable=False
    )

    email: Mapped[str] = mapped_column(
        "email",
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    phone: Mapped[str | None] = mapped_column(
        "phone", String(20), nullable=True
    )

    created_at: Mapped[DateTime] = mapped_column(
        "createdAt",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[DateTime] = mapped_column(
        "updatedAt",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
