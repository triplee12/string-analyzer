from sqlmodel import SQLModel, Field, Column
from typing import Dict
from sqlalchemy import JSON


class AnalyzedString(SQLModel, table=True):
    id: str = Field(primary_key=True, index=True)
    value: str
    length: int
    is_palindrome: bool
    unique_characters: int
    word_count: int
    character_frequency_map: Dict[str, int] = Field(sa_column=Column(JSON))
    created_at: str
