from pydantic import BaseModel
from typing import Dict, Optional


class CreateStringPayload(BaseModel):
    value: str


class PropertiesModel(BaseModel):
    length: int
    is_palindrome: bool
    unique_characters: int
    word_count: int
    sha256_hash: str
    character_frequency_map: Dict[str, int]


class StringResponse(BaseModel):
    id: str
    value: str
    properties: PropertiesModel
    created_at: str


class ListResponse(BaseModel):
    data: list[StringResponse]
    count: int
    filters_applied: Optional[dict]


class NLResponse(BaseModel):
    data: list[StringResponse]
    count: int
    interpreted_query: dict
