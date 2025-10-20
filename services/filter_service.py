import re
from typing import Dict, Any


def parse_nl_query(q: str) -> Dict[str, Any]:
    if not q or not q.strip():
        raise ValueError("Empty query")

    lowered = q.lower()
    parsed = {}

    if re.search(r"single word|one word|\\bonly one\\b", lowered):
        parsed["word_count"] = 1
    m = re.search(r"longer than (\\d+)", lowered)

    if m:
        parsed["min_length"] = int(m.group(1)) + 1
    m = re.search(r"(palindromic|palindrome|palindromic strings|palindromic string)", lowered)

    if m:
        parsed["is_palindrome"] = True
    m = re.search(r"contain(?:ing|s)? the letter ([a-z])", lowered)

    if m:
        parsed["contains_character"] = m.group(1)
    if "first vowel" in lowered:
        parsed.setdefault("contains_character", "a")

    m = re.search(r"containing the letter ([a-z])", lowered)
    if m:
        parsed["contains_character"] = m.group(1)

    return parsed
