# Blood Smear Analysis - Complete Setup Guide

## Overview

Your application now uses **MongoDB** database and the **vit_bloodsmear_finetuned.pth** Vision Transformer model for blood cell and parasite classification.

## System Architecture

```
Frontend (HTML/JS) → Flask Backend (Python) → MongoDB Database
                            ↓
                    vit_bloodsmear_finetuned.pth Model
```

## Quick Start

### 1. MongoDB Setup ✅
- Already configured and running on `mongodb://localhost:27017/`
- Database: `blood_smear_analysis`

### 2. Place Your Model File

Copy your trained model to the backend directory:
```
project/
  └── backend/
      └── vit_bloodsmear_finetuned.pth  ← Place your model here
```

### 3. Install Python Dependencies

```bash
cd backend
pip install torch torchvision transformers flask flask-cors pymongo pillow
```

### 4. Start the Backend Server

```bash
cd backend
python app.py
```

You should see:
```
* Running on http://0.0.0.0:5001
```

### 5. Start the Frontend

Open `index.html` in your browser or use a local server.

## What Changed

### ✅ Database Migration
- **From**: Supabase
- **To**: MongoDB (localhost:27017)
- All authentication and data storage now uses MongoDB

### ✅ Model Configuration
- **Model Name**: `vit_bloodsmear_finetuned.pth` (updated from `vit_best_model.pth`)
- **Architecture**: Vision Transformer (ViT-base-patch16-224)
- **Classes**: 10 types (Babesia, Leishmania, Trypanosome, Basophil, Eosinophil, Lymphocyte, Malaria Parasitized, Malaria Uninfected, Monocyte, Neutrophil)

### ✅ Updated Files

**Frontend**:
- `js/api.js` - API endpoints
- `js/auth.js` - Authentication (no Supabase)
- `js/analyze.js` - Image analysis
- `js/dashboard.js` - Dashboard data
- `js/results.js` - Results display
- `js/live.js` - Live capture
- `js/mongodb.js` - MongoDB helpers

**Backend**:
- `backend/app.py` - Flask server with model integration

## API Endpoints

All endpoints run on `http://localhost:5001/api/`

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login user

### Analysis
- `POST /api/analyze` - Analyze blood smear image
- `GET /api/results?user_id={id}` - Get user results
- `GET /api/stats/{userId}` - Get user statistics

## Disease/Cell Types Detected

1. **Babesia** - Parasitic infection
2. **Leishmania** - Parasitic infection
3. **Trypanosome** - Parasitic infection
4. **Basophil** - White blood cell
5. **Eosinophil** - White blood cell
6. **Lymphocyte** - White blood cell
7. **Malaria (Parasitized)** - Infected red blood cell
8. **Malaria (Uninfected)** - Normal red blood cell
9. **Monocyte** - White blood cell
10. **Neutrophil** - White blood cell

## Troubleshooting

### Backend Won't Start

**Error**: `FileNotFoundError: 'vit_bloodsmear_finetuned.pth'`
- **Solution**: Place your model file in the `backend/` directory

**Error**: `MongoDB connection failed`
- **Solution**: Start MongoDB service
- Check: `mongosh` to verify MongoDB is running

**Error**: `Port 5001 already in use`
- **Solution**: Kill the process or change port in `app.py`

### Frontend Issues

**Error**: `Failed to load results`
- **Solution**: Ensure backend is running on port 5001
- Check browser console for errors

**Error**: `Login failed`
- **Solution**: Check MongoDB connection
- Verify backend is running

### Model Issues

**Error**: Model loading fails
- **Solution**: Verify model file exists and is not corrupted
- Check PyTorch version compatibility

**Low accuracy**
- **Solution**: Ensure you're using the correct trained model
- Verify image preprocessing matches training

## File Structure

```
project/
├── backend/
│   ├── app.py                    # Flask server (UPDATED)
│   ├── vit_bloodsmear_finetuned.pth  # Your model file (PLACE HERE)
│   └── README.md                 # Backend documentation
├── js/
│   ├── api.js                    # API client (UPDATED)
│   ├── auth.js                   # Authentication (UPDATED)
│   ├── analyze.js                # Analysis logic (UPDATED)
│   ├── dashboard.js              # Dashboard (UPDATED)
│   ├── results.js                # Results display (UPDATED)
│   ├── live.js                   # Live capture (UPDATED)
│   └── mongodb.js                # MongoDB helpers (NEW)
├── server/                       # Node.js alternative (optional)
│   ├── server.js
│   ├── predict.py
│   └── modelService.js
├── index.html                    # Login page
├── dashboard.html                # Dashboard
├── analyze.html                  # Analysis page
├── results.html                  # Results page
└── live.html                     # Live capture page
```

## Testing the Application

### 1. Register a User
- Open `index.html`
- Click "Register" tab
- Fill in details and submit

### 2. Login
- Use your registered credentials
- Should redirect to dashboard

### 3. Analyze an Image
- Go to "Image Analysis"
- Upload a blood smear image
- Click "Analyze"
- View results

### 4. Check Results
- Go to "Results History"
- View all past analyses
- Filter by disease type

## Performance

- **CPU**: ~2-5 seconds per image
- **GPU (CUDA)**: ~0.5-1 second per image
- **Batch processing**: Can be implemented for multiple images

## Next Steps

1. ✅ Place `vit_bloodsmear_finetuned.pth` in `backend/` directory
2. ✅ Start MongoDB (already running)
3. ✅ Install Python dependencies
4. ✅ Start backend: `python app.py`
5. ✅ Open frontend in browser
6. ✅ Test with sample images

## Support

For issues:
1. Check MongoDB is running
2. Verify model file exists
3. Check backend console for errors
4. Check browser console for frontend errors
5. Ensure all dependencies are installed

## Security Notes

⚠️ **For Production**:
- Hash passwords (currently plain text)
- Implement JWT authentication
- Add input validation
- Enable HTTPS
- Restrict CORS origins
- Add rate limiting

---

**Your application is now ready to use with MongoDB and the vit_bloodsmear_finetuned.pth model!** 🚀
