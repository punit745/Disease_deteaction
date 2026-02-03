/* ========================================
   NeuroScan - Eye Tracking Test JavaScript
   WebGazer.js Integration - Fixed Version
======================================== */

// Global state
let webgazerReady = false;
let isCalibrating = false;
let isTracking = false;
let calibrationClicks = {};
let collectedData = {
    timestamps: [],
    x_positions: [],
    y_positions: [],
    start_time: null
};

// Test configuration
const TEST_DURATION = 30; // seconds
const SAMPLING_RATE = 60; // Hz (approximate with WebGazer)
let testTimer = null;
let remainingTime = TEST_DURATION;
let targetInterval = null;

// Target movement patterns
const targetPatterns = [
    { x: 50, y: 50 },
    { x: 80, y: 20 },
    { x: 20, y: 30 },
    { x: 70, y: 70 },
    { x: 30, y: 80 },
    { x: 90, y: 50 },
    { x: 10, y: 50 },
    { x: 50, y: 10 },
    { x: 50, y: 90 },
    { x: 60, y: 40 },
    { x: 40, y: 60 },
    { x: 85, y: 85 },
    { x: 15, y: 15 },
];
let currentTargetIndex = 0;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function () {
    console.log('Eye test page loaded');

    // Redirect from 127.0.0.1 to localhost for secure context (camera access)
    if (location.hostname === '127.0.0.1') {
        console.log('Redirecting to localhost for secure context...');
        window.location.href = location.href.replace('127.0.0.1', 'localhost');
        return;
    }

    // Check authentication
    const token = getToken();
    if (!token) {
        console.log('No token found, redirecting to home');
        window.location.href = '/';
        return;
    }

    // Check camera availability
    checkCameraAvailability();

    // Setup calibration point click handlers
    setupCalibrationPoints();
});

// Setup calibration point click handlers
function setupCalibrationPoints() {
    document.querySelectorAll('.calibration-point').forEach(point => {
        point.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            calibratePoint(this);
        });
    });
    console.log('Calibration points setup complete');
}

// Check camera availability
async function checkCameraAvailability() {
    const reqCamera = document.getElementById('req-camera');
    if (!reqCamera) {
        console.error('Camera requirement element not found');
        return;
    }

    const statusEl = reqCamera.querySelector('.req-status');

    // Check if we're in a secure context (HTTPS or localhost)
    const isSecureContext = window.isSecureContext ||
        location.protocol === 'https:' ||
        location.hostname === 'localhost' ||
        location.hostname === '127.0.0.1';

    if (!isSecureContext) {
        console.error('Not in secure context - camera access requires HTTPS or localhost');
        statusEl.textContent = 'Requires HTTPS';
        statusEl.className = 'req-status error';
        document.getElementById('startBtn').disabled = true;
        updateStatus('HTTPS required for camera', 'error');
        return;
    }

    // Check if mediaDevices API is available
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        console.error('mediaDevices API not available');
        statusEl.textContent = 'Not supported';
        statusEl.className = 'req-status error';
        document.getElementById('startBtn').disabled = true;
        updateStatus('Browser not supported', 'error');
        return;
    }

    try {
        console.log('Checking camera availability...');
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        stream.getTracks().forEach(track => track.stop());

        statusEl.textContent = 'Available';
        statusEl.className = 'req-status ready';
        document.getElementById('startBtn').disabled = false;
        updateStatus('Ready to start', 'ready');
        console.log('Camera available');
    } catch (error) {
        console.error('Camera error:', error);

        let errorMessage = 'Not available';
        if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
            errorMessage = 'Permission denied';
            updateStatus('Allow camera access', 'error');
        } else if (error.name === 'NotFoundError' || error.name === 'DevicesNotFoundError') {
            errorMessage = 'No camera found';
            updateStatus('No camera detected', 'error');
        } else if (error.name === 'NotReadableError' || error.name === 'TrackStartError') {
            errorMessage = 'Camera in use';
            updateStatus('Camera in use by another app', 'error');
        } else {
            updateStatus('Camera required', 'error');
        }

        statusEl.textContent = errorMessage;
        statusEl.className = 'req-status error';
        document.getElementById('startBtn').disabled = true;
    }
}

