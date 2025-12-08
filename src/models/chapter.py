from dataclasses import dataclass
from typing import List

@dataclass
class Chapter:
    id: str
    title: str
    time_minutes: int
    score_value: float
    prerequisites: List[str]
