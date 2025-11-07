import torch
from torchvision import models, transforms
from PIL import Image
import torch.nn as nn
import matplotlib.pyplot as plt

def test_blood_smear_model(image_path):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    checkpoint = torch.load('models/best_model.pth', map_location=device)
    class_names = checkpoint['class_names']
    print(f"Model classes: {class_names}")
    print(f"Model accuracy: {checkpoint['val_acc']:.2f}%")
    
    model = models.efficientnet_b0()
    model.classifier = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(1280, 512),
        nn.ReLU(),
        nn.BatchNorm1d(512),
        nn.Dropout(0.2),
        nn.Linear(512, len(class_names))
    )
    
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    model.eval()
    
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    try:
        image = Image.open(image_path).convert('RGB')
        print(f"Image size: {image.size}")
        
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.imshow(image)
        plt.title("Original Blood Smear Image")
        plt.axis('off')
        
        image_tensor = transform(image).unsqueeze(0).to(device)
        
        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            confidence, predicted = torch.max(probabilities, 0)
            
            top3_probs, top3_indices = torch.topk(probabilities, 3)
            
        prediction = class_names[predicted.item()]
        confidence_percent = confidence.item() * 100
        
        print(f"PREDICTION RESULTS:")
        print(f"Primary Prediction: {prediction} ({confidence_percent:.2f}%)")
        
        print(f"TOP 3 PREDICTIONS:")
        for i, (prob, idx) in enumerate(zip(top3_probs, top3_indices)):
            class_name = class_names[idx.item()]
            conf = prob.item() * 100
            print(f"{i+1}. {class_name:25}: {conf:.2f}%")
        
        plt.subplot(1, 2, 2)
        plt.imshow(image)
        plt.title(f"Prediction: {prediction}\nConfidence: {confidence_percent:.2f}%")
        plt.axis('off')
        
        plt.tight_layout()
        plt.show()
        
        return prediction, confidence_percent
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return None, 0

if __name__ == "__main__":
    image_path = r"C:\Users\SIVA\Downloads\C100P61ThinF_IMG_20150918_145042_cell_166.png"
    print("Testing Blood Smear Classification Model")
    print("=" * 50)
    
    prediction, confidence = test_blood_smear_model(image_path)
    
    if prediction:
        print(f"FINAL RESULT: {prediction} ({confidence:.2f}% confidence)")