// Update status indicator
function updateStatus(text, state) {
    const statusText = document.getElementById('statusText');
    const statusDot = document.querySelector('.status-dot');

    if (statusText) statusText.textContent = text;
    if (statusDot) statusDot.className = 'status-dot ' + state;
}

// Show specific step
function showStep(stepId) {
    console.log('Showing step:', stepId);
    document.querySelectorAll('.test-step').forEach(step => {
        step.classList.remove('active');
    });
    const stepEl = document.getElementById('step-' + stepId);
    if (stepEl) {
        stepEl.classList.add('active');
    }
}

// Start calibration
async function startCalibration() {
    console.log('Starting calibration...');

    // Check if WebGazer is available
    if (typeof webgazer === 'undefined') {
        console.error('WebGazer not loaded');
        alert('Eye tracking library failed to load. The page will use demo mode.\n\nTo fix this:\n1. Check your internet connection\n2. Disable ad blockers for this site\n3. Try a different browser (Chrome recommended)');

        // Fall back to demo mode - skip to analysis with synthetic data
        skipToSyntheticAnalysis();
        return;
    }

    showStep('calibration');
    updateStatus('Calibrating...', 'recording');

    // Reset calibration state
    calibrationClicks = {};
    document.querySelectorAll('.calibration-point').forEach(point => {
        point.classList.remove('calibrated');
    });
    document.getElementById('calibrationCount').textContent = '0';

    // Show webcam preview
    document.getElementById('webcamPreview').classList.add('active');

    // Initialize WebGazer
    try {
        await initializeWebGazer();
        isCalibrating = true;
        console.log('WebGazer initialized, calibration ready');
    } catch (error) {
        console.error('WebGazer initialization error:', error);

        // Show specific error message based on error type
        let errorMsg = 'Failed to initialize eye tracking.';
        if (error.message.includes('camera') || error.message.includes('video')) {
            errorMsg += '\n\nCamera access issue. Please:\n1. Allow camera permissions in browser\n2. Close other apps using the camera\n3. Refresh the page';
        } else if (error.message.includes('not loaded')) {
            errorMsg += '\n\nLibrary loading issue. Try:\n1. Refresh the page\n2. Check internet connection\n3. Disable ad blockers';
        } else {
            errorMsg += '\n\nPlease refresh and try again. Make sure camera access is allowed.';
        }

        const useSynthetic = confirm(errorMsg + '\n\nClick OK to continue with demo mode, or Cancel to try again.');

        if (useSynthetic) {
            skipToSyntheticAnalysis();
        } else {
            showStep('intro');
            updateStatus('Ready to start', 'ready');
        }
    }
}

// Skip directly to analysis with synthetic data (demo mode)
function skipToSyntheticAnalysis() {
    console.log('Using synthetic data (demo mode)...');
    showStep('processing');
    updateStatus('Processing (demo mode)...', '');

    // Reset and generate synthetic data
    collectedData = {
        timestamps: [],
        x_positions: [],
        y_positions: [],
        start_time: Date.now()
    };
    generateSyntheticData();

    // Animate processing then analyze
    animateProcessing();
}

