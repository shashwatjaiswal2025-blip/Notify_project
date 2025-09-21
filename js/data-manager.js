/**
 * Notifly Data Manager
 * Handles form submissions, local storage, and API communication
 */

class NotiflyDataManager {
    constructor() {
        this.apiBase = 'http://localhost:5000/api';
        this.localStorageKey = 'notifly_submissions';
        this.init();
    }

    init() {
        console.log('Notifly Data Manager initialized');
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Auto-submit stored data when online
        window.addEventListener('online', () => {
            this.syncStoredSubmissions();
        });
    }

    /**
     * Submit form data to backend
     */
    async submitNews(formData) {
        try {
            // Try API submission first
            const response = await this.submitToAPI(formData);
            if (response.success) {
                return response;
            }
        } catch (error) {
            console.warn('API submission failed, storing locally:', error);
        }

        // Fallback to local storage
        return this.storeLocally(formData);
    }

    /**
     * Submit to API endpoint
     */
    async submitToAPI(formData) {
        const endpoints = [
            `${this.apiBase}/submit-news`,
            '/api/submit-news',
            '/submit'
        ];

        for (const endpoint of endpoints) {
            try {
                const response = await fetch(endpoint, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                if (response.ok) {
                    const result = await response.json();
                    console.log('API submission successful:', result);
                    return result;
                }
            } catch (error) {
                console.warn(`Failed to submit to ${endpoint}:`, error);
                continue;
            }
        }

        throw new Error('All API endpoints failed');
    }

    /**
     * Store submission locally
     */
    storeLocally(formData) {
        try {
            const data = this.formDataToObject(formData);
            data.id = Date.now();
            data.stored_locally = true;
            data.submitted_at = new Date().toISOString();

            const stored = this.getStoredSubmissions();
            stored.push(data);
            localStorage.setItem(this.localStorageKey, JSON.stringify(stored));

            console.log('Data stored locally:', data);
            return {
                success: true,
                message: 'Stored locally - will sync when server is available',
                id: data.id,
                stored_locally: true
            };
        } catch (error) {
            throw new Error(`Local storage failed: ${error.message}`);
        }
    }

    /**
     * Convert FormData to plain object
     */
    formDataToObject(formData) {
        const obj = {};
        for (let [key, value] of formData.entries()) {
            obj[key] = value;
        }
        return obj;
    }

    /**
     * Get stored submissions from localStorage
     */
    getStoredSubmissions() {
        try {
            return JSON.parse(localStorage.getItem(this.localStorageKey) || '[]');
        } catch (error) {
            console.error('Error reading stored submissions:', error);
            return [];
        }
    }

    /**
     * Sync stored submissions to server
     */
    async syncStoredSubmissions() {
        const stored = this.getStoredSubmissions();
        const localSubmissions = stored.filter(item => item.stored_locally);

        if (localSubmissions.length === 0) {
            return;
        }

        console.log(`Syncing ${localSubmissions.length} local submissions...`);

        for (const submission of localSubmissions) {
            try {
                const formData = new FormData();
                Object.keys(submission).forEach(key => {
                    if (key !== 'id' && key !== 'stored_locally') {
                        formData.append(key, submission[key]);
                    }
                });

                const result = await this.submitToAPI(formData);
                if (result.success) {
                    // Remove from local storage
                    this.removeStoredSubmission(submission.id);
                    console.log('Synced submission:', submission.title);
                }
            } catch (error) {
                console.error('Failed to sync submission:', error);
            }
        }
    }

    /**
     * Remove a submission from local storage
     */
    removeStoredSubmission(id) {
        const stored = this.getStoredSubmissions();
        const filtered = stored.filter(item => item.id !== id);
        localStorage.setItem(this.localStorageKey, JSON.stringify(filtered));
    }

    /**
     * Get all submissions (local + remote)
     */
    async getAllSubmissions() {
        let remoteSubmissions = [];
        
        try {
            const response = await fetch(`${this.apiBase}/submissions`);
            if (response.ok) {
                const result = await response.json();
                remoteSubmissions = result.submissions || [];
            }
        } catch (error) {
            console.warn('Failed to fetch remote submissions:', error);
        }

        const localSubmissions = this.getStoredSubmissions();
        
        return {
            remote: remoteSubmissions,
            local: localSubmissions,
            total: remoteSubmissions.length + localSubmissions.length
        };
    }

    /**
     * Clear all local data (for testing)
     */
    clearLocalData() {
        localStorage.removeItem(this.localStorageKey);
        console.log('Local data cleared');
    }
}

// Initialize global instance
window.notiflyDataManager = new NotiflyDataManager();

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NotiflyDataManager;
}
