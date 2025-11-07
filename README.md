# Blood Smear Analysis System

Automated detection system for hematological and parasitic disorders using blood smear image analysis.

## Features

- User authentication (registration and login)
- Upload and analyze blood smear images
- Live microscopic analysis using camera
- Results history with filtering and search
- Downloadable analysis reports
- Dashboard with analytics and statistics

## Detectable Conditions

- Malaria
- Babesiosis
- Trypanosomiasis
- Leishmaniasis
- Leukemia
- Anemia
- Sickle Cell Anemia
- Thrombocytopenia

## Setup Instructions

1. **Environment Variables**

Create a `.env` file in the root directory:

```env
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB_NAME=blood_smear_analysis
```

2. **Install Dependencies**

```bash
npm install
```

3. **Database Setup**

Start MongoDB and the database will automatically create the following collections:
- `users` - User accounts and authentication
- `analyses` - Analysis records
- `results` - Analysis results and predictions

See `MONGODB_CONNECTION_SETUP.md` for detailed setup instructions.

4. **Start Backend Services**

```bash
# Terminal 1 - Python Backend
cd backend
python app.py

# Terminal 2 - Node.js Server
cd server
node server.js
```

5. **Run Development Server**

```bash
npm run dev
```

6. **Build for Production**

```bash
npm run build
```

## Project Structure

```
project/
├── index.html              # Login/Register page
├── dashboard.html          # Dashboard with analytics
├── analyze.html            # Image upload and analysis
├── live.html              # Live microscopic analysis
├── results.html           # Results history
├── styles/
│   └── main.css           # All styling
├── js/
│   ├── auth.js            # Authentication logic
│   ├── api.js             # API client
│   ├── dashboard.js       # Dashboard functionality
│   ├── analyze.js         # Image analysis logic
│   ├── live.js            # Live camera analysis
│   └── results.js         # Results management
├── backend/
│   └── app.py             # Python Flask ML backend
└── server/
    └── server.js          # Node.js Express server
```

## Usage

1. **Register/Login**: Create an account or sign in
2. **Upload Analysis**: Go to "Image Analysis" to upload blood smear images
3. **Live Analysis**: Use "Live Microscopy" for real-time camera analysis
4. **View Results**: Check "Results History" for all past analyses
5. **Dashboard**: Monitor statistics and trends

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Backend**: 
  - Python Flask (ML inference)
  - Node.js Express (API server)
- **Database**: MongoDB
- **ML Framework**: PyTorch (EfficientNet-B0)
- **Bundler**: Vite

## Model Reference

The system uses the `best_model.pth` (EfficientNet-B0) model for disease prediction. The model is loaded in the Python Flask backend for inference.

## Security

- Password hashing with bcrypt
- User authentication with session management
- Users can only access their own data
- Secure API endpoints with validation
