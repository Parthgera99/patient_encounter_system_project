# import os

# from sqlalchemy import create_engine
# from sqlalchemy.orm import DeclarativeBase, sessionmaker

# # Detect environment
# DATABASE_URL = os.getenv("DATABASE_URL")

# if DATABASE_URL:
#     # Production / local MySQL
#     engine = create_engine(
#         DATABASE_URL,
#         pool_pre_ping=True,
#         pool_recycle=1800,
#         echo=False,
#     )
# else:
#     # CI / tests / examiner fallback
#     engine = create_engine(
#         "sqlite:///./test.db",
#         connect_args={"check_same_thread": False},
#         echo=False,
#     )


# SessionLocal = sessionmaker(
#     bind=engine,
#     autoflush=False,
#     autocommit=False,
# )


# class Base(DeclarativeBase):
#     pass


# def create_tables():
#     Base.metadata.create_all(bind=engine)


from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# SQLite for all environments
engine = create_engine(
    "sqlite:///./app.db",
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