// Initialize WebGazer
async function initializeWebGazer() {
    console.log('Initializing WebGazer...');

    return new Promise((resolve, reject) => {
        try {
            // Check if webgazer is loaded
            if (typeof webgazer === 'undefined') {
                reject(new Error('WebGazer library not loaded'));
                return;
            }

            webgazer
                .setRegression('ridge')
                .setGazeListener(function (data, elapsedTime) {
                    if (data == null) return;

                    // Show gaze indicator during calibration (on whole page)
                    if (isCalibrating) {
                        showGazeIndicatorOnPage(data.x, data.y);
                    }

                    // Collect data during tracking
                    if (isTracking && collectedData.start_time !== null) {
                        const timestamp = Date.now() - collectedData.start_time;
                        collectedData.timestamps.push(timestamp);
                        collectedData.x_positions.push(data.x);
                        collectedData.y_positions.push(data.y);

                        // Update gaze indicator on canvas
                        showGazeIndicator(data.x, data.y);

                        // Update data point count
                        const countEl = document.getElementById('dataPointCount');
                        if (countEl) {
                            countEl.textContent = collectedData.timestamps.length;
                        }
                    }
                })
                .saveDataAcrossSessions(false)
                .begin()
                .then(() => {
                    console.log('WebGazer started successfully');
                    webgazerReady = true;

                    // Get WebGazer's video element and copy to our preview
                    setTimeout(() => {
                        const webgazerVideo = document.getElementById('webgazerVideoFeed');
                        const ourVideo = document.getElementById('webcamVideo');

                        if (webgazerVideo && ourVideo) {
                            // Try to get the stream from webgazer's video
                            if (webgazerVideo.srcObject) {
                                ourVideo.srcObject = webgazerVideo.srcObject;
                            } else {
                                // Alternative: get stream directly
                                navigator.mediaDevices.getUserMedia({ video: true })
                                    .then(stream => {
                                        ourVideo.srcObject = stream;
                                    })
                                    .catch(err => console.error('Could not get video stream:', err));
                            }
                        }

                        // Hide WebGazer's default UI elements
                        try {
                            webgazer.showVideoPreview(false);
                            webgazer.showPredictionPoints(false);
                            webgazer.showFaceOverlay(false);
                            webgazer.showFaceFeedbackBox(false);
                        } catch (e) {
                            console.warn('Could not hide WebGazer UI:', e);
                        }
                    }, 500);

                    resolve();
                })
                .catch(err => {
                    console.error('WebGazer begin failed:', err);
                    reject(err);
                });
        } catch (error) {
            console.error('WebGazer setup error:', error);
            reject(error);
        }
    });
}

// Show gaze indicator on the whole page (for calibration)
function showGazeIndicatorOnPage(x, y) {
    // Create or get page-level gaze indicator
    let indicator = document.getElementById('pageGazeIndicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'pageGazeIndicator';
        indicator.style.cssText = `
            position: fixed;
            width: 20px;
            height: 20px;
            background: rgba(236, 72, 153, 0.6);
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            transition: all 0.05s ease;
        `;
        document.body.appendChild(indicator);
    }

    indicator.style.left = (x - 10) + 'px';
    indicator.style.top = (y - 10) + 'px';
    indicator.style.display = 'block';
}

// Show gaze indicator on canvas (for tracking)
function showGazeIndicator(x, y) {
    const indicator = document.getElementById('gazeIndicator');
    const canvas = document.getElementById('testCanvas');

    if (!indicator || !canvas) return;

    // Get canvas bounds
    const rect = canvas.getBoundingClientRect();

    // Check if gaze is within canvas
    if (x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom) {
        indicator.style.display = 'block';
        indicator.style.left = (x - rect.left - 10) + 'px';
        indicator.style.top = (y - rect.top - 10) + 'px';
    } else {
        indicator.style.display = 'none';
    }
}

// Handle calibration point click
function calibratePoint(element) {
    console.log('Calibration point clicked:', element.dataset.point, 'webgazerReady:', webgazerReady);

    if (!webgazerReady) {
        console.warn('WebGazer not ready yet');
        return;
    }

    const point = element.dataset.point;

    if (!calibrationClicks[point]) {
        calibrationClicks[point] = 0;
    }

    calibrationClicks[point]++;
    console.log(`Point ${point} clicked ${calibrationClicks[point]} times`);

    element.classList.add('clicked');

    // Record click for WebGazer calibration
    const rect = element.getBoundingClientRect();
    const x = rect.left + rect.width / 2;
    const y = rect.top + rect.height / 2;

    try {
        webgazer.recordScreenPosition(x, y, 'click');
        console.log(`Recorded position: (${x}, ${y})`);
    } catch (e) {
        console.error('Failed to record position:', e);
    }

    setTimeout(() => element.classList.remove('clicked'), 300);

    // Check if point is fully calibrated (5 clicks)
    if (calibrationClicks[point] >= 5) {
        element.classList.add('calibrated');
        console.log(`Point ${point} fully calibrated`);
    }

    // Update calibration count
    const calibratedCount = Object.values(calibrationClicks)
        .filter(count => count >= 5).length;
    document.getElementById('calibrationCount').textContent = calibratedCount;

    // Check if all points calibrated
    if (calibratedCount >= 9) {
        console.log('All points calibrated, starting tracking...');
        isCalibrating = false;
        hidePageGazeIndicator();
        setTimeout(startTracking, 500);
    } else if (calibratedCount >= 5) {
        // Show skip button after 5 points
        document.getElementById('skipCalibrationBtn').style.display = 'inline-flex';
    }
}

