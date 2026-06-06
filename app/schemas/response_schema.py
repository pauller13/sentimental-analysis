from sqlmodel import SQLModel
from typing import Any


class ResponseSchema(SQLModel):
    success: bool
    message: str
    data: Any