/**
 * ImageShare Upload UI - Main Application
 * Vanilla JavaScript ES2021+ with no external dependencies
 */

// API Service - handles photo upload to backend
const BASE_URL = ''; // Empty for relative URLs

const ApiService = {
    /**
     * Upload photo to backend API
     * @param {File} photoFile - The photo file to upload
     * @returns {Promise<Object>} Upload response data
     * @throws {Error} If upload fails
     */
    async uploadPhoto(photoFile) {
        const formData = new FormData();
        formData.append('photo', photoFile);

        try {
            const response = await fetch(`${BASE_URL}/api/upload`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                // Parse error response from FastAPI
                const errorData = await response.json().catch(() => ({
                    detail: 'Unknown error occurred'
                }));

                // Handle both FastAPI formats: {detail: ""} and custom {error: ""}
                const errorMessage = errorData.detail || errorData.error || 'Failed to upload photo';
                throw new Error(errorMessage);
            }

            return await response.json();
        } catch (error) {
            // Network errors or fetch failures
            if (error.message.includes('Failed to fetch')) {
                throw new Error('Network error. Please check your connection and try again.');
            }
            throw error;
        }
    }
};

// Uploader Component - main upload logic
class Uploader {
    constructor() {
        // DOM elements
        this.form = document.getElementById('uploadForm');
        this.fileInput = document.getElementById('photoInput');
        this.uploadButton = document.querySelector('.upload-button');
        this.thumbnailContainer = document.getElementById('thumbnailContainer');
        this.thumbnailImage = document.getElementById('thumbnailImage');
        this.submitButton = document.getElementById('submitButton');
        this.loadingIndicator = document.getElementById('loadingIndicator');
        this.statusMessage = document.getElementById('statusMessage');
        this.uploadAnotherButton = document.getElementById('uploadAnotherButton');

        // State
        this.selectedFile = null;

        // Initialize
        this.attachEventListeners();
    }

    attachEventListeners() {
        // File input change
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));

        // Form submit
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));

        // Upload another button
        this.uploadAnotherButton.addEventListener('click', () => this.resetForm());

        // Keyboard accessibility for upload button label
        this.uploadButton.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.fileInput.click();
            }
        });
    }

    /**
     * Handle file selection from input
     */
    handleFileSelect(event) {
        const file = event.target.files[0];
        if (!file) return;

        this.selectedFile = file;

        // Generate and display thumbnail preview
        this.displayThumbnail(file);

        // Show submit button
        this.submitButton.hidden = false;

        // Clear any previous status messages
        this.clearStatus();
    }

    /**
     * Display thumbnail preview of selected photo
     */
    displayThumbnail(file) {
        const reader = new FileReader();

        reader.onload = (e) => {
            this.thumbnailImage.src = e.target.result;
            this.thumbnailContainer.hidden = false;
        };

        reader.onerror = () => {
            this.showError('Failed to read file. Please try again.');
        };

        reader.readAsDataURL(file);
    }

    /**
     * Handle form submission
     */
    async handleSubmit(event) {
        event.preventDefault();

        if (!this.selectedFile) {
            this.showError('Please select a photo first.');
            return;
        }

        // Show loading state
        this.setLoadingState(true);

        try {
            // Upload photo
            const result = await ApiService.uploadPhoto(this.selectedFile);

            // Show success
            this.showSuccess(
                'Photo uploaded! It will appear on the display soon.',
                result
            );

            // Show "Upload Another" button
            this.uploadAnotherButton.hidden = false;

            // Vibrate on success (if supported)
            if (navigator.vibrate) {
                navigator.vibrate(100);
            }
        } catch (error) {
            // Show error with retry option
            this.showError(error.message);

            // Vibrate on error (if supported)
            if (navigator.vibrate) {
                navigator.vibrate([100, 50, 100]);
            }
        } finally {
            // Hide loading state
            this.setLoadingState(false);
        }
    }

    /**
     * Set loading state (disable controls, show spinner)
     */
    setLoadingState(isLoading) {
        this.submitButton.disabled = isLoading;
        this.fileInput.disabled = isLoading;
        this.uploadButton.style.pointerEvents = isLoading ? 'none' : '';
        this.uploadButton.style.opacity = isLoading ? '0.6' : '';
        this.loadingIndicator.hidden = !isLoading;

        // Clear status during loading
        if (isLoading) {
            this.clearStatus();
        }
    }

    /**
     * Show success message
     */
    showSuccess(message, result) {
        this.statusMessage.textContent = message;
        this.statusMessage.className = 'status-message success';

        // Move focus to status message for screen readers
        this.statusMessage.setAttribute('tabindex', '-1');
        this.statusMessage.focus();
    }

    /**
     * Show error message
     */
    showError(message) {
        this.statusMessage.textContent = message;
        this.statusMessage.className = 'status-message error';

        // Move focus to error message for screen readers
        this.statusMessage.setAttribute('tabindex', '-1');
        this.statusMessage.focus();
    }

    /**
     * Clear status message
     */
    clearStatus() {
        this.statusMessage.textContent = '';
        this.statusMessage.className = 'status-message';
    }

    /**
     * Reset form to initial state
     */
    resetForm() {
        // Reset file input
        this.fileInput.value = '';
        this.selectedFile = null;

        // Hide elements
        this.thumbnailContainer.hidden = true;
        this.submitButton.hidden = true;
        this.uploadAnotherButton.hidden = true;

        // Clear thumbnail
        this.thumbnailImage.src = '';

        // Clear status
        this.clearStatus();

        // Re-enable controls
        this.setLoadingState(false);
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const uploader = new Uploader();
    console.log('ImageShare Upload UI initialized');
});
