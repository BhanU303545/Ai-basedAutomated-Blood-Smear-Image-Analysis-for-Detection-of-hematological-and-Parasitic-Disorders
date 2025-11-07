const express = require('express');
const cors = require('cors');
const { MongoClient, ObjectId } = require('mongodb');
const bcrypt = require('bcryptjs');
const path = require('path');
const { analyzeImage } = require('./modelService');

const app = express();
const PORT = 5001;

// Model configuration
const MODEL_PATH = path.join(__dirname, '..', 'backend', 'models', 'best_model.pth');
const MODEL_NAME = 'best_model.pth';

// MongoDB connection (Authenticated)
const MONGODB_URI = 'mongodb://bhanu:bhanu123@localhost:27017/bloodsmear?authSource=admin';
const DB_NAME = 'bloodsmear';

let db;
let model = null; // Will hold the loaded model

// Load ML Model (PyTorch model)
// TODO: Implement model loading with ONNX Runtime or Python bridge
async function loadModel() {
    try {
        console.log(`Loading model: ${MODEL_NAME}`);
        console.log(`Model path: ${MODEL_PATH}`);
        
        // TODO: Load your PyTorch model here
        // Options:
        // 1. Convert .pth to ONNX format and use onnxruntime-node
        // 2. Use a Python bridge (child_process to call Python script)
        // 3. Use TensorFlow.js if you convert the model
        
        console.log('Note: Model loading not implemented. Using mock predictions.');
        console.log('To use the actual model, implement one of the following:');
        console.log('1. Convert best_model.pth (EfficientNet-B0) to ONNX format');
        console.log('2. Create a Python API service');
        console.log('3. Use TensorFlow.js conversion');
        
        return null;
    } catch (error) {
        console.error('Error loading model:', error);
        return null;
    }
}

// Connect to MongoDB
MongoClient.connect(MONGODB_URI, { useUnifiedTopology: true })
    .then(async client => {
        console.log('Connected to MongoDB (authenticated)');
        console.log(`Database: ${DB_NAME}`);
        db = client.db(DB_NAME);
        
        // Load the model
        model = await loadModel();
    })
    .catch(error => console.error('MongoDB connection error:', error));

// Middleware
app.use(cors());
app.use(express.json({ limit: '50mb' }));

// Register endpoint
app.post('/api/register', async (req, res) => {
    try {
        const { email, password, full_name, role } = req.body;

        // Check if user already exists
        const existingUser = await db.collection('users').findOne({ email });
        if (existingUser) {
            return res.json({ error: 'User already exists' });
        }

        // Hash password
        const hashedPassword = await bcrypt.hash(password, 10);

        // Create user
        const result = await db.collection('users').insertOne({
            email,
            password: hashedPassword,
            full_name,
            role,
            created_at: new Date()
        });

        const user = {
            user_id: result.insertedId.toString(),
            email,
            full_name,
            role
        };

        res.json({ user });
    } catch (error) {
        console.error('Registration error:', error);
        res.json({ error: 'Registration failed' });
    }
});

// Login endpoint
app.post('/api/login', async (req, res) => {
    try {
        const { email, password } = req.body;

        // Find user
        const user = await db.collection('users').findOne({ email });
        if (!user) {
            return res.json({ error: 'Invalid credentials' });
        }

        // Verify password
        const validPassword = await bcrypt.compare(password, user.password);
        if (!validPassword) {
            return res.json({ error: 'Invalid credentials' });
        }

        const userData = {
            user_id: user._id.toString(),
            email: user.email,
            full_name: user.full_name,
            role: user.role
        };

        res.json({ user: userData });
    } catch (error) {
        console.error('Login error:', error);
        res.json({ error: 'Login failed' });
    }
});

// Analyze image endpoint
app.post('/api/analyze', async (req, res) => {
    try {
        const { image, user_id, notes } = req.body;

        // TODO: Use best_model.pth (EfficientNet-B0) model for predictions
        // Currently using mock data until model integration is complete
        // Model path: ${MODEL_PATH}
        const useMock = !model; // Use mock if model not loaded
        const predictionResult = await analyzeImage(image, useMock);
        
        const topPrediction = {
            disease: predictionResult.predicted_disease,
            confidence: predictionResult.confidence
        };
        
        const allPredictions = predictionResult.all_predictions;

        // Save analysis to database
        const analysis = await db.collection('analyses').insertOne({
            user_id,
            image_data: image,
            analysis_type: 'upload',
            status: 'completed',
            created_at: new Date()
        });

        // Save result
        const result = await db.collection('results').insertOne({
            analysis_id: analysis.insertedId.toString(),
            user_id,
            predicted_disease: topPrediction.disease,
            confidence_score: topPrediction.confidence,
            all_predictions: allPredictions,
            notes,
            created_at: new Date()
        });

        res.json({
            id: result.insertedId.toString(),
            analysis_id: analysis.insertedId.toString(),
            predicted_disease: topPrediction.disease,
            confidence_score: topPrediction.confidence,
            all_predictions: allPredictions,
            notes,
            created_at: new Date()
        });
    } catch (error) {
        console.error('Analysis error:', error);
        res.json({ error: 'Analysis failed' });
    }
});

// Get results endpoint
app.get('/api/results', async (req, res) => {
    try {
        const { user_id } = req.query;

        const results = await db.collection('results')
            .find({ user_id })
            .sort({ created_at: -1 })
            .toArray();

        // Get analysis data for each result
        const resultsWithAnalyses = await Promise.all(results.map(async (result) => {
            const analysis = await db.collection('analyses').findOne({
                _id: new ObjectId(result.analysis_id)
            });
            return {
                ...result,
                id: result._id.toString(),
                analyses: analysis ? {
                    id: analysis._id.toString(),
                    image_url: analysis.image_data,
                    analysis_type: analysis.analysis_type,
                    created_at: analysis.created_at
                } : null
            };
        }));

        res.json({ results: resultsWithAnalyses });
    } catch (error) {
        console.error('Get results error:', error);
        res.json({ error: 'Failed to fetch results' });
    }
});

// Get user stats endpoint
app.get('/api/stats/:userId', async (req, res) => {
    try {
        const { userId } = req.params;

        const analyses = await db.collection('analyses')
            .find({ user_id: userId })
            .sort({ created_at: -1 })
            .toArray();

        const results = await db.collection('results')
            .find({ user_id: userId })
            .sort({ created_at: -1 })
            .toArray();

        res.json({ analyses, results });
    } catch (error) {
        console.error('Get stats error:', error);
        res.json({ error: 'Failed to fetch stats' });
    }
});

// Delete result endpoint
app.delete('/api/results/:resultId', async (req, res) => {
    try {
        const { resultId } = req.params;

        await db.collection('results').deleteOne({ _id: new ObjectId(resultId) });

        res.json({ success: true });
    } catch (error) {
        console.error('Delete error:', error);
        res.json({ error: 'Failed to delete result' });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
    console.log(`MongoDB URI: ${MONGODB_URI}`);
    console.log(`Database: ${DB_NAME}`);
});
