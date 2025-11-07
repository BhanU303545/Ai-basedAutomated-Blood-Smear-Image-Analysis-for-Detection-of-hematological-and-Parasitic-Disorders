import torch
import torchvision.transforms as transforms
from PIL import Image
import io
import base64
import requests

def test_real_model():
    print("Testing if model is making real predictions...")
    
    try:
        # Create different test images
        test_images = [
            Image.new('RGB', (224, 224), color='red'),
            Image.new('RGB', (224, 224), color='blue'), 
            Image.new('RGB', (224, 224), color='green')
        ]
        
        for i, img in enumerate(test_images):
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            response = requests.post(
                'http://localhost:5001/api/analyze',
                json={
                    'image': f"data:image/jpeg;base64,{img_str}",
                    'user_id': 'test-user',
                    'notes': f'Test image {i+1}'
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"Test {i+1}: {result['result']['predicted_class']} ({result['result']['confidence']:.2%})")
            else:
                print(f"Test {i+1}: Error - {response.text}")
                
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == '__main__':
    test_real_model()