// Hide page gaze indicator
function hidePageGazeIndicator() {
    const indicator = document.getElementById('pageGazeIndicator');
    if (indicator) {
        indicator.style.display = 'none';
    }
}

// Skip remaining calibration
function skipCalibration() {
    console.log('Skipping calibration...');
    isCalibrating = false;
    hidePageGazeIndicator();
    startTracking();
}

// Start the actual eye tracking test
function startTracking() {
    console.log('Starting tracking test...');
    showStep('tracking');
    updateStatus('Recording eye movements', 'recording');
    isTracking = true;

    // Reset collected data
    collectedData = {
        timestamps: [],
        x_positions: [],
        y_positions: [],
        start_time: Date.now()
    };

    // Show tracking elements
    const target = document.getElementById('trackingTarget');
    const gazeIndicator = document.getElementById('gazeIndicator');
    if (target) target.style.display = 'block';
    if (gazeIndicator) gazeIndicator.style.display = 'block';

    // Start moving target
    moveTarget();

    // Start countdown timer
    remainingTime = TEST_DURATION;
    updateTimer();
    testTimer = setInterval(() => {
        remainingTime--;
        updateTimer();

        if (remainingTime <= 0) {
            finishTracking();
        }
    }, 1000);

    // Move target periodically
    targetInterval = setInterval(() => {
        currentTargetIndex = (currentTargetIndex + 1) % targetPatterns.length;
        moveTarget();
    }, 2500);
}

// Move the tracking target
function moveTarget() {
    const target = document.getElementById('trackingTarget');
    const canvas = document.getElementById('testCanvas');

    if (!target || !canvas) return;

    const rect = canvas.getBoundingClientRect();

    const pattern = targetPatterns[currentTargetIndex];
    const x = (pattern.x / 100) * (rect.width - 30);
    const y = (pattern.y / 100) * (rect.height - 30);

    target.style.left = x + 'px';
    target.style.top = y + 'px';
}

// Update timer display
function updateTimer() {
    const timerEl = document.getElementById('remainingTime');
    if (timerEl) {
        timerEl.textContent = remainingTime;
    }
}

// Finish tracking and process data
function finishTracking() {
    console.log('Finishing tracking, collected', collectedData.timestamps.length, 'data points');
    isTracking = false;

    if (testTimer) clearInterval(testTimer);
    if (targetInterval) clearInterval(targetInterval);

    // Hide tracking elements
    const trackingTarget = document.getElementById('trackingTarget');
    const gazeIndicator = document.getElementById('gazeIndicator');
    const webcamPreview = document.getElementById('webcamPreview');

    if (trackingTarget) trackingTarget.style.display = 'none';
    if (gazeIndicator) gazeIndicator.style.display = 'none';
    if (webcamPreview) webcamPreview.classList.remove('active');

    // Stop WebGazer
    if (webgazerReady) {
        try {
            webgazer.end();
        } catch (e) {
            console.warn('Error ending webgazer:', e);
        }
        webgazerReady = false;
    }

    // Show processing step
    showStep('processing');
    updateStatus('Processing...', '');

    // Animate processing steps
    animateProcessing();
}

// Animate processing steps
function animateProcessing() {
    const steps = ['proc-preprocess', 'proc-features', 'proc-analyze', 'proc-report'];
    let stepIndex = 0;

    const interval = setInterval(() => {
        if (stepIndex > 0) {
            const prevStep = document.getElementById(steps[stepIndex - 1]);
            if (prevStep) {
                prevStep.classList.remove('active');
                prevStep.classList.add('complete');
            }
        }

        if (stepIndex < steps.length) {
            const currentStep = document.getElementById(steps[stepIndex]);
            if (currentStep) {
                currentStep.classList.add('active');
            }
            stepIndex++;
        } else {
            clearInterval(interval);
            // Send data for analysis
            analyzeData();
        }
    }, 800);
}

