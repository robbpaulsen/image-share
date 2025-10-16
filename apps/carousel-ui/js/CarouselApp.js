/**
 * Image Share Carousel Application
 *
 * Displays photos from the backend in a continuous auto-advancing loop
 * with smooth crossfade transitions.
 */

// State management
let photos = [];
let currentIndex = 0;
let rotationInterval = null;
let pollingInterval = null;
let noPhotos = true;

// DOM elements
const primaryImage = document.getElementById('image-primary');
const secondaryImage = document.getElementById('image-secondary');
const carouselContainer = document.getElementById('carousel-container');
const noPhotosScreen = document.getElementById('no-photos-screen');
const qrCodeContainer = document.getElementById('qr-code-container');

// Configuration
const config = {
    rotationIntervalMs: 7000, // 7 seconds
    pollingIntervalMs: 10000, // 10 seconds
    apiEndpoint: '/api/photos',
    uploadUrl: 'http://photoshare.local',
};

/**
 * Initialize the carousel application.
 * Fetches photos, starts display, and begins polling.
 */
async function init() {
    console.log('Initializing carousel...');

    // Generate QR code
    generateQRCode();

    try {
        // Initial fetch
        await fetchAndUpdatePhotos();

        // Start polling for new photos
        startPolling();

    } catch (error) {
        console.error('Error initializing carousel:', error);
        showErrorMessage();
    }
}

/**
 * Fetch photos from API and update display.
 */
async function fetchAndUpdatePhotos() {
    try {
        const response = await fetch(config.apiEndpoint);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const fetchedPhotos = await response.json();

        // Detect new photos
        const newPhotos = detectNewPhotos(fetchedPhotos);

        if (newPhotos.length > 0) {
            console.log(`Detected ${newPhotos.length} new photos:`, newPhotos.map(p => p.url));

            // Add new photos to array (sorted chronologically)
            photos = [...photos, ...newPhotos].sort((a, b) =>
                new Date(a.createdAt) - new Date(b.createdAt)
            );

            // Transition from no photos state if needed
            if (noPhotos && photos.length > 0) {
                transitionToCarousel();
            } else if (photos.length > 1 && !rotationInterval) {
                startRotation();
            }
        }

        // Check if all photos were deleted
        if (fetchedPhotos.length === 0 && photos.length > 0) {
            console.log('All photos deleted, returning to instruction screen');
            photos = [];
            transitionToNoPhotos();
        }

        // Initial state: no photos
        if (fetchedPhotos.length === 0 && noPhotos) {
            console.log('No photos available');
            showNoPhotosScreen();
        }

    } catch (error) {
        console.error('Error fetching photos:', error);
        throw error;
    }
}

/**
 * Detect new photos by comparing current and fetched lists.
 *
 * @param {Array} fetchedPhotos - Newly fetched photo list
 * @returns {Array} - Array of new photos
 */
function detectNewPhotos(fetchedPhotos) {
    const existingIds = new Set(photos.map(p => p.id));
    return fetchedPhotos.filter(photo => !existingIds.has(photo.id));
}

/**
 * Start polling for new photos.
 */
function startPolling() {
    console.log(`Starting photo polling (${config.pollingIntervalMs}ms interval)`);

    if (pollingInterval) {
        clearInterval(pollingInterval);
    }

    pollingInterval = setInterval(fetchAndUpdatePhotos, config.pollingIntervalMs);
}

/**
 * Stop polling for photos.
 */
function stopPolling() {
    if (pollingInterval) {
        console.log('Stopping photo polling');
        clearInterval(pollingInterval);
        pollingInterval = null;
    }
}

/**
 * Display a photo at the specified index.
 *
 * @param {number} index - Index of the photo to display
 */
function displayPhoto(index) {
    if (index < 0 || index >= photos.length) {
        console.error(`Invalid photo index: ${index}`);
        return;
    }

    const photo = photos[index];
    console.log(`Displaying photo ${index + 1}/${photos.length}: ${photo.url}`);

    // Set the primary image source (initial load)
    primaryImage.src = photo.url;
    primaryImage.classList.add('visible');
    primaryImage.classList.remove('hidden');

    // Ensure secondary image is hidden initially
    secondaryImage.classList.add('hidden');
    secondaryImage.classList.remove('visible');

    currentIndex = index;
}

