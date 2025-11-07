# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Place Your Model
```
backend/vit_bloodsmear_finetuned.pth
```

### Step 2: Start Backend
```bash
cd backend
python app.py
```

### Step 3: Open Frontend
Open `index.html` in your browser

---

## ✅ Checklist

- [ ] MongoDB running on port 27017
- [ ] Model file `vit_bloodsmear_finetuned.pth` in `backend/` folder
- [ ] Python dependencies installed
- [ ] Backend running on port 5001
- [ ] Frontend opened in browser

---

## 📦 Install Dependencies

```bash
pip install torch torchvision transformers flask flask-cors pymongo pillow
```

---

## 🔍 Verify Setup

### Check MongoDB
```bash
mongosh
```

### Check Backend
```bash
curl http://localhost:5001/api/health
```

### Check Model File
```bash
ls backend/vit_bloodsmear_finetuned.pth
```

---

## 🎯 Model Information

- **Name**: `vit_bloodsmear_finetuned.pth`
- **Type**: Vision Transformer (ViT)
- **Classes**: 10 blood cell types
- **Input**: 224x224 RGB images

---

## 📝 API Endpoints

- `POST /api/register` - Register user
- `POST /api/login` - Login
- `POST /api/analyze` - Analyze image
- `GET /api/results` - Get results
- `GET /api/stats/{userId}` - Get stats
- `GET /api/health` - Health check

---

## 🐛 Common Issues

**Model not found?**
→ Place `vit_bloodsmear_finetuned.pth` in `backend/` folder

**MongoDB error?**
→ Start MongoDB: `mongod`

**Port 5001 in use?**
→ Kill process or change port in `app.py`

---

## 📚 More Info

- Full setup: `SETUP_GUIDE.md`
- Model update: `MODEL_UPDATE_SUMMARY.md`
- Backend docs: `backend/README.md`
- Server docs: `server/MODEL_SETUP.md`
