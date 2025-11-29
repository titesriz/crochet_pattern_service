from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from app.models import Pattern
from app.parser import parse_text_to_pattern
from app.ocr import image_file_to_text

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


@app.post("/parse-image", response_model=Pattern)
async def parse_image_endpoint(
    file: UploadFile = File(...),
    pattern_id: str = "amigurumi_001",
    part_id: str = "head_body",
    part_name: str = "Head / Body",
):
    # 1) OCR : image -> texte brut
    text = image_file_to_text(file)

    # 2) Parser : texte -> Pattern
    pattern = parse_text_to_pattern(
        text=text,
        pattern_id=pattern_id,
        part_id=part_id,
        part_name=part_name,
    )

    return pattern