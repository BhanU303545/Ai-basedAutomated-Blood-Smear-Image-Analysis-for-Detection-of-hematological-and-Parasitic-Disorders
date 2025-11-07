# Deployment Notes

## Important Setup Steps

### 1. Configure Environment Variables

You **must** create a `.env` file with your MongoDB credentials:

```env
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB_NAME=blood_smear_analysis
```

For production deployment, update the MongoDB URI to your production MongoDB instance.

### 2. Database Configuration

MongoDB will automatically create the following collections:
- **users** collection for user accounts and authentication
- **analyses** collection for analysis records
- **results** collection for disease predictions

See `MONGODB_CONNECTION_SETUP.md` for detailed setup instructions.

### 3. Backend Services

The application uses two backend services:

**Python Flask Backend (Port 5001)**:
- Handles ML inference using PyTorch
- Loads the `best_model.pth` (EfficientNet-B0) model
- Processes blood smear images
- Returns disease predictions with confidence scores

**Node.js Express Server (Port 5001)**:
- Handles user authentication
- Manages database operations
- Provides API endpoints for frontend

### 4. Model Integration

The Python backend uses the trained PyTorch model:
- Model file: `backend/models/best_model.pth`
- Architecture: EfficientNet-B0 with custom classifier
- Input: 224x224 RGB images
- Output: Disease predictions with confidence scores

### 5. Authentication

- Password hashing with bcrypt
- Session-based authentication using localStorage
- No email confirmation required (immediate login after registration)
- Users are automatically redirected to dashboard after login

### 7. Browser Compatibility

- Modern browsers required for camera access (Live Microscopy feature)
- HTTPS required in production for camera API access

## Testing the Application

1. Register a new account
2. Upload a blood smear image in "Image Analysis"
3. Try the live camera feature in "Live Microscopy"
4. View results in "Results History"
5. Download reports from any result
6. Check analytics in the Dashboard

## Known Limitations

- Camera feature requires HTTPS in production
- Large images may take longer to process
- Report downloads are in text format (can be enhanced to PDF)
- Both backend services currently use port 5001 (need to configure different ports for production)
