# MongoDB Connection Guide

## Quick Start Methods

### Method 1: Use MongoDB Compass (EASIEST) ✅

1. **Open MongoDB Compass** (the application you just showed)
2. **Connection String**: `mongodb://localhost:27017/`
3. **Click "Save & Connect"**
4. MongoDB will start automatically

**This is the easiest method and doesn't require admin privileges!**

---

### Method 2: Start as Windows Service (Requires Admin)

1. **Right-click on PowerShell** → **Run as Administrator**
2. Run:
   ```powershell
   net start MongoDB
   ```
3. You should see: "The MongoDB Server (MongoDB) service was started successfully."

---

### Method 3: Use Services Manager (GUI)

1. Press `Win + R`
2. Type: `services.msc`
3. Press Enter
4. Find **"MongoDB Server"** in the list
5. Right-click → **Start**

---

### Method 4: Use Task Manager

1. Press `Ctrl + Shift + Esc`
2. Click **"Services"** tab at the bottom
3. Find **"MongoDB"** in the list
4. Right-click → **Start**

---

## Verify MongoDB is Running

### Check in PowerShell:
```powershell
Get-Service MongoDB
```

You should see:
```
Status   Name               DisplayName
------   ----               -----------
Running  MongoDB            MongoDB Server (MongoDB)
```

### Check with MongoDB Compass:
- Open MongoDB Compass
- Connect to `mongodb://localhost:27017/`
- You should see your databases listed

---

## After MongoDB is Running

### 1. Verify Database Exists

In MongoDB Compass, you should see:
- **Database**: `blood_smear_analysis`
  - **Collection**: `users`
  - **Collection**: `analyses`

### 2. Restart Flask Server

```bash
cd backend
python app.py
```

You should see:
```
Model loaded: XX.XX% accuracy
Using device: cuda
Starting Flask server on http://0.0.0.0:5001
```

**No MongoDB connection errors!**

### 3. Test Your Application

1. Go to `http://localhost:5174` (or your Vite dev server port)
2. Login
3. Try analyzing an image
4. It should work without MongoDB errors!

---

## Troubleshooting

### Error: "Access is denied"
- You need to run PowerShell as **Administrator**
- Or use MongoDB Compass method (doesn't need admin)

### Error: "Service not found"
- MongoDB might not be installed as a service
- Use MongoDB Compass to connect instead

### Error: "Connection refused"
- MongoDB is not running
- Start it using one of the methods above

### MongoDB Compass won't connect
- Check if MongoDB is installed: `C:\Program Files\MongoDB\`
- Reinstall MongoDB if needed: https://www.mongodb.com/try/download/community

---

## Recommended Workflow

**For Development:**

1. **Start MongoDB Compass** → Connect to `mongodb://localhost:27017/`
2. **Keep MongoDB Compass open** while developing
3. **Start Flask server**: `python backend/app.py`
4. **Start Vite dev server**: `npm run dev`
5. **Develop and test** your application

**MongoDB Compass will keep MongoDB running as long as it's open!**

---

## Current Status

✅ MongoDB service exists on your system  
❌ MongoDB service is currently **stopped**  
📝 **Action needed**: Start MongoDB using one of the methods above

---

## Quick Commands Reference

```powershell
# Check MongoDB status
Get-Service MongoDB

# Start MongoDB (requires admin)
net start MongoDB

# Stop MongoDB (requires admin)
net stop MongoDB

# Check if MongoDB process is running
Get-Process mongod
```

---

**Recommendation**: Use **MongoDB Compass** method - it's the easiest and doesn't require admin privileges!
