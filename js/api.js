const API_BASE_URL = 'http://localhost:5001/api';

const authAPI = {
    async register(userData) {
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });
        return await response.json();
    },

    async login(credentials) {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(credentials)
        });
        return await response.json();
    }
};

const analysisAPI = {
    async analyzeImage(imageData, userId, notes = '') {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: imageData,
                user_id: userId,
                notes: notes
            })
        });
        return await response.json();
    },

    async getResults(userId) {
        const response = await fetch(`${API_BASE_URL}/results?user_id=${userId}`);
        return await response.json();
    },

    async getUserStats(userId) {
        const response = await fetch(`${API_BASE_URL}/stats/${userId}`);
        return await response.json();
    },

    async deleteResult(resultId) {
        const response = await fetch(`${API_BASE_URL}/results/${resultId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        return await response.json();
    }
};

function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });
}

export { authAPI, analysisAPI, fileToBase64 };
