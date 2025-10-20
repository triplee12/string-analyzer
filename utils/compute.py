from datetime import datetime, timezone
from collections import Counter
import hashlib
from typing import Dict, Any


def compute_properties(value: str) -> Dict[str, Any]:
    length = len(value)
    lowered = value.lower()
    is_pal = lowered == lowered[::-1]
    unique_chars = len(set(value))
    word_count = len(value.split())
    sha = hashlib.sha256(value.encode("utf-8")).hexdigest()
    freq = dict(Counter(value))
    created_at = datetime.now(timezone.utc).isoformat()
    return {
        "length": length,
        "is_palindrome": is_pal,
        "unique_characters": unique_chars,
        "word_count": word_count,
        "sha256_hash": sha,
        "character_frequency_map": freq,
        "created_at": created_at,
    }
