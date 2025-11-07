# MongoDB Connection Setup Guide

## ✅ Configuration Complete

Your MongoDB connection has been configured with the following settings:

### Connection Details
- **MongoDB URI**: `mongodb://localhost:27017/`
- **Database Name**: `blood_smear_analysis`
- **Connection Name**: `bloodsmear` (in MongoDB Compass)

### Required Collections
- `users` - Stores user accounts and authentication data
- `analyses` - Stores blood smear analysis records
- `results` - Stores analysis results and predictions

---

## 🚀 Quick Start

### Step 1: Start MongoDB

Choose one of these methods:

#### Method A: Using MongoDB Compass (Recommended - No Admin Required)
1. Open **MongoDB Compass**
2. Use connection string: `mongodb://localhost:27017/`
3. Connection name: `bloodsmear`
4. Click **"Save & Connect"**
5. MongoDB will start automatically

#### Method B: Using Windows Service (Requires Admin)
```powershell
# Open PowerShell as Administrator
net start MongoDB
```

#### Method C: Check MongoDB Status
```powershell
Get-Service MongoDB
```

---

### Step 2: Test MongoDB Connection

#### For Python Backend:
```bash
cd "c:\Users\SIVA\Downloads\project-bolt-sb1-zqlrzvfe (1)\project"
python test_mongodb_connection.py
```

#### For Node.js Server:
```bash
cd "c:\Users\SIVA\Downloads\project-bolt-sb1-zqlrzvfe (1)\project\server"
node test_mongodb_connection.js
```

**Expected Output:**
```
============================================================
MongoDB Connection Test
============================================================

1. Connecting to MongoDB at: mongodb://localhost:27017/
   ✓ Successfully connected to MongoDB!

2. Accessing database: blood_smear_analysis
   ✓ Database accessed successfully
   Existing collections: users, analyses, results

3. Verifying required collections...
   ✓ Collection exists: users
   ✓ Collection exists: analyses
   ✓ Collection exists: results

4. Testing write operation...
   ✓ Write test successful

5. Testing read operation...
   ✓ Read test successful

6. Cleanup completed

7. Database Statistics:
   - users: 0 documents
   - analyses: 0 documents
   - results: 0 documents

============================================================
✓ All tests passed! MongoDB is ready to use.
============================================================
```

---

### Step 3: Start Your Application

#### Terminal 1 - Start Backend (Python Flask):
```bash
cd "c:\Users\SIVA\Downloads\project-bolt-sb1-zqlrzvfe (1)\project\backend"
python app.py
```

**Expected Output:**
```
Model loaded: XX.XX% accuracy
Using device: cuda
Starting Flask server on http://0.0.0.0:5001
```

#### Terminal 2 - Start Server (Node.js):
```bash
cd "c:\Users\SIVA\Downloads\project-bolt-sb1-zqlrzvfe (1)\project\server"
node server.js
```

**Expected Output:**
```
Connected to MongoDB
Server running on http://localhost:5001
MongoDB URI: mongodb://localhost:27017/
Database: blood_smear_analysis
```

#### Terminal 3 - Start Frontend (Vite):
```bash
cd "c:\Users\SIVA\Downloads\project-bolt-sb1-zqlrzvfe (1)\project"
npm run dev
```

---

## 🔍 Verify Connection in MongoDB Compass

1. Open MongoDB Compass
2. Connect to `mongodb://localhost:27017/`
3. You should see the database: `blood_smear_analysis`
4. Inside, you'll find collections:
   - `users`
   - `analyses`
   - `results`

---

## 📝 Environment Variables

Your `.env` file now includes:

```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB_NAME=blood_smear_analysis

# Supabase Configuration (Legacy - can be removed if not used)
VITE_SUPABASE_URL=https://jswgbyyfbehnxgqvafuc.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 🔧 Connection Code

### Python (Flask Backend)
```python
from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'blood_smear_analysis'

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db['users']
analyses_collection = db['analyses']
```

### Node.js (Express Server)
```javascript
const { MongoClient } = require('mongodb');

const MONGODB_URI = 'mongodb://localhost:27017/';
const DB_NAME = 'blood_smear_analysis';

MongoClient.connect(MONGODB_URI, { useUnifiedTopology: true })
    .then(client => {
        console.log('Connected to MongoDB');
        db = client.db(DB_NAME);
    })
    .catch(error => console.error('MongoDB connection error:', error));
```

---

## ❌ Troubleshooting

### Error: "Connection refused" or "ECONNREFUSED"
**Solution**: MongoDB is not running
- Start MongoDB using one of the methods in Step 1
- Verify with: `Get-Service MongoDB`

### Error: "Access is denied"
**Solution**: You need admin privileges
- Use MongoDB Compass method instead (doesn't require admin)
- Or run PowerShell as Administrator

### Error: "Service not found"
**Solution**: MongoDB might not be installed as a service
- Use MongoDB Compass to connect
- Or reinstall MongoDB: https://www.mongodb.com/try/download/community

### MongoDB Compass won't connect
**Solution**: Check MongoDB installation
- Verify MongoDB is installed: `C:\Program Files\MongoDB\`
- Reinstall if needed
- Check if port 27017 is available

### Backend shows "pymongo not found"
**Solution**: Install Python dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Server shows "mongodb module not found"
**Solution**: Install Node.js dependencies
```bash
cd server
npm install
```

---

## 📊 Database Schema

### Users Collection
```javascript
{
  "_id": ObjectId,
  "email": String,
  "password": String (hashed),
  "full_name": String,
  "role": String,
  "created_at": Date
}
```

### Analyses Collection
```javascript
{
  "_id": ObjectId,
  "user_id": String,
  "image_data": String (base64),
  "analysis_type": String,
  "status": String,
  "created_at": Date
}
```

### Results Collection
```javascript
{
  "_id": ObjectId,
  "analysis_id": String,
  "user_id": String,
  "predicted_disease": String,
  "confidence_score": Number,
  "all_predictions": Array,
  "notes": String,
  "created_at": Date
}
```

---

## 🎯 Next Steps

1. ✅ MongoDB connection configured
2. ✅ Environment variables set
3. ✅ Test scripts created
4. 🔄 Test the connection (run test scripts)
5. 🔄 Start your application servers
6. 🔄 Test user registration and login
7. 🔄 Test blood smear analysis

---

## 📞 Support

If you encounter any issues:
1. Check MongoDB is running: `Get-Service MongoDB`
2. Run the test scripts to diagnose the issue
3. Check the troubleshooting section above
4. Verify all dependencies are installed

---

**Status**: ✅ MongoDB connection is configured and ready to use!
