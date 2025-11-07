// js/results.js - Updated for Flask backend
import { requireAuth, updateUserInfo } from './auth.js';

const API_BASE = 'http://localhost:5001/api';

let allAnalyses = [];

document.addEventListener('DOMContentLoaded', function() {
    const user = requireAuth();
    if (!user) return;

    updateUserInfo();
    loadUserResults(user.user_id);
    setupEventListeners();
    setupLogout();
});

async function loadUserResults(userId) {
    try {
        const response = await fetch(`${API_BASE}/results?user_id=${userId}`);
        const data = await response.json();

        if (response.ok) {
            allAnalyses = data.analyses;
            displayResults(allAnalyses);
        } else {
            throw new Error(data.error || 'Failed to load results');
        }
    } catch (error) {
        console.error('Error loading results:', error);
        document.getElementById('resultsGrid').innerHTML = `
            <div class="error-state">
                <p>Failed to load results: ${error.message}</p>
            </div>
        `;
    }
}

function displayResults(analyses) {
    const resultsGrid = document.getElementById('resultsGrid');
    
    if (!analyses || analyses.length === 0) {
        resultsGrid.innerHTML = `
            <div class="no-results">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                </svg>
                <h3>No Analysis Results</h3>
                <p>Start by analyzing some blood smear images to see results here.</p>
                <a href="/analyze.html" class="btn btn-primary">Analyze Images</a>
            </div>
        `;
        return;
    }

    const resultsHTML = analyses.map(analysis => {
        const result = analysis.result;
        
        // Skip if result is invalid
        if (!result || !result.predicted_class) {
            console.warn('Invalid result data:', analysis);
            return '';
        }
        
        const date = new Date(analysis.created_at).toLocaleDateString();
        const time = new Date(analysis.created_at).toLocaleTimeString();
        const confidencePercent = result.confidence ? (result.confidence * 100).toFixed(1) : '0.0';

        return `
            <div class="result-card" data-analysis-id="${analysis.analysis_id}">
                <div class="result-header">
                    <div class="result-disease">${result.predicted_class}</div>
                    <div class="result-confidence">${confidencePercent}%</div>
                </div>
                <div class="result-meta">
                    <div class="meta-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"/>
                            <polyline points="12 6 12 12 16 14"/>
                        </svg>
                        <span>${date} at ${time}</span>
                    </div>
                    <div class="meta-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
                            <circle cx="12" cy="7" r="4"/>
                        </svg>
                        <span>${analysis.notes || 'No notes'}</span>
                    </div>
                </div>
                <div class="result-actions">
                    <button class="btn btn-secondary btn-sm view-details">View Details</button>
                    <button class="btn btn-secondary btn-sm download-report">Download</button>
                </div>
            </div>
        `;
    }).join('');

    resultsGrid.innerHTML = resultsHTML;
    attachResultCardEvents();
}

function setupEventListeners() {
    // Search functionality
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', filterResults);

    // Filter functionality
    const diseaseFilter = document.getElementById('diseaseFilter');
    const dateFilter = document.getElementById('dateFilter');
    
    diseaseFilter.addEventListener('change', filterResults);
    dateFilter.addEventListener('change', filterResults);

    // Export functionality
    const exportAllBtn = document.getElementById('exportAllBtn');
    exportAllBtn.addEventListener('click', exportAllResults);

    // Modal functionality
    const modalOverlay = document.getElementById('modalOverlay');
    const closeModal = document.getElementById('closeModal');
    
    modalOverlay.addEventListener('click', closeResultModal);
    closeModal.addEventListener('click', closeResultModal);
}

function filterResults() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const diseaseFilter = document.getElementById('diseaseFilter').value;
    const dateFilter = document.getElementById('dateFilter').value;

    const filtered = allAnalyses.filter(analysis => {
        const result = analysis.result;
        
        // Skip invalid results
        if (!result || !result.predicted_class) return false;
        
        const matchesSearch = result.predicted_class.toLowerCase().includes(searchTerm) ||
                            (analysis.notes && analysis.notes.toLowerCase().includes(searchTerm));
        
        const matchesDisease = !diseaseFilter || 
                             result.predicted_class.toLowerCase().includes(diseaseFilter);
        
        const matchesDate = filterByDate(analysis.created_at, dateFilter);
        
        return matchesSearch && matchesDisease && matchesDate;
    });

    displayResults(filtered);
}

