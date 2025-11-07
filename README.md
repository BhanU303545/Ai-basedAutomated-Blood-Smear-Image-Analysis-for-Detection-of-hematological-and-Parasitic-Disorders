# Blood Smear Analysis - MongoDB Backend Server

This is the backend server for the Blood Smear Analysis application using MongoDB.

## Prerequisites

1. **MongoDB** - Install MongoDB Community Edition
   - Download from: https://www.mongodb.com/try/download/community
   - Authenticated connection: `mongodb://bhanu:bhanu123@localhost:27017/bloodsmear?authSource=admin`
   - Database: `bloodsmear`

2. **Node.js** - Install Node.js (v14 or higher)
   - Download from: https://nodejs.org/

## Setup Instructions

### 1. Install MongoDB

Connect to MongoDB using MongoDB Compass with:
```
mongodb://bhanu:bhanu123@localhost:27017/bloodsmear?authSource=admin
```

Make sure MongoDB is running on your system with authentication enabled.

### 2. Install Dependencies

Navigate to the server directory and install dependencies:

```bash
cd server
npm install
```

### 3. Start the Server

```bash
npm start
```

Or for development with auto-reload:

```bash
npm run dev
```

The server will start on `http://localhost:5001`

### 4. Database Structure

The application uses the following collections:

- **users** - User accounts
  - email
  - password (hashed)
  - full_name
  - role
  - created_at

- **analyses** - Analysis records
  - user_id
  - image_data (base64)
  - analysis_type (upload/live)
  - status
  - created_at

- **results** - Analysis results
  - analysis_id
  - user_id
  - predicted_disease
  - confidence_score
  - all_predictions
  - notes
  - created_at

## API Endpoints

### Authentication

- `POST /api/register` - Register new user
- `POST /api/login` - Login user

### Analysis

- `POST /api/analyze` - Analyze blood smear image
- `GET /api/results?user_id={userId}` - Get user's results
- `GET /api/stats/{userId}` - Get user statistics
- `DELETE /api/results/{resultId}` - Delete a result

## Configuration

You can modify the following in `server.js`:

- `PORT` - Server port (default: 5001)
- `MONGODB_URI` - MongoDB connection string (default: mongodb://bhanu:bhanu123@localhost:27017/bloodsmear?authSource=admin)
- `DB_NAME` - Database name (default: bloodsmear)

## Testing

You can test the API using:
- Postman
- cURL
- The frontend application

## Integration with ML Model

The `/api/analyze` endpoint currently returns mock data. To integrate your ML model:

1. Install your ML model dependencies (TensorFlow.js, ONNX, etc.)
2. Load your model in the server
3. Replace the mock predictions in the analyze endpoint with actual model predictions

Example:
```javascript
// Load your model
const model = await loadModel();

// In the analyze endpoint
const predictions = await model.predict(imageData);
```

## Troubleshooting

### MongoDB Connection Issues

If you can't connect to MongoDB:
1. Make sure MongoDB service is running
2. Check the connection string matches your MongoDB setup
3. Verify the port (default: 27017)

### Port Already in Use

If port 5001 is already in use, change the PORT variable in server.js

### CORS Issues

The server is configured to allow all origins. For production, update the CORS configuration to only allow your frontend domain.
