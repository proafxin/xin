from pydantic import BaseModel


class Base(BaseModel):
    """All models must be a pydantic model."""


class QueryResult(Base):
    table_name: str