function filterByDate(dateString, filter) {
    if (!filter) return true;
    
    const date = new Date(dateString);
    const now = new Date();
    
    switch (filter) {
        case 'today':
            return date.toDateString() === now.toDateString();
        case 'week':
            const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
            return date >= weekAgo;
        case 'month':
            const monthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
            return date >= monthAgo;
        case 'year':
            const yearAgo = new Date(now.getTime() - 365 * 24 * 60 * 60 * 1000);
            return date >= yearAgo;
        default:
            return true;
    }
}

function attachResultCardEvents() {
    document.querySelectorAll('.view-details').forEach(button => {
        button.addEventListener('click', function() {
            const card = this.closest('.result-card');
            const analysisId = card.dataset.analysisId;
            const analysis = allAnalyses.find(a => a.analysis_id === analysisId);
            if (analysis) {
                showResultModal(analysis);
            }
        });
    });

    document.querySelectorAll('.download-report').forEach(button => {
        button.addEventListener('click', function() {
            const card = this.closest('.result-card');
            const analysisId = card.dataset.analysisId;
            const analysis = allAnalyses.find(a => a.analysis_id === analysisId);
            if (analysis) {
                downloadReport(analysis);
            }
        });
    });
}

function showResultModal(analysis) {
    const modal = document.getElementById('resultModal');
    const result = analysis.result;
    
    if (!result || !result.predicted_class) {
        console.error('Invalid result data');
        return;
    }
    
    // Update modal content
    document.getElementById('modalDisease').textContent = result.predicted_class;
    const confidence = result.confidence ? (result.confidence * 100).toFixed(1) : '0.0';
    document.getElementById('modalConfidence').textContent = `${confidence}% Confidence`;
    document.getElementById('modalDate').textContent = new Date(analysis.created_at).toLocaleString();
    document.getElementById('modalId').textContent = analysis.analysis_id;
    document.getElementById('modalNotes').textContent = analysis.notes || 'No notes provided';
    
    // Update predictions
    const predictionsContainer = document.getElementById('modalPredictions');
    if (result.all_predictions && result.all_predictions.length > 0) {
        predictionsContainer.innerHTML = result.all_predictions
            .map(pred => `
                <div class="prediction-row">
                    <span class="prediction-name">${pred.disease}</span>
                    <span class="prediction-value">${(pred.confidence * 100).toFixed(1)}%</span>
                </div>
            `).join('');
    } else {
        predictionsContainer.innerHTML = '<p>No prediction details available</p>';
    }
    
    // Show modal
    modal.classList.remove('hidden');
    
    // Attach modal actions
    document.getElementById('downloadModalReport').onclick = () => downloadReport(analysis);
    document.getElementById('deleteResult').onclick = () => deleteResult(analysis.analysis_id);
}

function closeResultModal() {
    const modal = document.getElementById('resultModal');
    modal.classList.add('hidden');
}

function downloadReport(analysis) {
    const result = analysis.result;
    const date = new Date(analysis.created_at).toLocaleString();
    
    const report = `
BLOOD SMEAR ANALYSIS REPORT
============================

Analysis ID: ${analysis.analysis_id}
Date: ${date}

PRIMARY DIAGNOSIS
-----------------
Condition: ${result.predicted_class}
Confidence: ${(result.confidence * 100).toFixed(1)}%

ALL PREDICTIONS
---------------
${result.all_predictions.map(pred => 
    `${pred.disease}: ${(pred.confidence * 100).toFixed(1)}%` 
).join('\n')}

NOTES
-----
${analysis.notes || 'No notes provided'}

Generated by Blood Smear Analysis System
    `.trim();

    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `blood-analysis-${analysis.analysis_id}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function exportAllResults() {
    if (allAnalyses.length === 0) {
        alert('No results to export');
        return;
    }

    const exportData = allAnalyses.map(analysis => ({
        analysis_id: analysis.analysis_id,
        date: analysis.created_at,
        predicted_class: analysis.result.predicted_class,
        confidence: (analysis.result.confidence * 100).toFixed(1) + '%',
        notes: analysis.notes || ''
    }));

    const csv = convertToCSV(exportData);
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `blood-analysis-export-${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function convertToCSV(data) {
    const headers = ['Analysis ID', 'Date', 'Condition', 'Confidence', 'Notes'];
    const rows = data.map(item => [
        item.analysis_id,
        item.date,
        item.predicted_class,
        item.confidence,
        `"${item.notes.replace(/"/g, '""')}"` 
    ]);
    
    return [headers, ...rows].map(row => row.join(',')).join('\n');
}

function deleteResult(analysisId) {
    if (confirm('Are you sure you want to delete this analysis result?')) {
        // Note: You'll need to implement a DELETE endpoint in your Flask backend
        alert('Delete functionality would be implemented here with a DELETE endpoint');
        console.log('Would delete analysis:', analysisId);
    }
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
