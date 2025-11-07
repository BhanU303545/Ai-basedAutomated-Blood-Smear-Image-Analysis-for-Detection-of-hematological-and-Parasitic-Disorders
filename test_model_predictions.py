"""
Test script to verify model predictions
"""
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import io
import base64

print("=" * 60)
print("TESTING MODEL PREDICTIONS")
print("=" * 60)

# Load model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"\n1. Device: {device}")

# Load checkpoint
checkpoint = torch.load('models/best_model.pth', map_location=device)
class_names = checkpoint['class_names']

print(f"\n2. Loading model weights...")
print(f"   Model accuracy: {checkpoint['val_acc']:.2f}%")

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
model.to(device)
model.eval()
print("   ✅ Model loaded successfully")

# Define transforms
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

print(f"\n3. Testing with different colored images:")
print("-" * 60)

# Test with different colored images
colors = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'purple': (128, 0, 128),
    'pink': (255, 192, 203)
}

for color_name, color_rgb in colors.items():
    # Create test image
    img = Image.new('RGB', (224, 224), color=color_rgb)
    
    # Transform and predict
    img_tensor = transform(img).unsqueeze(0).to(device)
    
    with torch.no_grad():
        outputs = model(img_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted_idx = torch.max(probabilities, 1)
    
    predicted_class = class_names[predicted_idx.item()]
    confidence_score = confidence.item()
    
    print(f"   {color_name:8} → {predicted_class:25} ({confidence_score*100:5.1f}%)")

print("\n" + "=" * 60)
print("4. Testing with actual blood smear images (if available):")
print("-" * 60)

import os
import glob

# Look for image files
image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
image_files = []
for ext in image_extensions:
    image_files.extend(glob.glob(ext))

if image_files:
    print(f"   Found {len(image_files)} image(s)")
    
    for img_file in image_files[:5]:  # Test first 5 images
        try:
            img = Image.open(img_file).convert('RGB')
            img_tensor = transform(img).unsqueeze(0).to(device)
            
            with torch.no_grad():
                outputs = model(img_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                confidence, predicted_idx = torch.max(probabilities, 1)
            
            predicted_class = class_names[predicted_idx.item()]
            confidence_score = confidence.item()
            
            # Get top 3 predictions
            top3_probs, top3_indices = torch.topk(probabilities[0], 3)
            
            print(f"\n   📷 {img_file}")
            print(f"      Primary: {predicted_class:20} ({confidence_score*100:5.1f}%)")
            print(f"      Top 3:")
            for i, (prob, idx) in enumerate(zip(top3_probs, top3_indices)):
                print(f"         {i+1}. {class_names[idx.item()]:20} ({prob.item()*100:5.1f}%)")
                
        except Exception as e:
            print(f"   ❌ Error processing {img_file}: {e}")
else:
    print("   ℹ️  No blood smear images found in current directory")
    print("   💡 To test with actual images, place some .jpg or .png files here")

print("\n" + "=" * 60)
print("5. Model Statistics:")
print("-" * 60)

# Count parameters
total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

print(f"   Total parameters:     {total_params:,}")
print(f"   Trainable parameters: {trainable_params:,}")
print(f"   Model size:           ~{total_params * 4 / (1024**2):.1f} MB")

print("\n" + "=" * 60)
print("6. Testing prediction consistency:")
print("-" * 60)

# Test same image multiple times
test_img = Image.new('RGB', (224, 224), color='red')
predictions = []

for i in range(5):
    img_tensor = transform(test_img).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(img_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted_idx = torch.max(probabilities, 1)
    predictions.append((class_names[predicted_idx.item()], confidence.item()))

# Check if all predictions are the same
if len(set(p[0] for p in predictions)) == 1:
    print(f"   ✅ Model is consistent: All 5 predictions → {predictions[0][0]}")
else:
    print(f"   ⚠️  Model predictions vary:")
    for i, (pred, conf) in enumerate(predictions):
        print(f"      Run {i+1}: {pred} ({conf*100:.1f}%)")

print("\n" + "=" * 60)
print("TESTING COMPLETE")
print("=" * 60)

# Summary
print("\n📊 SUMMARY:")
print(f"   • Model loaded: ✅")
print(f"   • Device: {device}")
print(f"   • Classes: {len(class_names)}")
print(f"   • Model is {'consistent' if len(set(p[0] for p in predictions)) == 1 else 'inconsistent'}")
print(f"   • Ready for predictions: ✅")
print("\n")
