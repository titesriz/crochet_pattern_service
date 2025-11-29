from pydantic import BaseModel
from typing import List, Optional


class Round(BaseModel):
    round: int
    raw_text: str
    total_stitches: Optional[int] = None


class Part(BaseModel):
    part_id: str               # ex: "head_body"
    name: str                  # ex: "Head / Body"
    work_type: str             # ex: "rounds"
    rounds: List[Round]


class Pattern(BaseModel):
    schema_version: str = "1.0"
    pattern_id: str            # ex: "ours_001"
    part: Part                 # pour le MVP : une seule partie