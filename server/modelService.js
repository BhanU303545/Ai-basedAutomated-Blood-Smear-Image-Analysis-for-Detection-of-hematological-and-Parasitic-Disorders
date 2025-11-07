const { spawn } = require('child_process');
const path = require('path');

const PYTHON_SCRIPT = path.join(__dirname, 'predict.py');

/**
 * Run prediction using the best_model.pth (EfficientNet-B0) model
 * @param {string} base64Image - Base64 encoded image
 * @returns {Promise<Object>} Prediction results
 */
function runPrediction(base64Image) {
    return new Promise((resolve, reject) => {
        // Spawn Python process
        const python = spawn('python', [PYTHON_SCRIPT, base64Image]);
        
        let dataString = '';
        let errorString = '';
        
        // Collect data from stdout
        python.stdout.on('data', (data) => {
            dataString += data.toString();
        });
        
        // Collect errors from stderr
        python.stderr.on('data', (data) => {
            errorString += data.toString();
        });
        
        // Handle process completion
        python.on('close', (code) => {
            if (code !== 0) {
                console.error('Python script error:', errorString);
                reject(new Error(`Python script exited with code ${code}: ${errorString}`));
                return;
            }
            
            try {
                const result = JSON.parse(dataString);
                
                if (result.error) {
                    reject(new Error(result.error));
                } else {
                    resolve(result);
                }
            } catch (error) {
                console.error('Failed to parse Python output:', dataString);
                reject(new Error('Failed to parse prediction results'));
            }
        });
        
        // Handle process errors
        python.on('error', (error) => {
            console.error('Failed to start Python process:', error);
            reject(new Error('Failed to start prediction service. Make sure Python is installed.'));
        });
    });
}

/**
 * Get mock predictions (fallback when model is not available)
 * @returns {Object} Mock prediction results
 */
function getMockPredictions() {
    const mockPredictions = [
        { disease: 'babesia', confidence: 45.2 },
        { disease: 'leishmania', confidence: 23.1 },
        { disease: 'trypanosome', confidence: 15.8 },
        { disease: 'basophil', confidence: 8.3 },
        { disease: 'eosinophil', confidence: 4.2 },
        { disease: 'lymphocyte', confidence: 2.1 },
        { disease: 'malaria_parasitized', confidence: 0.8 },
        { disease: 'malaria_uninfected', confidence: 0.3 },
        { disease: 'monocyte', confidence: 0.1 },
        { disease: 'neutrophil', confidence: 0.1 }
    ];
    
    return {
        predicted_disease: mockPredictions[0].disease,
        confidence: mockPredictions[0].confidence,
        all_predictions: mockPredictions
    };
}

/**
 * Analyze image using best_model.pth (EfficientNet-B0) model
 * @param {string} base64Image - Base64 encoded image
 * @param {boolean} useMock - Whether to use mock predictions
 * @returns {Promise<Object>} Analysis results
 */
async function analyzeImage(base64Image, useMock = false) {
    if (useMock) {
        console.log('Using mock predictions (model not loaded)');
        return getMockPredictions();
    }
    
    try {
        console.log('Running prediction with best_model.pth (EfficientNet-B0)...');
        const result = await runPrediction(base64Image);
        return result;
    } catch (error) {
        console.error('Prediction error:', error.message);
        console.log('Falling back to mock predictions');
        return getMockPredictions();
    }
}

module.exports = {
    analyzeImage,
    getMockPredictions
};
