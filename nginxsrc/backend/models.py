from sqlmodel import SQLModel, Field, Column, Text, create_engine
from ..core.domain.models.server import Server


class ServerData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    data: str = Field(sa_column=Column(Text, nullable=False))  # <- mover nullable para Column

class ServerDTO(Server):
    id: int

engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)
