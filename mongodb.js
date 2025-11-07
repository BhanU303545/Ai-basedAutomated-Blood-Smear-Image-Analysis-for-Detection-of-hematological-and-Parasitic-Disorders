// MongoDB Configuration (Authenticated)
const MONGODB_URI = 'mongodb://bhanu:bhanu123@localhost:27017/bloodsmear?authSource=admin';
const DB_NAME = 'bloodsmear';

// Helper function to check if user is authenticated
function checkAuth() {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user) {
        window.location.href = '/';
        return null;
    }
    return user;
}

// Helper function to get user profile
function getUserProfile() {
    const user = JSON.parse(localStorage.getItem('user'));
    return user;
}

export { checkAuth, getUserProfile, MONGODB_URI, DB_NAME };
