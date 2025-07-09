from fastapi import FastAPI, UploadFile
from parser import extract_sow_data

app = FastAPI(title="SOW Extractor API")

@app.post("/extract")
async def extract(file: UploadFile):
    content = await file.read()
    result = extract_sow_data(content)
    return result
