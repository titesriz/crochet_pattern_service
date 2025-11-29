from fastapi import FastAPI
from pydantic import BaseModel

from app.models import Pattern
from app.parser import parse_text_to_pattern

app = FastAPI(title="Crochet Pattern Service")

@app.get("/health")
def health():
    return {"status": "ok"}

class ParseTextRequest(BaseModel):
    text: str
    pattern_id: str = "amigurumi_001"
    part_id: str = "head_body"
    part_name: str = "Head / Body"


@app.post("/parse-text", response_model=Pattern)
def parse_text_endpoint(payload: ParseTextRequest):
    pattern = parse_text_to_pattern(
        text=payload.text,
        pattern_id=payload.pattern_id,
        part_id=payload.part_id,
        part_name=payload.part_name,
    )
    return pattern