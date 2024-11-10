import os
import torch
from .document import PDF_Processing
from .ocr_model import OCR
from .llms import LLM

class Pipeline:
    def __init__(self):
        self.cwd = os.getcwd()
        self.model_path = os.path.join(self.cwd, "models", "detection_model.pt")
    
    def load_model(self):
        # Create the models directory if it doesn't exist
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)

        # Check if the model file exists
        if not os.path.exists(self.model_path):
            print("Downloading detection model, please wait. This may take several minutes depending upon your network connection.")
            # Example: torch.hub.download_url_to_file(url, self.model_path)
            # For now, this is a placeholder for downloading the model
            # torch.save(torch_model, self.model_path)  # Save model here
        else:
            print("Model already downloaded.")

        # Load the model
        self.model = torch.load(self.model_path, map_location="cpu")
        self.model.eval()

    def process(self, file, file_type):
        self.load_model()  # Ensure the model is loaded before processing
        try:
            print("Started processing...")
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

