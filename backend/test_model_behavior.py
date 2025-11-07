import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import numpy as np

print("Testing model behavior with different inputs...")

# Load checkpoint
checkpoint = torch.load('models/best_model.pth', map_location='cpu')
class_names = checkpoint['class_names']

print(f"Model accuracy: {checkpoint['val_acc']:.2f}%")
print(f"Classes: {class_names}")

# Create EfficientNet model
model = models.efficientnet_b0()
in_features = model.classifier[1].in_features
model.classifier = nn.Sequential(
    nn.Dropout(0.3),
    nn.Linear(in_features, 512),
    nn.ReLU(),
    nn.BatchNorm1d(512),
    nn.Dropout(0.2),
    nn.Linear(512, len(class_names))
)

model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

print("\nTesting with different color images:")
colors = ['red', 'green', 'blue', 'white', 'black']
for color in colors:
    img = Image.new('RGB', (224, 224), color=color)
    img_tensor = transform(img).unsqueeze(0)
    
    with torch.no_grad():
        outputs = model(img_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted_idx = torch.max(probabilities, 1)
    
    predicted_class = class_names[predicted_idx.item()]
    confidence_score = confidence.item()
    
    print(f"{color:6}: {predicted_class:20} ({confidence_score:.2%})")
    
    all_probs = probabilities[0].numpy()
    top_3_indices = np.argsort(all_probs)[-3:][::-1]
    for idx in top_3_indices:
        print(f"         {class_names[idx]:20} {all_probs[idx]:.2%}")

print("\nTesting with actual blood smear images (if available):")
try:
    import os
    blood_images = [f for f in os.listdir('.') if f.endswith(('.jpg', '.jpeg', '.png'))]
    for img_file in blood_images[:3]:
        img = Image.open(img_file).convert('RGB')
        img_tensor = transform(img).unsqueeze(0)
        
        with torch.no_grad():
            outputs = model(img_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted_idx = torch.max(probabilities, 1)
        
        predicted_class = class_names[predicted_idx.item()]
        confidence_score = confidence.item()
        
        print(f"{img_file:20}: {predicted_class:20} ({confidence_score:.2%})")
except:
    print("No blood smear images found for testing")