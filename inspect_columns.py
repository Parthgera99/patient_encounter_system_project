from sqlalchemy import inspect

from src.database import engine

inspector = inspect(engine)

columns = inspector.get_columns("parthPatients")

for col in columns:
    print(col["name"], col["type"])