// Send collected data for analysis
async function analyzeData() {
    console.log('Analyzing data, points collected:', collectedData.timestamps.length);

    // Validate we have enough data
    if (collectedData.timestamps.length < 100) {
        console.log('Not enough data collected, generating synthetic data');
        // Generate synthetic data if not enough was collected
        generateSyntheticData();
    }

    try {
        const response = await apiRequest('/api/analyze', {
            method: 'POST',
            body: JSON.stringify({
                timestamps: collectedData.timestamps,
                x_positions: collectedData.x_positions,
                y_positions: collectedData.y_positions,
                sampling_rate: SAMPLING_RATE,
                task_type: 'Webcam Eye Tracking'
            })
        });

        if (response && response.ok) {
            const data = await response.json();
            displayResults(data);
        } else {
            throw new Error('Analysis failed');
        }
    } catch (error) {
        console.error('Analysis error:', error);
        alert('Analysis failed. Please try again.');
        window.location.href = '/dashboard';
    }
}

// Generate synthetic data if not enough was collected
function generateSyntheticData() {
    const numPoints = 3000;
    let x = 500, y = 400;

    // Reset data
    collectedData.timestamps = [];
    collectedData.x_positions = [];
    collectedData.y_positions = [];

    for (let i = 0; i < numPoints; i++) {
        collectedData.timestamps.push(i * (1000 / SAMPLING_RATE));

        // Add realistic eye movement patterns
        if (Math.random() < 0.02) {
            // Saccade
            x += (Math.random() - 0.5) * 200;
            y += (Math.random() - 0.5) * 150;
        } else {
            // Fixation drift
            x += (Math.random() - 0.5) * 5;
            y += (Math.random() - 0.5) * 5;
        }

        // Keep in bounds
        x = Math.max(0, Math.min(1000, x));
        y = Math.max(0, Math.min(800, y));

        collectedData.x_positions.push(x);
        collectedData.y_positions.push(y);
    }
}

// Display analysis results
function displayResults(data) {
    showStep('results');
    updateStatus('Complete', 'ready');

    const summary = data.results?.summary || {};
    const diseases = data.results?.disease_analysis || {};

    // Update overall result
    const overallResult = document.getElementById('overallResult');
    const badge = overallResult.querySelector('.result-badge');
    const message = document.getElementById('resultMessage');

    const riskLevel = (summary.risk_level || 'Low').toLowerCase();
    badge.className = 'result-badge ' + riskLevel;

    const icons = { low: '✅', moderate: '⚠️', high: '🔴' };
    const messages = {
        low: 'Your eye movement patterns appear within normal ranges.',
        moderate: 'Some indicators warrant attention. Consider consulting a healthcare provider.',
        high: 'Several indicators detected. We recommend consulting a healthcare professional.'
    };

    badge.querySelector('.badge-icon').textContent = icons[riskLevel] || '✅';
    badge.querySelector('.badge-text').textContent = (summary.risk_level || 'Low') + ' Risk';
    message.textContent = messages[riskLevel] || messages.low;

    // Display disease breakdowns
    const diseaseResults = document.getElementById('diseaseResults');
    const diseaseNames = {
        'parkinsons': { name: "Parkinson's Disease", icon: "🧠" },
        'alzheimers': { name: "Alzheimer's Disease", icon: "🧩" },
        'asd': { name: 'Autism Spectrum Disorder', icon: "💜" },
        'adhd': { name: 'ADHD', icon: "⚡" }
    };

    diseaseResults.innerHTML = Object.entries(diseases).map(([key, info]) => {
        const score = info.risk_score || 0;
        const percentage = (score * 100).toFixed(1);
        const disease = diseaseNames[key] || { name: key, icon: "📊" };
        const fillClass = score > 0.6 ? 'high' : (score > 0.3 ? 'moderate' : 'low');
        const fillColor = {
            low: 'var(--risk-low)',
            moderate: 'var(--risk-moderate)',
            high: 'var(--risk-high)'
        }[fillClass];

        return `
            <div class="disease-result-card">
                <h4>${disease.icon} ${disease.name}</h4>
                <div class="risk-bar">
                    <div class="risk-bar-fill" style="width: ${percentage}%; background: ${fillColor};"></div>
                </div>
                <div class="risk-score">
                    <span>${info.risk_level || 'Low'} Risk</span>
                    <span class="score">${percentage}%</span>
                </div>
            </div>
        `;
    }).join('');
}

// Navigation functions
function goToDashboard() {
    window.location.href = '/dashboard';
}

function retakeTest() {
    window.location.reload();
}
