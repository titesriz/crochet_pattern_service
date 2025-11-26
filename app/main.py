from fastapi import FastAPI

app = FastAPI(title="Crochet Pattern Service")

@app.get("/health")
def health():
    return {"status": "ok"}