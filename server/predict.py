import sys
import json
import torch
import base64
from io import BytesIO
from PIL import Image
import torchvision.transforms as transforms
from torchvision import models

# Model configuration
MODEL_PATH = '../backend/models/best_model.pth'
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Class names will be loaded from checkpoint
CLASS_NAMES = []

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def load_model():
    """Load the EfficientNet-B0 PyTorch model"""
    global CLASS_NAMES
    try:
        # Load checkpoint
        checkpoint = torch.load(MODEL_PATH, map_location=DEVICE)
        CLASS_NAMES = checkpoint['class_names']
        
        # Create EfficientNet-B0 model
        model = models.efficientnet_b0()
        num_ftrs = model.classifier[1].in_features
        model.classifier[1] = torch.nn.Linear(num_ftrs, len(CLASS_NAMES))
        
        # Load trained weights
        model.load_state_dict(checkpoint['model_state_dict'])
        model = model.to(DEVICE)
        model.eval()
        
        return model
    except Exception as e:
        print(json.dumps({'error': f'Failed to load model: {str(e)}'}))
        sys.exit(1)

def preprocess_image(base64_image):
    """Convert base64 image to tensor"""
    try:
        # Remove data URL prefix if present
        if ',' in base64_image:
            base64_image = base64_image.split(',')[1]
        
        # Decode base64 to image
        image_data = base64.b64decode(base64_image)
        image = Image.open(BytesIO(image_data)).convert('RGB')
        
        # Apply transformations
        image_tensor = transform(image).unsqueeze(0)
        return image_tensor.to(DEVICE)
    except Exception as e:
        print(json.dumps({'error': f'Failed to preprocess image: {str(e)}'}))
        sys.exit(1)

def predict(model, image_tensor):
    """Make prediction"""
    try:
        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            
        # Get all predictions
        probs = probabilities[0].cpu().numpy()
        predictions = []
        
        for idx, prob in enumerate(probs):
            predictions.append({
                'disease': CLASS_NAMES[idx],
                'confidence': float(prob * 100)
            })
        
        # Sort by confidence
        predictions.sort(key=lambda x: x['confidence'], reverse=True)
        
        return predictions
    except Exception as e:
        print(json.dumps({'error': f'Prediction failed: {str(e)}'}))
        sys.exit(1)

def main():
    """Main function"""
    try:
        # Read base64 image from command line argument
        if len(sys.argv) < 2:
            print(json.dumps({'error': 'No image data provided'}))
            sys.exit(1)
        
        base64_image = sys.argv[1]
        
        # Load model
        model = load_model()
        
        # Preprocess image
        image_tensor = preprocess_image(base64_image)
        
        # Make prediction
        predictions = predict(model, image_tensor)
        
        # Output results as JSON
        result = {
            'predicted_disease': predictions[0]['disease'],
            'confidence': predictions[0]['confidence'],
            'all_predictions': predictions
        }
        
        print(json.dumps(result))
        
    except Exception as e:
        print(json.dumps({'error': str(e)}))
        sys.exit(1)

if __name__ == '__main__':
    main()
