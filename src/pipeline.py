from .document import PDF_Processing 
from .ocr_model import OCR
from .llms import LLM
import os

class Pipeline:
    def __init__(self):
        self.cwd = os.getcwd()

    def process(self, file, file_type):  # Ensure 'self' is included
        try:
            print("started")
            if file_type.lower() == "pdf":
                image = PDF_Processing.pdf_to_image(file)
            else:
                image = PDF_Processing.load_image(file)
                
            # Extract text and process
            text = OCR.extract_text(image)
            json_text = LLM().get_json(input_data=text, key="json")
            final = LLM().get_json(input_data=json_text)
            return final
        except Exception as e:
            print(e)
            return f"An error occurred: {e}"
