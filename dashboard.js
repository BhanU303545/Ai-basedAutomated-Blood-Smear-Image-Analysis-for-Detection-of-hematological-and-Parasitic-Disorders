// js/dashboard.js - Updated for Flask backend
import { requireAuth, updateUserInfo } from './auth.js';

const API_BASE = 'http://localhost:5001/api';

document.addEventListener('DOMContentLoaded', function() {
    const user = requireAuth();
    if (!user) return;

    updateUserInfo();
    loadDashboardData();
    setupLogout();
});

async function loadDashboardData() {
    const user = requireAuth();
    if (!user) return;

    updateUserInfo();

    try {
        // Load stats
        const statsResponse = await fetch(`${API_BASE}/stats/${user.user_id}`);
        const stats = await statsResponse.json();
        console.log('Stats:', stats);
        
        // Load recent analyses
        const analysesResponse = await fetch(`${API_BASE}/results?user_id=${user.user_id}`);
        const analysesData = await analysesResponse.json();
        const analyses = analysesData.analyses || [];
        console.log('Total analyses received:', analyses.length);
        console.log('Analyses data:', analyses);
        
        // Check how many have valid results
        const validAnalyses = analyses.filter(a => a.result && a.result.predicted_class);
        console.log('Valid analyses:', validAnalyses.length);

        updateStats(stats, analyses);
        updateRecentAnalyses(analyses);
        updateDiseaseChart(analyses);
        updateTimelineChart(analyses);
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

function updateStats(stats, analyses) {
    document.getElementById('totalAnalyses').textContent = stats.total_analyses;
    document.getElementById('monthAnalyses').textContent = stats.month_analyses;
    document.getElementById('weekAnalyses').textContent = stats.week_analyses;
    
    // Calculate positive results (parasitic infections)
    // Match actual model class names
    const positiveCount = analyses.filter(analysis => {
        if (!analysis.result || !analysis.result.predicted_class) return false;
        
        const className = analysis.result.predicted_class.toLowerCase();
        // Check if it's a parasitic infection (not normal blood cells)
        return className.includes('babesia') || 
               className.includes('leishmania') || 
               className.includes('trypanosome') || 
               className.includes('malaria parasitized');
    }).length;
    
    console.log('Positive results count:', positiveCount);
    console.log('All analyses:', analyses.map(a => a.result?.predicted_class));
    document.getElementById('positiveResults').textContent = positiveCount;
}

function updateRecentAnalyses(analyses) {
    const recentList = document.getElementById('recentAnalyses');
    
    console.log('updateRecentAnalyses called with:', analyses);
    
    if (!analyses || analyses.length === 0) {
        console.log('No analyses array or empty');
        recentList.innerHTML = '<div class="no-data">No recent analyses</div>';
        return;
    }

    const validAnalyses = analyses.filter(analysis => analysis.result && analysis.result.predicted_class);
    console.log('Valid analyses after filter:', validAnalyses.length);
    
    const recentItems = validAnalyses.slice(0, 5)
        .map(analysis => {
            const result = analysis.result;
            const date = new Date(analysis.created_at).toLocaleDateString();
            const confidence = result.confidence ? (result.confidence * 100).toFixed(1) : '0.0';
            
            return `
                <div class="recent-item">
                    <div class="recent-disease">${result.predicted_class}</div>
                    <div class="recent-confidence">${confidence}%</div>
                    <div class="recent-date">${date}</div>
                </div>
            `;
        }).join('');

    if (recentItems) {
        recentList.innerHTML = recentItems;
    } else {
        console.log('No valid analyses to display');
        recentList.innerHTML = '<div class="no-data">No valid analyses</div>';
    }
}

function updateDiseaseChart(analyses) {
    const chartContainer = document.getElementById('diseaseChart');
    
    if (!analyses || analyses.length === 0) {
        chartContainer.innerHTML = '<div class="no-data">No analysis data available yet</div>';
        return;
    }

    // Count diseases (filter out invalid results)
    const diseaseCounts = {};
    analyses.forEach(analysis => {
        if (analysis.result && analysis.result.predicted_class) {
            const disease = analysis.result.predicted_class;
            diseaseCounts[disease] = (diseaseCounts[disease] || 0) + 1;
        }
    });

    // Create simple chart
    const chartHTML = Object.entries(diseaseCounts)
        .map(([disease, count]) => {
            const percentage = (count / analyses.length * 100).toFixed(1);
            return `
                <div class="chart-item">
                    <div class="chart-bar">
                        <div class="chart-fill" style="width: ${percentage}%"></div>
                    </div>
                    <div class="chart-label">
                        <span>${disease}</span>
                        <span>${count} (${percentage}%)</span>
                    </div>
                </div>
            `;
        }).join('');

    chartContainer.innerHTML = chartHTML;
}

function updateTimelineChart(analyses) {
    const timelineContainer = document.getElementById('timelineChart');
    
    if (!analyses || analyses.length === 0) {
        timelineContainer.innerHTML = '<div class="no-data">No timeline data available</div>';
        return;
    }

    // Filter valid analyses
    const validAnalyses = analyses.filter(a => a.result && a.result.predicted_class && a.created_at);
    
    if (validAnalyses.length === 0) {
        timelineContainer.innerHTML = '<div class="no-data">No timeline data available</div>';
        return;
    }

    // Group analyses by date
    const analysesByDate = {};
    validAnalyses.forEach(analysis => {
        const date = new Date(analysis.created_at).toLocaleDateString();
        if (!analysesByDate[date]) {
            analysesByDate[date] = [];
        }
        analysesByDate[date].push(analysis);
    });

    // Sort dates
    const sortedDates = Object.keys(analysesByDate).sort((a, b) => {
        return new Date(a) - new Date(b);
    });

    // Create timeline HTML
    const timelineHTML = sortedDates.map(date => {
        const dayAnalyses = analysesByDate[date];
        const count = dayAnalyses.length;
        
        // Count positive results for this day
        const positiveCount = dayAnalyses.filter(a => {
            const className = a.result.predicted_class.toLowerCase();
            return className.includes('babesia') || 
                   className.includes('leishmania') || 
                   className.includes('trypanosome') || 
                   className.includes('malaria parasitized');
        }).length;
        
        const diseases = dayAnalyses.map(a => a.result.predicted_class).join(', ');
        
        return `
            <div class="timeline-item">
                <div class="timeline-date">${date}</div>
                <div class="timeline-content">
                    <div class="timeline-count">${count} analysis${count > 1 ? 'es' : ''}</div>
                    ${positiveCount > 0 ? `<div class="timeline-positive">${positiveCount} positive result${positiveCount > 1 ? 's' : ''}</div>` : ''}
                    <div class="timeline-diseases">${diseases}</div>
                </div>
            </div>
        `;
    }).join('');

    timelineContainer.innerHTML = timelineHTML;
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
