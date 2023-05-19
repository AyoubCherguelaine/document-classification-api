# api for doc classification 

fastapi app for documents classificatio

## model used

### ocr
 - textract 

### language detection 
 - XLM-Roberta-base-language-detection

### zero shot classification
 - Bart-MNLI-CNN_news



## install 

```bash
 sudo apt-get install tesseract-ocr
```

```bash
pip install -r requirements.txt

```

## Usage

### create a config.py
 create config.py in ./apis containe 

 ```python 
 labels = [] #labels list ["news","sport"]
 huggingface_key = "<huggingface key>"
 deta_key = "<deta key>"

 ```

### run the app

```bash
uvicorn main:app --reload
```

you can check /docs endpoint to get the documentation 
