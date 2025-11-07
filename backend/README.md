# Blood Smear Analysis - Flask Backend

This is the Flask-based backend server for the Blood Smear Analysis application using MongoDB and the `models/best_model.pth` EfficientNet model.

## Prerequisites

1. **Python 3.7+**
2. **MongoDB** running with authentication
   - Connection: `mongodb://bhanu:bhanu123@localhost:27017/bloodsmear?authSource=admin`
   - Database: `bloodsmear`
3. **Required Python packages**

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install torch torchvision transformers flask flask-cors pymongo pillow
```

Or if you have a requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. Place Your Model File

Copy your trained model to the backend directory:
```
backend/
  └── models/
      └── best_model.pth
```

### 3. Verify MongoDB is Running

Make sure MongoDB is running on port 27017:
```bash
# Check if MongoDB is running
mongosh
```

### 4. Start the Flask Server

```bash
python app.py
```

The server will start on `http://0.0.0.0:5001`

## Model Information

- **Model File**: `models/best_model.pth`
- **Architecture**: EfficientNet-B0
- **Classes**: 10 blood cell types and parasites
  - Babesia
  - Basophil
  - Eosinophil
  - Leishmania
  - Lymphocyte
  - Malaria (Parasitized)
  - Malaria (Uninfected)
  - Monocyte
  - Neutrophil
  - Trypanosome

## API Endpoints

### Authentication

**POST /api/register**
- Register a new user
- Body: `{ "email": "...", "password": "...", "name": "...", "role": "..." }`

**POST /api/login**
- Login user
- Body: `{ "email": "...", "password": "..." }`

### Analysis

**POST /api/analyze**
- Analyze blood smear image
- Body: `{ "image": "base64_data", "user_id": "...", "notes": "..." }`
- Returns: Prediction results with confidence scores

**GET /api/results?user_id={userId}**
- Get all analysis results for a user
- Returns: Array of analysis results

**GET /api/stats/{userId}**
- Get user statistics
- Returns: Analysis counts and results

## Database Structure

**Database**: `bloodsmear`

**Collections**:

1. **users**
   - user_id (UUID)
   - email
   - password (plain text - should be hashed in production!)
   - name
   - role
   - created_at

2. **analyses**
   - analysis_id (UUID)
   - user_id
   - notes
   - result (prediction object)
   - created_at

## Configuration

You can modify these settings in `app.py`:

```python
MONGO_URI = 'mongodb://bhanu:bhanu123@localhost:27017/bloodsmear?authSource=admin'
DB_NAME = 'bloodsmear'
PORT = 5001
```

## Model Loading

The model is loaded when the server starts:

```python
analyzer = BloodSmearAnalyzer('models/best_model.pth')
```

If the model file is not found, you'll see:
```
FileNotFoundError: [Errno 2] No such file or directory: 'models/best_model.pth'
```

Make sure the model file is in the `backend/models/` directory.

## GPU Support

The model automatically uses CUDA if available:
```python
self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
```

To check if GPU is being used, look for this in the console when starting the server.

## Troubleshooting

### Model Not Found
- Ensure `best_model.pth` is in the `backend/models/` directory
- Check the file name matches exactly (case-sensitive)
- Create the `models/` directory if it doesn't exist

### MongoDB Connection Error
- Verify MongoDB is running: `mongosh`
- Check the connection string in `app.py`

### Port Already in Use
- Change the port in `app.py`: `app.run(port=5002)`
- Or kill the process using port 5001

### CUDA/GPU Issues
- The server will automatically fall back to CPU if CUDA is not available
- For CPU-only: The model will still work but slower

### Import Errors
- Install missing packages: `pip install <package_name>`
- Use Python 3.7 or higher

## Production Considerations

⚠️ **Security Issues to Fix**:

1. **Password Hashing**: Currently passwords are stored in plain text
   - Use `bcrypt` or `werkzeug.security` to hash passwords

2. **Authentication**: No JWT or session management
   - Implement proper authentication tokens

3. **CORS**: Currently allows all origins
   - Restrict CORS to your frontend domain only

4. **Error Handling**: Some errors expose internal details
   - Implement proper error handling and logging

5. **Input Validation**: Limited validation on inputs
   - Add comprehensive input validation

## Performance Tips

1. **Use GPU** for faster inference
2. **Batch Processing** for multiple images
3. **Model Caching** (already implemented)
4. **Database Indexing** on user_id and created_at
5. **Connection Pooling** for MongoDB

## Testing

Test the API using curl:

```bash
# Register
curl -X POST http://localhost:5001/api/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123","name":"Test User","role":"technician"}'

# Login
curl -X POST http://localhost:5001/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'
```
