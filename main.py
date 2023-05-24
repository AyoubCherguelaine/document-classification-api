from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from apis import doc_classifier, language, transformation, config
import shutil
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


class TextInput(BaseModel):
    text: str


@app.post("/api/classifier")
async def classify_text(text: TextInput):
    out = doc_classifier.pred(text.text)
    if out is not None:
        return out
    else:
        return {"Problem": "no solution!"}


@app.post("/api/language")
async def detect_language(text: TextInput):
    out = language.pred(text.text)
    if out is not None:
        return out
    else:
        return {"Problem": "no solution!"}


@app.post("/api/transformer")
async def transform_file(file: UploadFile = File(...)):
    file_path = f"static/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    text = transformation.extract_text(file.filename, file_path)
    return {"filename": file.filename, "content": text}


@app.post("/classify")
async def classify_uploaded_file(file: UploadFile = File(...)):
    file_path = f"static/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    text = transformation.extract_text(file.filename, file_path)
    
    lang = language.pred(text)
    if lang is not None:
        topic = doc_classifier.pred(text)
        if lang == "en":
            
            
            result = {
                    "label": topic,
                    "language": "en"
                }
        else:
            result = {
                "type": "not english",
                "language": lang,
                "label": topic
            }
    else:
        result = {"exception": 2, "type": "language detection"}
    os.remove(file_path)
    return result


@app.post("/configlabel")
async def configure_labels(text: TextInput):
    cleaned_str = text.text.strip('[]').replace(' ', '')
    result_list = cleaned_str.split(',')
    config.labels = result_list


@app.get("/labels")
async def get_labels():
    return config.labels


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,  port=4002)
