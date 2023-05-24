import requests
from . import config, text_processing
import re
from gradio_client import Client





import json




def pred(text):
    try:
        client = Client("https://ayoubchlin-ayoubchlin-bart-mnli-cnn-news.hf.space/" ,hf_token=config.huggingface_key)
        labels  = ",".join(config.labels)
        print(labels)
        text = text_processing.preprocess_text(text)
        result = client.predict(
                text,
				labels,	# str representing input in 'Possible class names (comma-separated)' Textbox component
				False,	# bool representing input in 'Allow multiple true classes' Checkbox component
				api_name="/predict"
        )
        # Open the file in read mode
        with open(result, 'r') as file:
            # Read the contents of the file
            json_data = json.load(file)
        print(json_data)
        return json_data["label"]
        
    except Exception as e:
        # Handle any other exceptions
        print(f"Exception: {e}")
        return None