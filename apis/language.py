import requests
import re
from . import config, text_processing

API_URL = "https://api-inference.huggingface.co/models/papluca/xlm-roberta-base-language-detection"
headers = {"Authorization": "Bearer " + config.huggingface_key}


def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception if the request was not successful
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle request-related exceptions
        print(f"Request Exception: {e}")
    except ValueError as e:
        # Handle JSON decoding exceptions
        print(f"JSON Decoding Exception: {e}")
    return None


def pred(text):
    try:
        text = text_processing.preprocess_text(text)
        
        if text is None:
            return None
        
        output = query({"inputs": text})
        
        if output is not None:
            return output[0][0]
    except Exception as e:
        # Handle any other exceptions
        print(f"Exception: {e}")
    
    return None