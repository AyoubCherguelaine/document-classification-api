import pytesseract
from PIL import Image
import textract
from . import config

def extract_text(filename: str, file_path: str) -> str:
    file_extension = filename.split('.')[-1].lower()
    
    if file_extension in ['pdf', 'docx', 'xlsx', 'doc', 'rtf', 'odt']:
        # Use textract library to extract text from PDF, DOCX, or XLSX files
        text = textract.process(file_path, method='tesseract', encoding='utf-8')
        text = text.decode('utf-8')
        return text
    
    elif file_extension in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff']:
        # Convert other file types (images) to text using Tesseract OCR
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text
    
    return None