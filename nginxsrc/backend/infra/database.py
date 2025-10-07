from sqlmodel import SQLModel, create_engine
from sqlalchemy.engine import Engine

def create_engine_instance(uri: str) -> Engine:
    return create_engine(uri)

def create_tables(engine: Engine):
    SQLModel.metadata.create_all(engine)
