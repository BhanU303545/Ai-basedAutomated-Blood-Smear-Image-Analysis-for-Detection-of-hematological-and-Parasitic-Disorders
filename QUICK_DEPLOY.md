# Quick Deployment Steps

## Fix Git LFS Issue and Deploy

### Step 1: Remove Model Files from Git

```bash
# Remove model files from Git tracking
git rm --cached backend/models/*.pth
git rm --cached best_model.pth
git rm --cached backend/*.pth

# Update .gitattributes to stop tracking .pth files with LFS
# (Already done in your .gitignore)

# Commit the changes
git add .
git commit -m "Remove model files from Git LFS, use external hosting"
git push origin main
```

### Step 2: Host Your Model File

**Quickest Option - Google Drive:**

1. Upload `backend/models/best_model.pth` to Google Drive
2. Right-click → "Get link" → "Anyone with the link"
3. Copy the link, extract the FILE_ID
4. Create direct download URL:
   ```
   https://drive.google.com/uc?export=download&id=YOUR_FILE_ID
   ```

**See `MODEL_HOSTING_GUIDE.md` for other options (Hugging Face, Dropbox, etc.)**

### Step 3: Update Render Environment Variables

Go to your Render dashboard and add:

```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/bloodsmear
DB_NAME=bloodsmear
MODEL_PATH=backend/models/best_model.pth
MODEL_URL=YOUR_DIRECT_DOWNLOAD_URL
PORT=10000
PYTHON_VERSION=3.11.0
```

### Step 4: Redeploy on Render

1. Go to your Render dashboard
2. Click "Manual Deploy" → "Deploy latest commit"
3. Monitor the logs - you should see:
   ```
   Downloading model from [URL]...
   ✓ Model downloaded successfully
   ✓ Model loaded successfully
   ```

### Step 5: Verify Deployment

Test the health endpoint:
```
curl https://your-app.onrender.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cpu",
  "test_prediction_status": "success"
}
```

## Commands to Run Now

```bash
# Navigate to project directory
cd c:\Users\SIVA\Downloads\bloodsmearimageanalysisproject\project

# Remove model files from Git
git rm --cached backend/models/*.pth
git rm --cached best_model.pth 2>$null
git rm --cached backend/*.pth 2>$null

# Commit changes
git add .
git commit -m "Remove model files from Git, implement external model hosting"

# Push to GitHub
git push origin main
```

## Next Steps

1. ✅ Upload model to Google Drive/Hugging Face
2. ✅ Get direct download URL
3. ✅ Add MODEL_URL to Render environment variables
4. ✅ Trigger manual deploy on Render
5. ✅ Test the deployment

## Troubleshooting

**If deployment still fails:**
- Check Render logs for specific errors
- Verify MODEL_URL is accessible (test in browser)
- Ensure MongoDB Atlas IP whitelist includes 0.0.0.0/0
- Check all environment variables are set correctly

**Model download is slow:**
- First deployment will take longer (downloading 56MB)
- Subsequent deploys will use cached model
- Consider using Hugging Face for faster CDN delivery
