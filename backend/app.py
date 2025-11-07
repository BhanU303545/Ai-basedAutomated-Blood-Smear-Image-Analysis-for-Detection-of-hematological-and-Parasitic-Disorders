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

app = Flask(__name__)
CORS(app)

# MongoDB Configuration (Authenticated)
MONGO_URI = 'mongodb://bhanu:bhanu123@localhost:27017/bloodsmear?authSource=admin'
DB_NAME = 'bloodsmear'

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_collection = db['users']
analyses_collection = db['analyses']

print(f"Connected to MongoDB: {DB_NAME}")

class BloodSmearAnalyzer:
    def __init__(self, model_path='models/best_model.pth'):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        checkpoint = torch.load(model_path, map_location=self.device)
        self.class_names = checkpoint['class_names']
        
        self.model = models.efficientnet_b0()
        in_features = self.model.classifier[1].in_features
        self.model.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(in_features, 512),
            nn.ReLU(),
            nn.BatchNorm1d(512),
            nn.Dropout(0.2),
            nn.Linear(512, len(self.class_names))
        )
        
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.to(self.device)
        self.model.eval()
        
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        print(f"Model loaded: {checkpoint['val_acc']:.2f}% accuracy")
    
    def predict(self, image_data):
        try:
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            image = Image.open(io.BytesIO(base64.b64decode(image_data))).convert('RGB')
            
            inputs = self.transform(image).unsqueeze(0)
            inputs = inputs.to(self.device)
            
            with torch.no_grad():
                outputs = self.model(inputs)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                confidence, predicted_idx = torch.max(probabilities, 1)
            
            predicted_class = self.class_names[predicted_idx.item()]
            confidence_score = confidence.item()
            
            all_probs = probabilities[0].cpu().numpy()
            predictions = [
                {'disease': self.class_names[i], 'confidence': float(all_probs[i])}
                for i in range(len(self.class_names))
            ]
            predictions.sort(key=lambda x: x['confidence'], reverse=True)
            
            return {
                'predicted_class': predicted_class,
                'confidence': confidence_score,
                'all_predictions': predictions,
                'status': 'success'
            }
            
        except Exception as e:
            return {'error': str(e), 'status': 'error'}

analyzer = BloodSmearAnalyzer('models/best_model.pth')

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
    model_path = 'models/best_model.pth'
    if not os.path.exists(model_path):
        print(f"Warning: Model file '{model_path}' not found")
    
    print(f"Using device: {analyzer.device}")
    print("Starting Flask server on http://0.0.0.0:5001")
    
    app.run(host='0.0.0.0', port=5001, debug=True)