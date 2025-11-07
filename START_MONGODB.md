# 🚀 Start MongoDB - Quick Guide

## Current Status
❌ **MongoDB is NOT running** - You need to start it first!

---

## ✅ EASIEST METHOD: Use MongoDB Compass

### Step-by-Step:

1. **Open MongoDB Compass** (the application from your screenshot)

2. **Enter Connection String**:
   ```
   mongodb://localhost:27017/
   ```

3. **Connection Name**: `bloodsmear`

4. **Click "Save & Connect"**

5. **MongoDB will start automatically!** 🎉

**This method doesn't require admin privileges and is the simplest way!**

---

## Alternative Methods (If Compass doesn't work)

### Method 1: Start as Windows Service (Requires Admin)

1. **Right-click PowerShell** → **Run as Administrator**
2. Run:
   ```powershell
   net start MongoDB
   ```

### Method 2: Start MongoDB Manually

1. Open PowerShell
2. Navigate to MongoDB bin folder:
   ```powershell
   cd "C:\Program Files\MongoDB\Server\7.0\bin"
   ```
   (Adjust version number if different)

3. Start MongoDB:
   ```powershell
   .\mongod.exe --dbpath "C:\data\db"
   ```

### Method 3: Use Services Manager (GUI)

1. Press `Win + R`
2. Type: `services.msc`
3. Press Enter
4. Find **"MongoDB Server"** in the list
5. Right-click → **Start**

---

## 🔍 Verify MongoDB is Running

After starting MongoDB, run this command:

```powershell
python test_mongodb_connection.py
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
...
✓ All tests passed! MongoDB is ready to use.
============================================================
```

---

## 📋 What to Do Next

### Once MongoDB is Running:

1. ✅ **Keep MongoDB Compass open** (to keep MongoDB running)

2. **Start Backend Server** (Terminal 1):
   ```bash
   cd backend
   python app.py
   ```

3. **Start Node.js Server** (Terminal 2):
   ```bash
   cd server
   node server.js
   ```

4. **Start Frontend** (Terminal 3):
   ```bash
   npm run dev
   ```

---

## ❌ Troubleshooting

### "MongoDB Compass won't connect"
- Check if MongoDB is installed: `C:\Program Files\MongoDB\`
- Download and install: https://www.mongodb.com/try/download/community
- Make sure port 27017 is not blocked by firewall

### "Access is denied" when starting service
- You need to run PowerShell as **Administrator**
- Or use MongoDB Compass method (doesn't need admin)

### "mongod.exe not found"
- MongoDB might not be installed
- Install MongoDB Community Server: https://www.mongodb.com/try/download/community
- During installation, select "Install MongoDB as a Service"

---

## 🎯 Quick Checklist

- [ ] MongoDB Compass installed
- [ ] Connected to `mongodb://localhost:27017/` in Compass
- [ ] Connection successful (green indicator)
- [ ] Database `blood_smear_analysis` visible
- [ ] Test script passes: `python test_mongodb_connection.py`
- [ ] Backend server starts without MongoDB errors
- [ ] Application works correctly

---

## 💡 Pro Tip

**Keep MongoDB Compass open while developing!**

When you close MongoDB Compass, MongoDB might stop. To keep it running:
- Keep Compass minimized in the background
- Or set up MongoDB as a Windows service (requires admin)

---

**Current Action Required**: 
👉 **Open MongoDB Compass and connect to `mongodb://localhost:27017/`**

Then run the test script to verify the connection works!
