// js/analyze.js - Updated for Flask backend
import { requireAuth, updateUserInfo } from './auth.js';

const API_BASE = 'http://localhost:5001/api';

let currentImageData = null;

document.addEventListener('DOMContentLoaded', function() {
    const user = requireAuth();
    if (!user) return;

    updateUserInfo();
    setupEventListeners();
    setupLogout();
});

function setupEventListeners() {
    // File upload
    const browseBtn = document.getElementById('browseBtn');
    const imageInput = document.getElementById('imageInput');
    const uploadCard = document.getElementById('uploadCard');
    const previewCard = document.getElementById('previewCard');
    const changeImageBtn = document.getElementById('changeImageBtn');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const newAnalysisBtn = document.getElementById('newAnalysisBtn');

    browseBtn.addEventListener('click', () => imageInput.click());
    imageInput.addEventListener('change', handleImageSelect);
    changeImageBtn.addEventListener('click', resetImageSelection);
    analyzeBtn.addEventListener('click', analyzeImage);
    newAnalysisBtn.addEventListener('click', resetAnalysis);

    // Drag and drop
    uploadCard.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadCard.style.borderColor = '#007bff';
    });

    uploadCard.addEventListener('dragleave', () => {
        uploadCard.style.borderColor = '#e9ecef';
    });

    uploadCard.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadCard.style.borderColor = '#e9ecef';
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });
}

function handleImageSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

function handleFile(file) {
    if (!file.type.match('image.*')) {
        alert('Please select an image file (JPG, PNG)');
        return;
    }

    if (file.size > 10 * 1024 * 1024) {
        alert('File size must be less than 10MB');
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        currentImageData = e.target.result;
        showPreview(currentImageData, file);
    };
    reader.readAsDataURL(file);
}

function showPreview(imageData, file) {
    const uploadCard = document.getElementById('uploadCard');
    const previewCard = document.getElementById('previewCard');
    const imagePreview = document.getElementById('imagePreview');
    const imageInfo = document.getElementById('imageInfo');

    // Create image preview
    const img = document.createElement('img');
    img.src = imageData;
    img.alt = 'Blood smear preview';
    imagePreview.innerHTML = '';
    imagePreview.appendChild(img);

    // Show file info
    const fileSize = (file.size / 1024 / 1024).toFixed(2);
    imageInfo.innerHTML = `
        <div><strong>File:</strong> ${file.name}</div>
        <div><strong>Size:</strong> ${fileSize} MB</div>
        <div><strong>Type:</strong> ${file.type}</div>
    `;

    uploadCard.classList.add('hidden');
    previewCard.classList.remove('hidden');
}

function resetImageSelection() {
    const imageInput = document.getElementById('imageInput');
    imageInput.value = '';
    currentImageData = null;
    
    const uploadCard = document.getElementById('uploadCard');
    const previewCard = document.getElementById('previewCard');
    
    previewCard.classList.add('hidden');
    uploadCard.classList.remove('hidden');
}

async function analyzeImage() {
    if (!currentImageData) {
        alert('Please select an image first');
        return;
    }

    const user = requireAuth();
    if (!user) return;

    const analyzeBtn = document.getElementById('analyzeBtn');
    const processingModal = document.getElementById('processingModal');
    const notes = document.getElementById('analysisNotes').value;

    // Show processing modal
    analyzeBtn.disabled = true;
    analyzeBtn.querySelector('.btn-text').textContent = 'Analyzing...';
    processingModal.classList.remove('hidden');

    try {
        const response = await fetch(`${API_BASE}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: currentImageData,
                user_id: user.user_id,
                notes: notes
            }),
        });

        const data = await response.json();

        if (response.ok && data.result) {
            // Check if result has the expected structure
            if (data.result.status === 'error') {
                throw new Error(data.result.error || 'Analysis failed');
            }
            if (!data.result.predicted_class) {
                throw new Error('Invalid response from server: missing predicted_class');
            }
            showResults(data.result);
        } else {
            throw new Error(data.error || 'Analysis failed');
        }
    } catch (error) {
        alert('Analysis failed: ' + error.message);
    } finally {
        processingModal.classList.add('hidden');
        analyzeBtn.disabled = false;
        analyzeBtn.querySelector('.btn-text').textContent = 'Analyze Image';
    }
}

function showResults(result) {
    const resultsSection = document.getElementById('resultsSection');
    const primaryResult = document.getElementById('primaryResult');
    const predictionsList = document.getElementById('predictionsList');

    // Show primary result
    primaryResult.innerHTML = `
        <div class="result-disease">${result.predicted_class}</div>
        <div class="result-confidence">
            <div class="confidence-label">Confidence</div>
            <div class="confidence-value">${(result.confidence * 100).toFixed(1)}%</div>
            <div class="confidence-bar">
                <div class="confidence-fill" style="width: ${result.confidence * 100}%"></div>
            </div>
        </div>
    `;

    // Show all predictions
    predictionsList.innerHTML = result.all_predictions
        .map(pred => `
            <div class="prediction-item">
                <span class="prediction-disease">${pred.disease}</span>
                <span class="prediction-confidence">${(pred.confidence * 100).toFixed(1)}%</span>
            </div>
        `).join('');

    resultsSection.classList.remove('hidden');
}

function resetAnalysis() {
    const resultsSection = document.getElementById('resultsSection');
    const previewCard = document.getElementById('previewCard');
    const uploadCard = document.getElementById('uploadCard');
    const analysisNotes = document.getElementById('analysisNotes');

    resultsSection.classList.add('hidden');
    previewCard.classList.add('hidden');
    uploadCard.classList.remove('hidden');
    
    analysisNotes.value = '';
    currentImageData = null;
    
    const imageInput = document.getElementById('imageInput');
    imageInput.value = '';
}

function setupLogout() {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('currentUser');
            window.location.href = '/index.html';
        });
    }
}

// Download report functionality
document.getElementById('downloadReportBtn')?.addEventListener('click', function() {
    const primaryResult = document.getElementById('primaryResult');
    const disease = primaryResult.querySelector('.result-disease').textContent;
    const confidence = primaryResult.querySelector('.confidence-value').textContent;
    
    const report = `
Blood Smear Analysis Report
============================

Primary Diagnosis: ${disease}
Confidence: ${confidence}

Date: ${new Date().toLocaleDateString()}
Time: ${new Date().toLocaleTimeString()}

Generated by Blood Smear Analysis System
    `.trim();

    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `blood-analysis-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
});
