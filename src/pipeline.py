from .document import PDF_Processing 
from .ocr_model import OCR
from .llms import LLM
import os

class Pipeline:
    def __init__(self):
        self.cwd = os.getcwd()

    def process(self, file, file_type):  # Added 'self' and renamed 'type' to 'file_type'
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

# Testing code for main
if __name__ == "__main__":
    path = "test_docs/CBC-test-report-format-example-sample-template-Drlogy-lab-report.pdf"
    pipeline = Pipeline()
    result = pipeline.process(path, "pdf")  # Pass the file type as well
    print(result)
