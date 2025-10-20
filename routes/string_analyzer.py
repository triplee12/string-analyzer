from fastapi import APIRouter, HTTPException, status, Query, Path
from typing import Optional
from schema.string_analyzer import CreateStringPayload, StringResponse, ListResponse
from services.string_service import StringService


router = APIRouter()


@router.post("", response_model=StringResponse, status_code=status.HTTP_201_CREATED)
def create_string(payload: CreateStringPayload):
    value = payload.value
    if not isinstance(value, str):
        raise HTTPException(status_code=422, detail='"value" must be a string')
    try:
        props = StringService.create(value)
    except ValueError as e:
        if str(e) == "exists":
            raise HTTPException(status_code=409, detail="String already exists")
        raise
    return {
        "id": props["sha256_hash"],
        "value": value,
        "properties": {
            "length": props["length"],
            "is_palindrome": props["is_palindrome"],
            "unique_characters": props["unique_characters"],
            "word_count": props["word_count"],
            "sha256_hash": props["sha256_hash"],
            "character_frequency_map": props["character_frequency_map"],
        },
        "created_at": props["created_at"],
    }


@router.get("/{string_value}", response_model=StringResponse)
def get_string(string_value: str = Path(...)):
    res = StringService.get_by_value(string_value)
    if not res:
        raise HTTPException(status_code=404, detail="String not found")
    return {
        "id": res["properties"]["sha256_hash"],
        "value": res["value"],
        "properties": res["properties"],
        "created_at": res["created_at"]
    }


@router.get("", response_model=ListResponse)
def list_strings(
    is_palindrome: Optional[bool] = Query(None),
    min_length: Optional[int] = Query(None, ge=0),
    max_length: Optional[int] = Query(None, ge=0),
    word_count: Optional[int] = Query(None, ge=0),
    contains_character: Optional[str] = Query(None, min_length=1, max_length=1),
):
    if min_length is not None and max_length is not None and min_length > max_length:
        raise HTTPException(status_code=400, detail="min_length cannot be > max_length")
    filters = {
        "is_palindrome": is_palindrome,
        "min_length": min_length,
        "max_length": max_length,
        "word_count": word_count,
        "contains_character": contains_character
    }
    data = StringService.list(filters)
    applied = {k: v for k, v in filters.items() if v is not None}
    return {"data": data, "count": len(data), "filters_applied": applied}


@router.delete("/{string_value}", status_code=status.HTTP_204_NO_CONTENT)
def delete_string(string_value: str = Path(...)):
    ok = StringService.delete(string_value)
    if not ok:
        raise HTTPException(status_code=404, detail="String not found")
    return None
