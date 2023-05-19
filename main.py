from fastapi import FastAPI, UploadFile,File, HTTPException
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from apis import doc_classifier, language , transformation, config
import shutil
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


class TextInput(BaseModel):
    text: str

@app.post("/api/classifier")
async def read_root(text :TextInput ):

    out= doc_classifier.pred(text.text)
    if out != None:
        return out
    else:
        return {"Problem":"no solution !"}


@app.post("/api/language")
async def read_root(text :TextInput ):

    out= language.pred(text.text)

    if out != None:
        return out
    else:
        return {"Problem":"no solution !"}
    

@app.post("/api/transformer")
async def upload_file(file: UploadFile = File(...)):
    # Save the file in the "/static" folder
    file_path = f"static/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    text = transformation.extract_text(file.filename, file_path)


    return {"filename": file.filename, "content": text}



@app.post("/classifie")
async def upload_file(file: UploadFile = File(...)):
    # Save the file in the "/static" folder
    file_path = f"static/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from the file
    text = transformation.extract_text(file.filename, file_path)
    
    # Perform language detection
    lang = language.pred(text)

    if lang != None:
        if lang["label"] == "en":
            # If the language is English, continue the process
            # Perform document classification
            topic = doc_classifier.pred(text)
            
            if topic != None:
                # Return the classification results
                result = {
                    "label": topic["labels"][0],
                    "score": topic["scores"][0],
                    "language": "en"
                }
            else:
                # Document classification failed
                result = {"exception": 4, "type": "classifier"}
        else:
            # Non-English language detected
            result = {
                "exception": 3,
                "type": "not english",
                "language": lang["label"]
            }
    else:
        # Language detection failed
        result = {"exception": 2, "type": "language detection"}
    
    # Delete the file after processing
    os.remove(file_path)
    
    return result

@app.post("/configlabel")
async def configLabel(text :TextInput):
    # Remove the square brackets and spaces
    cleaned_str = text.text.strip('[]').replace(' ', '')

    # Split the string by comma and create a list
    result_list = cleaned_str.split(',')

    config.labels = result_list

    