import requests
from . import config, text_processing
import re

API_URL = "https://api-inference.huggingface.co/models/AyoubChLin/Bart-MNLI-CNN_news"
headers = {"Authorization": "Bearer " + config.huggingface_key}



def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception if the request was not successful
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle request-related exceptions
        print(f"Request Exception: {e}")
        return None
    except ValueError as e:
        # Handle JSON decoding exceptions
        print(f"JSON Decoding Exception: {e}")
        return None

def pred(text):
    try:
        text = text_processing.preprocess_text(text)
        output = query({
            "inputs": text,
            "parameters": {"candidate_labels": config.labels},
        })

        return output
        
    except Exception as e:
        # Handle any other exceptions
        print(f"Exception: {e}")
        return None