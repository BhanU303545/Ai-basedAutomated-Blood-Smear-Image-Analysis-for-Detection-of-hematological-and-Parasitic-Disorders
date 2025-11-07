# Blood Smear Image Analysis - Deployment Guide

This guide will help you deploy your Blood Smear Analysis application to GitHub and Render.

## Prerequisites

- Git installed on your system
- GitHub account
- Render account (free tier available)
- MongoDB Atlas account (for cloud database)

## Part 1: Prepare for GitHub

### 1. Initialize Git Repository (if not already done)

```bash
cd c:\Users\SIVA\Downloads\bloodsmearimageanalysisproject\project
git init
```

### 2. Install Git LFS for Large Model Files

The model files (*.pth) are large and need Git LFS (Large File Storage):

```bash
# Install Git LFS
git lfs install

# Track model files
git lfs track "*.pth"
git lfs track "backend/models/*.pth"
```

### 3. Add Files to Git

```bash
# Add all files
git add .

# Commit
git commit -m "Initial commit - Blood Smear Analysis Project"
```

### 4. Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., `bloodsmear-analysis`)
3. Don't initialize with README (you already have one)

### 5. Push to GitHub

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/bloodsmear-analysis.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Part 2: Set Up MongoDB Atlas (Cloud Database)

Since Render doesn't support local MongoDB, you need a cloud database:

### 1. Create MongoDB Atlas Account

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for free tier
3. Create a new cluster (M0 Free tier)

### 2. Configure Database Access

1. Go to "Database Access" → Add New Database User
2. Create username and password (save these!)
3. Set privileges to "Read and write to any database"

### 3. Configure Network Access

1. Go to "Network Access" → Add IP Address
2. Click "Allow Access from Anywhere" (0.0.0.0/0)
3. Confirm

### 4. Get Connection String

1. Click "Connect" on your cluster
2. Choose "Connect your application"
3. Copy the connection string (looks like):
   ```
   mongodb+srv://username:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
4. Replace `<password>` with your actual password
5. Add database name: 
   ```
   mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/bloodsmear?retryWrites=true&w=majority
   ```

## Part 3: Deploy to Render

### 1. Sign Up for Render

1. Go to https://render.com
2. Sign up (you can use GitHub to sign in)

### 2. Create New Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select the `bloodsmear-analysis` repository

### 3. Configure Web Service

Fill in the following settings:

- **Name**: `bloodsmear-analyzer` (or your preferred name)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: Leave empty (or specify if your app is in a subdirectory)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

### 4. Add Environment Variables

Click "Advanced" → "Add Environment Variable" and add:

| Key | Value |
|-----|-------|
| `MONGO_URI` | Your MongoDB Atlas connection string |
| `DB_NAME` | `bloodsmear` |
| `PORT` | `10000` |
| `PYTHON_VERSION` | `3.11.0` |

### 5. Deploy

1. Click "Create Web Service"
2. Render will start building and deploying
3. Wait for deployment to complete (5-10 minutes)

### 6. Handle Model Files

**Important**: Model files are too large for GitHub free tier. You have two options:

#### Option A: Use Git LFS (Recommended)
- GitHub LFS allows 1GB free storage
- Already configured in `.gitattributes`
- Your model file should be tracked automatically

#### Option B: Download Model Separately
If Git LFS doesn't work, you'll need to:

1. Upload model to cloud storage (Google Drive, Dropbox, etc.)
2. Add download script in `app.py`:

```python
import os
import urllib.request

def download_model():
    model_path = 'backend/models/best_model.pth'
    if not os.path.exists(model_path):
        print("Downloading model...")
        os.makedirs('backend/models', exist_ok=True)
        # Replace with your model URL
        url = 'YOUR_MODEL_DOWNLOAD_URL'
        urllib.request.urlretrieve(url, model_path)
        print("Model downloaded!")

# Call before initializing analyzer
download_model()
analyzer = BloodSmearAnalyzer('backend/models/best_model.pth')
```

## Part 4: Update Frontend

Update your frontend JavaScript files to use the Render URL:

```javascript
// In js/api.js or wherever you make API calls
const API_BASE_URL = 'https://bloodsmear-analyzer.onrender.com';
```

## Part 5: Test Deployment

1. Visit your Render URL: `https://bloodsmear-analyzer.onrender.com/api/health`
2. You should see a health check response
3. Test the frontend by deploying it to:
   - GitHub Pages
   - Netlify
   - Vercel

## Troubleshooting

### Build Fails

**Issue**: PyTorch installation timeout
**Solution**: Add to `requirements.txt`:
```
--index-url https://download.pytorch.org/whl/cpu
torch==2.0.1+cpu
torchvision==0.15.2+cpu
```

### Model Not Loading

**Issue**: Model file not found
**Solution**: 
1. Check if Git LFS pushed the file
2. Use Option B (download model separately)

### MongoDB Connection Error

**Issue**: Can't connect to MongoDB
**Solution**:
1. Verify connection string in Render environment variables
2. Check MongoDB Atlas network access (allow 0.0.0.0/0)
3. Ensure username/password are correct

### Cold Start Issues

**Issue**: First request is slow
**Solution**: Render free tier spins down after inactivity. Consider:
1. Using a paid plan
2. Setting up a cron job to ping your service every 10 minutes

## Monitoring

1. **Render Dashboard**: Check logs and metrics
2. **MongoDB Atlas**: Monitor database usage
3. **Health Check**: `GET /api/health` endpoint

## Updating Your Deployment

```bash
# Make changes to your code
git add .
git commit -m "Description of changes"
git push origin main

# Render will automatically redeploy
```

## Cost Considerations

- **Render Free Tier**: 750 hours/month, spins down after 15 min inactivity
- **MongoDB Atlas Free**: 512MB storage
- **Git LFS**: 1GB storage, 1GB bandwidth/month

## Security Recommendations

1. Never commit `.env` file (already in `.gitignore`)
2. Use environment variables for all secrets
3. Enable HTTPS (Render provides this automatically)
4. Implement rate limiting for API endpoints
5. Add authentication tokens for production

## Next Steps

1. Set up custom domain (optional)
2. Add monitoring and alerting
3. Implement CI/CD pipeline
4. Add automated tests
5. Set up staging environment

## Support

If you encounter issues:
1. Check Render logs: Dashboard → Logs
2. Check MongoDB Atlas logs
3. Review this guide's troubleshooting section
4. Contact support on respective platforms

---

**Deployment Checklist:**
- [ ] Git repository initialized
- [ ] Git LFS installed and configured
- [ ] Code pushed to GitHub
- [ ] MongoDB Atlas cluster created
- [ ] MongoDB connection string obtained
- [ ] Render account created
- [ ] Web service configured on Render
- [ ] Environment variables added
- [ ] Deployment successful
- [ ] Health check endpoint working
- [ ] Frontend updated with Render URL
- [ ] Full end-to-end test completed
