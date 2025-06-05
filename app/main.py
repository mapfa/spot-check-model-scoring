from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import io
from PIL import Image
import torch
import torchvision.transforms as transforms
from typing import Dict, Any
import os
from app.models.mobilenetv3 import MobileNetV3Classifier
import logging

app = FastAPI(title="Model Inference API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model and move to device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = MobileNetV3Classifier(num_classes=2).to(device)

# Load the trained model weights
model_path = os.path.join(os.path.dirname(__file__), 'models', 'best_model.pth')
model.load_state_dict(torch.load(model_path, map_location=device))
model.eval()

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    return {"message": "Model Inference API is running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> Dict[str, Any]:
    try:
        logger.info("Received prediction request")
        # Read and process the image
        contents = await file.read()
        logger.info("Image read successfully")
        image = Image.open(io.BytesIO(contents))
        logger.info("Image opened successfully")
        
        # Preprocess the image
        image_tensor = transform(image).unsqueeze(0).to(device)
        logger.info("Image preprocessed successfully")
        
        # Make prediction
        with torch.no_grad():
            logger.info("Starting model inference")
            prediction = model(image_tensor)
            logger.info("Model inference completed")
            probabilities = torch.softmax(prediction, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_class].item()
            logger.info(f"Prediction completed: class {predicted_class}, confidence {confidence}")
        
        return {
            "predicted_class": int(predicted_class),
            "confidence": float(confidence),
            "status": "success"
        }
    
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}", exc_info=True)
        return {
            "error": str(e),
            "status": "error"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 