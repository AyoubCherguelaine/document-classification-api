import requests
import re
from . import config, text_processing


def pred(text):
    try:
        text = text_processing.preprocess_text(text)
        
        if text is None:
            return None
        
        response = requests.post("https://team-language-detector-languagedetector.hf.space/run/predict", json={
	            "data": [
		                text,
	                    ]
                                }).json()
        
        if response is not None:
            data = response["data"]
            return data[0]["label"]
    except Exception as e:
        # Handle any other exceptions
        print(f"Exception: {e}")
    
    return None