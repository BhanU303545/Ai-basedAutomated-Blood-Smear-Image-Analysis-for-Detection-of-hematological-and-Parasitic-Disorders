# Troubleshooting: Analysis Error

## Error Message
```
Analysis failed: Cannot read properties of undefined (reading 'predicted_class')
```

## What This Means

The frontend is trying to access `result.predicted_class`, but the backend is returning an error response instead of a successful prediction.

## Fixes Applied

### 1. **Frontend Error Handling** (`js/analyze.js`)
Added better error checking to show the actual error message from the backend:

```javascript
if (response.ok && data.result) {
    // Check if result has the expected structure
    if (data.result.status === 'error') {
        throw new Error(data.result.error || 'Analysis failed');
    }
    if (!data.result.predicted_class) {
        throw new Error('Invalid response from server: missing predicted_class');
    }
    showResults(data.result);
}
```

### 2. **Backend Debug Logging** (`backend/app.py`)
Added detailed logging in the `predict()` method to track exactly where the error occurs:

```python
print("Starting prediction...")
print("Decoding image...")
print(f"Image size: {image.size}")
print("Preprocessing image...")
print(f"Input tensor shape: {inputs.shape}")
print("Running model inference...")
print(f"Model output shape: {outputs.shape}")
print("Processing results...")
print(f"Predicted: {predicted_class} with confidence {confidence_score}")
print("Prediction successful!")
```

## How to Debug

### Step 1: Restart Flask Server
```bash
cd backend
python app.py
```

### Step 2: Try Uploading an Image
1. Go to the analyze page
2. Upload a blood smear image
3. Click "Analyze Image"

### Step 3: Check Flask Server Output
The server will now print detailed information:

**If successful, you'll see:**
```
Starting prediction...
Decoding image...
Image size: (640, 480)
Preprocessing image...
Input tensor shape: torch.Size([1, 3, 224, 224])
Running model inference...
Model output shape: torch.Size([1, 10])
Processing results...
Predicted: Neutrophil with confidence 0.85
Prediction successful!
```

**If there's an error, you'll see:**
```
Starting prediction...
Decoding image...
ERROR in predict: <error message>
<full stack trace>
```

## Common Issues & Solutions

### Issue 1: Model File Not Found
**Error**: `FileNotFoundError: vit_bloodsmear_finetuned.pth`

**Solution**: Place your model file in the `backend/` directory:
```
backend/
├── app.py
└── vit_bloodsmear_finetuned.pth  ← Place model here
```

### Issue 2: Model Architecture Mismatch
**Error**: `RuntimeError: Error(s) in loading state_dict`

**Solution**: The model architecture in `app.py` must match the architecture used during training. Check:
- Number of layers (depth=12)
- Number of heads (heads=12)
- Embedding dimension (dim=768)
- Number of classes (num_classes=10)

### Issue 3: CUDA Out of Memory
**Error**: `RuntimeError: CUDA out of memory`

**Solution**: The model will automatically fall back to CPU if CUDA is not available. If you're getting this error, modify line 128:
```python
self.device = torch.device('cpu')  # Force CPU
```

### Issue 4: Invalid Image Data
**Error**: `Cannot identify image file`

**Solution**: Ensure the image is:
- Valid JPG or PNG format
- Less than 10MB
- Not corrupted

### Issue 5: Missing Dependencies
**Error**: `ModuleNotFoundError: No module named 'torch'`

**Solution**: Install required packages:
```bash
pip install torch torchvision transformers flask flask-cors pymongo pillow
```

## Expected Backend Response

### Success Response:
```json
{
  "analysis_id": "uuid-here",
  "result": {
    "predicted_class": "Neutrophil",
    "confidence": 0.85,
    "all_predictions": [
      {"disease": "Neutrophil", "confidence": 0.85},
      {"disease": "Lymphocyte", "confidence": 0.08},
      {"disease": "Monocyte", "confidence": 0.04},
      ...
    ],
    "status": "success"
  }
}
```

### Error Response:
```json
{
  "error": "Error message here",
  "status": "error"
}
```

## Testing the Backend Directly

You can test the backend API directly using curl:

```bash
# Health check
curl http://localhost:5001/api/health

# Test analysis (with base64 image)
curl -X POST http://localhost:5001/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "image": "base64-encoded-image-data",
    "user_id": "test-user-id",
    "notes": "Test analysis"
  }'
```

## Next Steps

1. **Restart the Flask server** with the updated code
2. **Try uploading an image** 
3. **Check the server console** for detailed debug output
4. **Share the error message** if you still see issues

The detailed logging will help identify exactly where the problem is occurring!

---

**Status**: Debugging tools added ✅
**Next**: Restart server and check console output
