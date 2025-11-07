# Model File Hosting Guide for Deployment

Your model file (`best_model.pth`, ~56MB) is too large for GitHub's free LFS tier. Here are solutions to host it externally:

## Option 1: Google Drive (Recommended - Free & Easy)

### Step 1: Upload Model to Google Drive
1. Go to [Google Drive](https://drive.google.com)
2. Upload `backend/models/best_model.pth`
3. Right-click the file → "Get link"
4. Set permissions to "Anyone with the link can view"
5. Copy the link (looks like): `https://drive.google.com/file/d/FILE_ID/view?usp=sharing`

### Step 2: Convert to Direct Download Link
Replace the Google Drive link format:
```
FROM: https://drive.google.com/file/d/FILE_ID/view?usp=sharing
TO:   https://drive.google.com/uc?export=download&id=FILE_ID
```

Example:
```
Original: https://drive.google.com/file/d/1ABC123xyz/view?usp=sharing
Direct:   https://drive.google.com/uc?export=download&id=1ABC123xyz
```

### Step 3: Add to Render Environment Variables
In your Render dashboard, add:
```
MODEL_URL=https://drive.google.com/uc?export=download&id=YOUR_FILE_ID
```

## Option 2: Dropbox

### Step 1: Upload to Dropbox
1. Upload `best_model.pth` to Dropbox
2. Click "Share" → "Create a link"
3. Copy the link

### Step 2: Convert to Direct Download
Replace `www.dropbox.com` with `dl.dropboxusercontent.com` and remove `?dl=0`:
```
FROM: https://www.dropbox.com/s/abc123/best_model.pth?dl=0
TO:   https://dl.dropboxusercontent.com/s/abc123/best_model.pth
```

### Step 3: Add to Render
```
MODEL_URL=https://dl.dropboxusercontent.com/s/YOUR_FILE_ID/best_model.pth
```

## Option 3: Hugging Face Hub (Best for ML Models)

### Step 1: Create Hugging Face Account
1. Go to [Hugging Face](https://huggingface.co)
2. Create a free account

### Step 2: Create a Model Repository
```bash
# Install huggingface_hub
pip install huggingface_hub

# Login
huggingface-cli login

# Upload model
huggingface-cli upload BhanU303545/bloodsmear-model backend/models/best_model.pth
```

### Step 3: Get Direct Download URL
```
https://huggingface.co/BhanU303545/bloodsmear-model/resolve/main/best_model.pth
```

### Step 4: Add to Render
```
MODEL_URL=https://huggingface.co/BhanU303545/bloodsmear-model/resolve/main/best_model.pth
```

## Option 4: GitHub Releases (Alternative)

### Step 1: Create a Release
1. Go to your GitHub repository
2. Click "Releases" → "Create a new release"
3. Tag version: `v1.0`
4. Upload `best_model.pth` as a release asset
5. Publish release

### Step 2: Get Direct Download URL
```
https://github.com/BhanU303545/YOUR_REPO_NAME/releases/download/v1.0/best_model.pth
```

### Step 3: Add to Render
```
MODEL_URL=https://github.com/BhanU303545/YOUR_REPO_NAME/releases/download/v1.0/best_model.pth
```

## Complete Render Environment Variables

After hosting your model, add these to Render:

```bash
# MongoDB Configuration
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/bloodsmear?retryWrites=true&w=majority
DB_NAME=bloodsmear

# Model Configuration
MODEL_PATH=backend/models/best_model.pth
MODEL_URL=YOUR_DIRECT_DOWNLOAD_URL_HERE

# Server Configuration
PORT=10000
PYTHON_VERSION=3.11.0
```

## Testing Locally

Before deploying, test the download functionality:

```bash
# Set environment variable
export MODEL_URL="your_direct_download_url"

# Remove local model to test download
rm backend/models/best_model.pth

# Run the app
python app.py
```

The app should automatically download the model on startup.

## Troubleshooting

### Issue: Model download fails
**Solution**: Verify the URL is a direct download link (not a preview page)

### Issue: Download is slow
**Solution**: 
- Use a CDN-backed service (Hugging Face recommended)
- Consider upgrading to Render's paid tier for better bandwidth

### Issue: Model not found after download
**Solution**: Check the `MODEL_PATH` environment variable matches the download destination

## Recommended Solution

For production deployment, I recommend **Hugging Face Hub** because:
- ✅ Free and unlimited bandwidth
- ✅ Designed for ML models
- ✅ Fast CDN delivery
- ✅ Version control for models
- ✅ No file size limits

For quick testing, use **Google Drive** as it's the easiest to set up.
