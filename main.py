from fastapi import FastAPI, UploadFile, Header, HTTPException
from parser import extract_sow_data
import os

app = FastAPI(title="SOW Extractor API")

API_KEY = os.environ.get("API_KEY")  # lê do ambiente

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/extract")
async def extract(
    file: UploadFile,
    authorization: str = Header(None)
):
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    content = await file.read()
    result = extract_sow_data(content)
    return result
