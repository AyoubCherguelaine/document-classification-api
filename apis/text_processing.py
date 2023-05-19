def preprocess_text(text):
    # Remove newline characters
    text = text.replace('\n', ' ')
    
    # Remove HTML tags and attributes
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove consecutive spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Remove non-alphanumeric characters except for certain special characters
    text = re.sub(r'[^\w\s$€%.,-]|(?<=\d)[.,](?=\d)|(?<=\d)[/](?=\d)', ' ', text).lower()
    
    # Remove leading and trailing whitespace
    text = text.strip()
    
    if len(text.split(' ')) < 4:
        return None
    else:
        return text