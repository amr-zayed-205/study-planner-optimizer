import json
from pathlib import Path
from typing import List
from ..models.chapter import Chapter

def read_chapters_json(path: str) -> List[Chapter]:
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    data = json.loads(file_path.read_text(encoding="utf-8"))

    chapters = []
    for item in data:
        chapters.append(
            Chapter(
                id=item["id"],
                title=item.get("title", ""),
                time_minutes=item["time_minutes"],
                score_value=item["score_value"],
                prerequisites=item.get("prerequisites", []),
            )
        )
    return chapters
