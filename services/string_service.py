from sqlmodel import Session, select
from db.database import engine
from models.string_analyzer import AnalyzedString
from utils.compute import compute_properties
from typing import Optional, Dict, Any, List


class StringService:
    @staticmethod
    def create(value: str) -> Dict[str, Any]:
        props = compute_properties(value)
        sha = props["sha256_hash"]
        with Session(engine) as sess:
            existing = sess.get(AnalyzedString, sha)
            if existing:
                raise ValueError("exists")
            obj = AnalyzedString(
                id=sha,
                value=value,
                length=props["length"],
                is_palindrome=props["is_palindrome"],
                unique_characters=props["unique_characters"],
                word_count=props["word_count"],
                character_frequency_map=props["character_frequency_map"],
                created_at=props["created_at"],
            )
            sess.add(obj)
            sess.commit()
        return props

    @staticmethod
    def get_by_value(value: str) -> Optional[Dict[str, Any]]:
        import hashlib
        sha = hashlib.sha256(value.encode("utf-8")).hexdigest()
        with Session(engine) as sess:
            obj = sess.get(AnalyzedString, sha)
            if not obj:
                return None

            return {
                "value": obj.value,
                "properties": {
                    "length": obj.length,
                    "is_palindrome": obj.is_palindrome,
                    "unique_characters": obj.unique_characters,
                    "word_count": obj.word_count,
                    "sha256_hash": obj.id,
                    "character_frequency_map": obj.character_frequency_map,
                },
                "created_at": obj.created_at,
            }
    
    @staticmethod
    def list(filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        q = select(AnalyzedString)
        if filters.get("is_palindrome") is not None:
            q = q.where(AnalyzedString.is_palindrome == filters["is_palindrome"])
        if filters.get("min_length") is not None:
            q = q.where(AnalyzedString.length >= filters["min_length"])
        if filters.get("max_length") is not None:
            q = q.where(AnalyzedString.length <= filters["max_length"])
        if filters.get("word_count") is not None:
            q = q.where(AnalyzedString.word_count == filters["word_count"])
        if filters.get("contains_character") is not None:
            ch = filters["contains_character"]
            q = q.where(AnalyzedString.value.contains(ch))
        with Session(engine) as sess:
            results = sess.exec(q).all()
            out = []
            for obj in results:
                out.append({
                    "id": obj.id,
                    "value": obj.value,
                    "properties": {
                        "length": obj.length,
                        "is_palindrome": obj.is_palindrome,
                        "unique_characters": obj.unique_characters,
                        "word_count": obj.word_count,
                        "sha256_hash": obj.id,
                        "character_frequency_map": obj.character_frequency_map,
                    },
                    "created_at": obj.created_at,
                })
            return out

    @staticmethod
    def delete(value: str) -> bool:
        import hashlib
        sha = hashlib.sha256(value.encode("utf-8")).hexdigest()
        with Session(engine) as sess:
            obj = sess.get(AnalyzedString, sha)
            if not obj:
                return False

            sess.delete(obj)
            sess.commit()
            return True
