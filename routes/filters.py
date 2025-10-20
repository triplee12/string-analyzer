from fastapi import APIRouter, HTTPException, Query
from services.string_service import StringService
from services.filter_service import parse_nl_query


router = APIRouter()


@router.get("/strings/filter-by-natural-language")
def filter_by_nl(query: str = Query(...)):
    try:
        parsed = parse_nl_query(query)
    except ValueError:
        raise HTTPException(status_code=400, detail="Unable to parse natural language query")

    if "min_length" in parsed and "max_length" in parsed and parsed["min_length"] > parsed["max_length"]:
        raise HTTPException(
            status_code=422,
            detail="Parsed query resulted in conflicting filters"
        )

    data = StringService.list(parsed)
    return {
        "data": data,
        "count": len(data),
        "interpreted_query": {
            "original": query,
            "parsed_filters": parsed
        }
    }
