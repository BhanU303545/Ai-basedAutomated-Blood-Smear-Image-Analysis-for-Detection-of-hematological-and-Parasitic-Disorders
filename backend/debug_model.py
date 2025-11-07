import torch
import torch.nn as nn

print("=== Model Debug Information ===")

try:
    model_data = torch.load('vit_blood_best.pth', map_location='cpu')
    print(" Model loaded successfully")
    print(f"Model type: {type(model_data)}")
    
    if isinstance(model_data, dict):
        print(f"Number of keys: {len(model_data)}")
        print("\nFirst 10 keys:")
        for i, key in enumerate(list(model_data.keys())[:10]):
            if hasattr(model_data[key], 'shape'):
                print(f"  {i+1}. {key}: {model_data[key].shape}")
            else:
                print(f"  {i+1}. {key}: {type(model_data[key])}")
        
        print("\nLast 10 keys:")
        for i, key in enumerate(list(model_data.keys())[-10:]):
            if hasattr(model_data[key], 'shape'):
                print(f"  {i+1}. {key}: {model_data[key].shape}")
            else:
                print(f"  {i+1}. {key}: {type(model_data[key])}")
                
    else:
        print("Model is not a state_dict")
        print(f"Model structure: {model_data}")
        
except Exception as e:
    print(f" Error loading model: {e}")