/**
 * Transition to the next photo with crossfade effect.
 */
function transitionToNextPhoto() {
    if (photos.length < 2) return;

    // Calculate next index
    const nextIndex = (currentIndex + 1) % photos.length;
    const nextPhoto = photos[nextIndex];

    console.log(`Transitioning to photo ${nextIndex + 1}/${photos.length}`);

    // Determine which image is active and which is inactive
    const activeImage = primaryImage.classList.contains('visible') ? primaryImage : secondaryImage;
    const inactiveImage = activeImage === primaryImage ? secondaryImage : primaryImage;

    // Load the next image into the inactive element
    inactiveImage.src = nextPhoto.url;

    // Once the new image is loaded, perform the crossfade
    inactiveImage.onload = () => {
        inactiveImage.classList.remove('hidden');
        inactiveImage.classList.add('visible');
        activeImage.classList.remove('visible');
        activeImage.classList.add('hidden');
    };

    currentIndex = nextIndex;
}


/**
 * Start automatic photo rotation.
 */
function startRotation() {
    console.log(`Starting automatic rotation (${config.rotationIntervalMs}ms interval)`);

    // Clear any existing interval
    if (rotationInterval) {
        clearInterval(rotationInterval);
    }

    // Set up new interval
    rotationInterval = setInterval(transitionToNextPhoto, config.rotationIntervalMs);
}

/**
 * Stop automatic photo rotation.
 */
function stopRotation() {
    if (rotationInterval) {
        console.log('Stopping automatic rotation');
        clearInterval(rotationInterval);
        rotationInterval = null;
    }
}

/**
 * Show the "No Photos" instruction screen.
 */
function showNoPhotosScreen() {
    noPhotos = true;
    noPhotosScreen.classList.remove('hidden');
    noPhotosScreen.classList.add('visible');
    carouselContainer.style.display = 'none';
}

/**
 * Transition from "No Photos" screen to carousel.
 */
function transitionToCarousel() {
    console.log('Transitioning to carousel mode');
    noPhotos = false;

    // Fade out instruction screen
    noPhotosScreen.classList.remove('visible');
    noPhotosScreen.classList.add('hidden');

    // Show carousel
    carouselContainer.style.display = 'block';

    // Display first photo
    displayPhoto(0);

    // Start rotation if multiple photos
    if (photos.length > 1) {
        startRotation();
    }
}

/**
 * Transition from carousel to "No Photos" screen.
 */
function transitionToNoPhotos() {
    noPhotos = true;

    // Stop rotation
    stopRotation();

    // Hide carousel
    carouselContainer.style.display = 'none';

    // Show instruction screen
    noPhotosScreen.classList.remove('hidden');
    noPhotosScreen.classList.add('visible');
}

/**
 * Generate QR code for upload URL.
 */
function generateQRCode() {
    // Clear existing QR code
    qrCodeContainer.innerHTML = '';

    // Generate new QR code
    new QRCode(qrCodeContainer, {
        text: config.uploadUrl,
        width: 300,
        height: 300,
        colorDark: '#000000',
        colorLight: '#ffffff',
        correctLevel: QRCode.CorrectLevel.H
    });

    console.log('QR code generated for:', config.uploadUrl);
}

/**
 * Display an error message.
 */
function showErrorMessage() {
    console.error('Failed to load photos');
    const container = document.getElementById('carousel-container');
    container.innerHTML = `
        <div style="
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            color: #ff6b6b;
            font-size: 2rem;
            text-align: center;
        ">
            Error loading photos.<br>
            Please check your connection and try again.
        </div>
    `;
}

// Start the application when the page loads
window.addEventListener('DOMContentLoaded', init);

// Clean up intervals on page unload
window.addEventListener('beforeunload', () => {
    stopRotation();
    stopPolling();
});
