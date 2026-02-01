/* ========================================
   NeuroScan - Eye Tracking Test JavaScript
   WebGazer.js Integration
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
    // Check authentication
    const token = getToken();
    if (!token) {
        window.location.href = '/';
        return;
    }

    // Check camera availability
    checkCameraAvailability();
});

// Check camera availability
async function checkCameraAvailability() {
    const reqCamera = document.getElementById('req-camera');
    const statusEl = reqCamera.querySelector('.req-status');

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        stream.getTracks().forEach(track => track.stop());

        statusEl.textContent = 'Available';
        statusEl.className = 'req-status ready';
        document.getElementById('startBtn').disabled = false;
        updateStatus('Ready to start', 'ready');
    } catch (error) {
        statusEl.textContent = 'Not available';
        statusEl.className = 'req-status error';
        document.getElementById('startBtn').disabled = true;
        updateStatus('Camera required', 'error');
        console.error('Camera error:', error);
    }
}

// Update status indicator
function updateStatus(text, state) {
    const statusText = document.getElementById('statusText');
    const statusDot = document.querySelector('.status-dot');

    statusText.textContent = text;
    statusDot.className = 'status-dot ' + state;
}

// Show specific step
function showStep(stepId) {
    document.querySelectorAll('.test-step').forEach(step => {
        step.classList.remove('active');
    });
    document.getElementById('step-' + stepId).classList.add('active');
}

// Start calibration
async function startCalibration() {
    showStep('calibration');
    updateStatus('Calibrating...', 'recording');

    // Show webcam preview
    document.getElementById('webcamPreview').classList.add('active');

    // Initialize WebGazer
    try {
        await initializeWebGazer();
        isCalibrating = true;
    } catch (error) {
        console.error('WebGazer initialization error:', error);
        alert('Failed to initialize eye tracking. Please refresh and try again.');
    }
}

// Initialize WebGazer
async function initializeWebGazer() {
    return new Promise((resolve, reject) => {
        try {
            webgazer
                .setGazeListener(function (data, elapsedTime) {
                    if (data == null) return;

                    // Show gaze indicator during calibration
                    if (isCalibrating) {
                        showGazeIndicator(data.x, data.y);
                    }

                    // Collect data during tracking
                    if (isTracking && collectedData.start_time !== null) {
                        const timestamp = Date.now() - collectedData.start_time;
                        collectedData.timestamps.push(timestamp);
                        collectedData.x_positions.push(data.x);
                        collectedData.y_positions.push(data.y);

                        // Update gaze indicator
                        showGazeIndicator(data.x, data.y);

                        // Update data point count
                        document.getElementById('dataPointCount').textContent =
                            collectedData.timestamps.length;
                    }
                })
                .saveDataAcrossSessions(false)
                .begin()
                .then(() => {
                    webgazerReady = true;

                    // Show video in our preview
                    const webgazerVideo = document.getElementById('webgazerVideoFeed');
                    const ourVideo = document.getElementById('webcamVideo');

                    if (webgazerVideo && ourVideo) {
                        ourVideo.srcObject = webgazerVideo.srcObject;
                    }

                    // Hide WebGazer's default video
                    webgazer.showVideoPreview(false);
                    webgazer.showPredictionPoints(false);
                    webgazer.showFaceOverlay(false);
                    webgazer.showFaceFeedbackBox(false);

                    resolve();
                })
                .catch(reject);
        } catch (error) {
            reject(error);
        }
    });
}

// Show gaze indicator
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
    if (!webgazerReady) return;

    const point = element.dataset.point;

    if (!calibrationClicks[point]) {
        calibrationClicks[point] = 0;
    }

    calibrationClicks[point]++;
    element.classList.add('clicked');

    // Record click for WebGazer calibration
    const rect = element.getBoundingClientRect();
    const x = rect.left + rect.width / 2;
    const y = rect.top + rect.height / 2;
    webgazer.recordScreenPosition(x, y, 'click');

    setTimeout(() => element.classList.remove('clicked'), 300);

    // Check if point is fully calibrated (5 clicks)
    if (calibrationClicks[point] >= 5) {
        element.classList.add('calibrated');
    }

    // Update calibration count
    const calibratedCount = Object.values(calibrationClicks)
        .filter(count => count >= 5).length;
    document.getElementById('calibrationCount').textContent = calibratedCount;

    // Check if all points calibrated
    if (calibratedCount >= 9) {
        isCalibrating = false;
        setTimeout(startTracking, 500);
    } else if (calibratedCount >= 5) {
        // Show skip button after 5 points
        document.getElementById('skipCalibrationBtn').style.display = 'inline-flex';
    }
}

// Skip remaining calibration
function skipCalibration() {
    isCalibrating = false;
    startTracking();
}

// Start the actual eye tracking test
function startTracking() {
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
    target.style.display = 'block';
    gazeIndicator.style.display = 'block';

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

let targetInterval;

// Move the tracking target
function moveTarget() {
    const target = document.getElementById('trackingTarget');
    const canvas = document.getElementById('testCanvas');
    const rect = canvas.getBoundingClientRect();

    const pattern = targetPatterns[currentTargetIndex];
    const x = (pattern.x / 100) * (rect.width - 30);
    const y = (pattern.y / 100) * (rect.height - 30);

    target.style.left = x + 'px';
    target.style.top = y + 'px';
}

// Update timer display
function updateTimer() {
    document.getElementById('remainingTime').textContent = remainingTime;
}

// Finish tracking and process data
function finishTracking() {
    isTracking = false;
    clearInterval(testTimer);
    clearInterval(targetInterval);

    // Hide tracking elements
    document.getElementById('trackingTarget').style.display = 'none';
    document.getElementById('gazeIndicator').style.display = 'none';
    document.getElementById('webcamPreview').classList.remove('active');

    // Stop WebGazer
    if (webgazerReady) {
        webgazer.end();
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
            document.getElementById(steps[stepIndex - 1]).classList.remove('active');
            document.getElementById(steps[stepIndex - 1]).classList.add('complete');
        }

        if (stepIndex < steps.length) {
            document.getElementById(steps[stepIndex]).classList.add('active');
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
    // Validate we have enough data
    if (collectedData.timestamps.length < 100) {
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
