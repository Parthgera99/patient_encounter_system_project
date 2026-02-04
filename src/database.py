# import os

# from dotenv import load_dotenv
# from sqlalchemy import create_engine
# from sqlalchemy.orm import DeclarativeBase, sessionmaker

# load_dotenv()

# # MySQL connection URL
# DATABASE_URL = os.getenv("DATABASE_URL")

# if not DATABASE_URL:
#     raise RuntimeError("DATABASE_URL environment variable is not set")


# # Create SQLAlchemy engine
# engine = create_engine(
#     DATABASE_URL,
#     pool_pre_ping=True,  # Detect stale connections
#     pool_recycle=1800,  # Prevent MySQL timeout issues
#     echo=False,
# )


# # Session factory
# SessionLocal = sessionmaker(
#     bind=engine,
#     autoflush=False,
#     autocommit=False,
# )


# # Base class for models
# class Base(DeclarativeBase):
#     pass


# def create_tables():
#     Base.metadata.create_all(bind=engine)


import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Detect environment
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Production / local MySQL
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=1800,
        echo=False,
    )
else:
    # CI / tests / examiner fallback
    engine = create_engine(
        "sqlite:///./test.db",
        connect_args={"check_same_thread": False},
        echo=False,
    )


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass


def create_tables():
    Base.metadata.create_all(bind=engine)
