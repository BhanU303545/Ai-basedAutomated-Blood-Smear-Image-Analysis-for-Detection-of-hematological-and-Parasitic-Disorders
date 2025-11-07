# Model Setup Guide - vit_bloodsmear_finetuned.pth

This guide explains how to integrate your `vit_bloodsmear_finetuned.pth` PyTorch model with the Node.js backend.

## Current Setup

The server is configured to use the model: **vit_bloodsmear_finetuned.pth**

- Model path: `server/models/vit_bloodsmear_finetuned.pth`
- Python script: `server/predict.py`
- Node.js service: `server/modelService.js`

## Prerequisites

1. **Python 3.7+** with the following packages:
   ```bash
   pip install torch torchvision pillow
   ```

2. **Your trained model file**: `vit_blood_best.pth`

## Setup Steps

### 1. Create Models Directory

```bash
cd server
mkdir models
```

### 2. Place Your Model

Copy your `vit_bloodsmear_finetuned.pth` file to the models directory:
```
server/
  └── models/
      └── vit_bloodsmear_finetuned.pth
```

### 3. Update predict.py (if needed)

Open `server/predict.py` and update the model loading section (lines 31-35) to match your model architecture:

```python
def load_model():
    """Load the PyTorch model"""
    try:
        # Define your model architecture
        # Example for Vision Transformer:
        from torchvision.models import vit_b_16
        model = vit_b_16(num_classes=10)  # Adjust num_classes
        
        # Load the trained weights
        model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
        model.eval()
        return model
    except Exception as e:
        print(json.dumps({'error': f'Failed to load model: {str(e)}'}))
        sys.exit(1)
```

### 4. Verify Class Names

Make sure the CLASS_NAMES in `predict.py` (lines 13-24) match your model's output classes:

```python
CLASS_NAMES = [
    'babesia',
    'basophil',
    'eosinophil',
    'leishmania',
    'lymphocyte',
    'malaria_parasitized',
    'malaria_uninfected',
    'monocyte',
    'neutrophil',
    'trypanosome'
]
```

### 5. Test Python Script

Test the prediction script directly:

```bash
cd server
python predict.py "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
```

You should see JSON output with predictions.

### 6. Restart Server

The Node.js server will automatically use the model if it's available:

```bash
npm start
```

## How It Works

1. **Frontend** sends base64 image to `/api/analyze`
2. **Node.js server** receives the request
3. **modelService.js** spawns a Python process
4. **predict.py** loads the model and makes predictions
5. **Results** are returned as JSON to the frontend

## Fallback Behavior

If the model is not available or Python fails:
- The server automatically uses **mock predictions**
- This allows development/testing without the model
- Check server logs for model loading status

## Troubleshooting

### Model Not Loading

Check server console for:
```
Loading model: vit_blood_best.pth
Model path: /path/to/server/models/vit_blood_best.pth
```

### Python Not Found

Make sure Python is in your system PATH:
```bash
python --version
```

### CUDA/GPU Issues

The script automatically falls back to CPU if CUDA is not available.

### Model Architecture Mismatch

If you get a "state_dict" error, ensure your model architecture in `predict.py` matches the saved model.

## Alternative: ONNX Format

For better performance, you can convert your PyTorch model to ONNX:

```python
# Convert to ONNX
import torch
model = torch.load('vit_blood_best.pth')
dummy_input = torch.randn(1, 3, 224, 224)
torch.onnx.export(model, dummy_input, "vit_blood_best.onnx")
```

Then use `onnxruntime-node` in Node.js directly (no Python needed).

## Performance Tips

1. **Use GPU** if available (CUDA)
2. **Batch predictions** for multiple images
3. **Cache model** in memory (already implemented)
4. **Consider ONNX** for production deployment

## Support

For issues with:
- **Model loading**: Check `predict.py` model architecture
- **Predictions**: Verify class names and preprocessing
- **Integration**: Check `modelService.js` Python spawn
