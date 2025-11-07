import torch
import torch.nn as nn
import torch.nn.functional as F
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime, timedelta
import base64
from PIL import Image
import io
import os
import uuid
import torchvision.transforms as transforms
import torchvision.models as models
from dotenv import load_dotenv
import urllib.request
import sys

# Load environment variables
load_dotenv()

def download_model_from_url(url, destination):
    """Download model file from external URL if not present locally"""
    try:
        if os.path.exists(destination):
            print(f"✓ Model file already exists at {destination}")
            return True
        
        print(f"Downloading model from {url}...")
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        
        # Download with progress
        def reporthook(count, block_size, total_size):
            percent = int(count * block_size * 100 / total_size)
            sys.stdout.write(f"\rDownloading: {percent}%")
            sys.stdout.flush()
        
        urllib.request.urlretrieve(url, destination, reporthook)
        print(f"\n✓ Model downloaded successfully to {destination}")
        return True
    except Exception as e:
        print(f"✗ Error downloading model: {e}")
        return False

app = Flask(__name__)
CORS(app)

# MongoDB Configuration from environment variables
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/bloodsmear')
DB_NAME = os.getenv('DB_NAME', 'bloodsmear')

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    users_collection = db['users']
    analyses_collection = db['analyses']
    # Test connection
    client.server_info()
    print(f"✓ Connected to MongoDB: {DB_NAME}")
except Exception as e:
    print(f"✗ MongoDB connection error: {e}")
    print("Application will start but database operations will fail.")

class BloodSmearAnalyzer:
    def __init__(self, model_path=None):
        # Use environment variable if no path provided
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Get model path from environment or use default
        model_path = model_path or os.getenv('MODEL_PATH', 'best_model.pth')
        
        try:
            # Load model checkpoint
            checkpoint = torch.load(model_path, map_location=self.device)
            self.class_names = checkpoint['class_names']
            
            # Initialize model architecture
            self.model = models.efficientnet_b0(pretrained=False)
            in_features = self.model.classifier[1].in_features
            
            # Define custom classifier
            self.model.classifier = nn.Sequential(
                nn.Dropout(0.3),
                nn.Linear(in_features, 512),
                nn.ReLU(),
                nn.BatchNorm1d(512),
                nn.Dropout(0.2),
                nn.Linear(512, len(self.class_names))
            )
            
            # Load model weights
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.model.to(self.device)
            self.model.eval()
            
            # Image transformations
            self.transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                   std=[0.229, 0.224, 0.225])
            ])
            
            print(f"✓ Model loaded successfully from {model_path}")
            print(f"✓ Using device: {self.device}")
            
        except Exception as e:
            print(f"✗ Error loading model: {str(e)}")
            raise
    
    def predict(self, image_data):
        """Predict disease from base64 encoded image"""
        try:
            # Remove data URL prefix if present
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decode base64 to image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            
            # Apply transformations
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # Make prediction
            with torch.no_grad():
                outputs = self.model(image_tensor)
                probabilities = F.softmax(outputs, dim=1)
            
            # Get all predictions
            probs = probabilities[0].cpu().numpy()
            predictions = []
            
            for idx, prob in enumerate(probs):
                predictions.append({
                    'disease': self.class_names[idx],
                    'confidence': float(prob * 100)
                })
            
            # Sort by confidence
            predictions.sort(key=lambda x: x['confidence'], reverse=True)
            
            return {
                'status': 'success',
                'predicted_disease': predictions[0]['disease'],
                'confidence': predictions[0]['confidence'],
                'all_predictions': predictions
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

# Download model if not present (for deployment)
MODEL_PATH = os.getenv('MODEL_PATH', 'best_model.pth')
MODEL_URL = os.getenv('MODEL_URL', '')

if MODEL_URL and not os.path.exists(MODEL_PATH):
    print("Model file not found locally. Attempting to download...")
    download_model_from_url(MODEL_URL, MODEL_PATH)

analyzer = BloodSmearAnalyzer(MODEL_PATH)

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        role = data.get('role', 'technician')
        
        existing_user = users_collection.find_one({'email': email})
        if existing_user:
            return jsonify({'error': 'User already exists'}), 400
        
        user_id = str(uuid.uuid4())
        user_data = {
            'user_id': user_id,
            'email': email,
            'password': password,
            'name': name,
            'role': role,
            'created_at': datetime.utcnow()
        }
        
        users_collection.insert_one(user_data)
        
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'user_id': user_id,
                'email': email,
                'name': name,
                'role': role
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        user = users_collection.find_one({'email': email, 'password': password})
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        return jsonify({
            'message': 'Login successful',
            'user': {
                'user_id': user['user_id'],
                'email': user['email'],
                'name': user['name'],
                'role': user['role']
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    try:
        data = request.json
        image_data = data.get('image')
        user_id = data.get('user_id')
        notes = data.get('notes', '')
        
        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400
        
        result = analyzer.predict(image_data)
        
        if result['status'] == 'error':
            return jsonify({'error': result['error']}), 500
        
        analysis_id = str(uuid.uuid4())
        analysis_data = {
            'analysis_id': analysis_id,
            'user_id': user_id,
            'notes': notes,
            'result': result,
            'created_at': datetime.utcnow()
        }
        
        analyses_collection.insert_one(analysis_data)
        
        return jsonify({
            'analysis_id': analysis_id,
            'result': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/results', methods=['GET'])
def get_results():
    try:
        user_id = request.args.get('user_id')
        analyses = list(analyses_collection.find(
            {'user_id': user_id},
            {'_id': 0}
        ).sort('created_at', -1).limit(100))
        
        for analysis in analyses:
            analysis['created_at'] = analysis['created_at'].isoformat()
        
        return jsonify({
            'analyses': analyses
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats/<user_id>', methods=['GET'])
def get_user_stats(user_id):
    try:
        total_analyses = analyses_collection.count_documents({'user_id': user_id})
        
        start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_analyses = analyses_collection.count_documents({
            'user_id': user_id,
            'created_at': {'$gte': start_of_month}
        })
        
        today = datetime.utcnow()
        start_of_week = today.replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_week = start_of_week - timedelta(days=today.weekday())
        week_analyses = analyses_collection.count_documents({
            'user_id': user_id,
            'created_at': {'$gte': start_of_week}
        })
        
        return jsonify({
            'total_analyses': total_analyses,
            'month_analyses': month_analyses,
            'week_analyses': week_analyses
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        test_image = Image.new('RGB', (224, 224), color='black')
        buffered = io.BytesIO()
        test_image.save(buffered, format="JPEG")
        test_image_data = base64.b64encode(buffered.getvalue()).decode()
        
        result = analyzer.predict(test_image_data)
        
        return jsonify({
            'status': 'healthy',
            'model_loaded': True,
            'device': str(analyzer.device),
            'test_prediction_status': result['status']
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'model_loaded': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    model_path = 'best_model.pth'
    if not os.path.exists(model_path):
        print(f"Warning: Model file '{model_path}' not found")
    
    print(f"Using device: {analyzer.device}")
    
    # Use dynamic port for Render deployment
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Flask server on http://0.0.0.0:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=False)