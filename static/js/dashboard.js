/* ========================================
   NeuroScan - Dashboard JavaScript
======================================== */

let selectedTestType = 'webcam';

// Initialize dashboard on load
document.addEventListener('DOMContentLoaded', function () {
    const token = getToken();
    const user = getUser();

    if (!token || !user) {
        window.location.href = '/';
        return;
    }

    // Set user name
    document.getElementById('userName').textContent = user.first_name;

    // Load initial data
    loadDashboardData();

    // Setup navigation
    setupNavigation();
});

function setupNavigation() {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', function (e) {
            e.preventDefault();
            const section = this.dataset.section;
            showSection(section);
        });
    });
}

function showSection(sectionId) {
    // Update navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.toggle('active', item.dataset.section === sectionId);
    });

    // Update sections
    document.querySelectorAll('.dashboard-section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(`${sectionId}-section`).classList.add('active');

    // Update header title
    const titles = {
        'overview': 'Overview',
        'new-test': 'New Test',
        'history': 'Test History',
        'progress': 'Progress Tracking',
        'profile': 'Profile'
    };
    document.getElementById('page-title').textContent = titles[sectionId] || 'Dashboard';

    // Load section-specific data
    if (sectionId === 'history') {
        loadTestHistory();
    } else if (sectionId === 'profile') {
        loadProfile();
    } else if (sectionId === 'progress') {
        loadProgressData();
    }
}

async function loadDashboardData() {
    try {
        // Load statistics
        const statsResponse = await apiRequest('/api/statistics');
        if (statsResponse && statsResponse.ok) {
            const data = await statsResponse.json();
            updateStats(data.statistics);
        }

        // Load recent results
        const resultsResponse = await apiRequest('/api/results?per_page=5');
        if (resultsResponse && resultsResponse.ok) {
            const data = await resultsResponse.json();
            displayRecentResults(data.results);
        }
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

function updateStats(stats) {
    if (!stats) {
        document.getElementById('totalTests').textContent = '0';
        document.getElementById('lastTestDate').textContent = '-';
        document.getElementById('lowRiskCount').textContent = '0';
        document.getElementById('highRiskCount').textContent = '0';
        return;
    }

    document.getElementById('totalTests').textContent = stats.total_tests || 0;

    if (stats.latest_test_date) {
        const date = new Date(stats.latest_test_date);
        document.getElementById('lastTestDate').textContent = date.toLocaleDateString();
    }

    const riskDist = stats.risk_level_distribution || {};
    document.getElementById('lowRiskCount').textContent = riskDist.Low || 0;
    document.getElementById('highRiskCount').textContent = (riskDist.High || 0) + (riskDist.Moderate || 0);
}

function displayRecentResults(results) {
    const container = document.getElementById('recentResults');

    if (!results || results.length === 0) {
        container.innerHTML = '<p class="empty-state">No tests yet. Start your first screening!</p>';
        return;
    }

    container.innerHTML = results.map(result => {
        const date = new Date(result.test_date);
        const riskClass = getRiskClass(result.overall_risk_level);

        return `
            <div class="result-item" onclick="viewResult(${result.id})">
                <div class="result-info">
                    <h4>${result.task_type || 'Eye Tracking Test'}</h4>
                    <p>${date.toLocaleDateString()} at ${date.toLocaleTimeString()}</p>
                </div>
                <span class="result-risk ${riskClass}">${result.overall_risk_level || 'Unknown'}</span>
            </div>
        `;
    }).join('');
}

function getRiskClass(riskLevel) {
    if (!riskLevel) return 'low';
    const level = riskLevel.toLowerCase();
    if (level === 'high') return 'high';
    if (level === 'moderate') return 'moderate';
    return 'low';
}

// Test type selection
function selectTestType(type) {
    selectedTestType = type;
    document.querySelectorAll('.test-option').forEach(option => {
        option.classList.remove('active');
    });
    event.currentTarget.classList.add('active');
}

// Start test
async function startTest() {
    if (selectedTestType === 'webcam') {
        // Navigate to the webcam eye tracking page
        window.location.href = '/eye-test';
        return;
    }

    showTestProgress();

    if (selectedTestType === 'sample') {
        await runSampleAnalysis();
    } else {
        // For visual_search and other types, run sample for now
        await runSampleAnalysis();
    }
}

function showTestProgress() {
    document.getElementById('startTestBtn').style.display = 'none';
    const progress = document.getElementById('testProgress');
    progress.style.display = 'block';

    // Animate progress bar
    const fill = progress.querySelector('.progress-fill');
    let width = 0;
    const interval = setInterval(() => {
        width += Math.random() * 15;
        if (width >= 90) {
            clearInterval(interval);
        }
        fill.style.width = `${Math.min(width, 90)}%`;
    }, 200);

    progress.dataset.interval = interval;
}

function hideTestProgress() {
    document.getElementById('startTestBtn').style.display = 'block';
    const progress = document.getElementById('testProgress');
    progress.style.display = 'none';

    const fill = progress.querySelector('.progress-fill');
    fill.style.width = '100%';

    if (progress.dataset.interval) {
        clearInterval(parseInt(progress.dataset.interval));
    }
}

// Run sample analysis
async function runSampleAnalysis() {
    try {
        // Generate sample eye tracking data
        const numSamples = 5000;
        const timestamps = Array.from({ length: numSamples }, (_, i) => i);
        const xPositions = generateSampleData(numSamples, 500, 50);
        const yPositions = generateSampleData(numSamples, 400, 40);

        const response = await apiRequest('/api/analyze', {
            method: 'POST',
            body: JSON.stringify({
                timestamps,
                x_positions: xPositions,
                y_positions: yPositions,
                sampling_rate: 1000,
                task_type: 'Sample Analysis'
            })
        });

        if (response && response.ok) {
            const data = await response.json();
            hideTestProgress();
            displayResults(data);
        } else {
            hideTestProgress();
            alert('Analysis failed. Please try again.');
        }
    } catch (error) {
        console.error('Analysis error:', error);
        hideTestProgress();
        alert('Connection error. Please try again.');
    }
}

function generateSampleData(length, center, spread) {
    const data = [];
    let current = center;

    for (let i = 0; i < length; i++) {
        // Add some random movement
        current += (Math.random() - 0.5) * spread * 0.1;

        // Occasional saccades
        if (Math.random() < 0.02) {
            current += (Math.random() - 0.5) * spread;
        }

        // Keep within bounds
        current = Math.max(center - spread, Math.min(center + spread, current));
        data.push(current);
    }

    return data;
}

function displayResults(data) {
    const resultsCard = document.getElementById('resultsCard');
    resultsCard.style.display = 'block';

    const summary = data.results?.summary || {};
    const diseases = data.results?.disease_analysis || {};

    // Display summary
    const summaryEl = document.getElementById('resultsSummary');
    const riskLevel = summary.risk_level || 'Low';
    const riskClass = getRiskClass(riskLevel);

    summaryEl.innerHTML = `
        <h4>Overall Risk Assessment</h4>
        <div class="risk-level ${riskClass}">${riskLevel} Risk</div>
        <p>Highest concern: ${summary.highest_risk_disease || 'None'}</p>
    `;

    // Display breakdown
    const breakdownEl = document.getElementById('riskBreakdown');
    breakdownEl.innerHTML = Object.entries(diseases).map(([disease, info]) => {
        const score = info.risk_score || 0;
        const percentage = (score * 100).toFixed(1);
        const fillClass = score > 0.6 ? 'high' : (score > 0.3 ? 'moderate' : 'low');

        const diseaseNames = {
            'parkinsons': "Parkinson's Disease",
            'alzheimers': "Alzheimer's Disease",
            'asd': 'Autism Spectrum Disorder',
            'adhd': 'ADHD'
        };

        return `
            <div class="risk-item">
                <h5>${diseaseNames[disease] || disease}</h5>
                <div class="risk-bar">
                    <div class="risk-bar-fill ${fillClass}" style="width: ${percentage}%"></div>
                </div>
                <span class="risk-score">${percentage}% risk score</span>
            </div>
        `;
    }).join('');

    // Scroll to results
    resultsCard.scrollIntoView({ behavior: 'smooth' });

    // Refresh dashboard data
    loadDashboardData();
}

// Load test history
async function loadTestHistory() {
    const container = document.getElementById('historyList');
    container.innerHTML = '<p class="empty-state">Loading...</p>';

    try {
        const response = await apiRequest('/api/results?per_page=50');

        if (response && response.ok) {
            const data = await response.json();
            displayHistoryList(data.results);
        } else {
            container.innerHTML = '<p class="empty-state">Failed to load history</p>';
        }
    } catch (error) {
        console.error('Error loading history:', error);
        container.innerHTML = '<p class="empty-state">Connection error</p>';
    }
}

function displayHistoryList(results) {
    const container = document.getElementById('historyList');

    if (!results || results.length === 0) {
        container.innerHTML = '<p class="empty-state">No test history yet. Complete your first screening!</p>';
        return;
    }

    container.innerHTML = results.map(result => {
        const date = new Date(result.test_date);
        const risks = result.risk_scores || {};

        return `
            <div class="history-item" onclick="viewResult(${result.id})">
                <div class="history-info">
                    <h4>${result.task_type || 'Eye Tracking Test'}</h4>
                    <p>${date.toLocaleDateString()} at ${date.toLocaleTimeString()}</p>
                </div>
                <div class="history-risks">
                    ${formatMiniRisks(risks)}
                </div>
                <span class="result-risk ${getRiskClass(result.overall_risk_level)}">${result.overall_risk_level || 'Unknown'}</span>
            </div>
        `;
    }).join('');
}

function formatMiniRisks(risks) {
    const items = [];

    if (risks.parkinsons) items.push(`<span class="mini-risk park">PD ${(risks.parkinsons * 100).toFixed(0)}%</span>`);
    if (risks.alzheimers) items.push(`<span class="mini-risk alzh">AD ${(risks.alzheimers * 100).toFixed(0)}%</span>`);
    if (risks.asd) items.push(`<span class="mini-risk asd">ASD ${(risks.asd * 100).toFixed(0)}%</span>`);
    if (risks.adhd) items.push(`<span class="mini-risk adhd">ADHD ${(risks.adhd * 100).toFixed(0)}%</span>`);

    return items.join('');
}

// View specific result
async function viewResult(testId) {
    try {
        const response = await apiRequest(`/api/results/${testId}/report`);

        if (response && response.ok) {
            const data = await response.json();

            // Show result with option to download PDF
            const downloadPdf = confirm(
                (data.report || 'Analysis complete.') +
                '\n\n📥 Would you like to download the PDF report?'
            );

            if (downloadPdf) {
                downloadPdfReport(testId);
            }
        }
    } catch (error) {
        console.error('Error loading result:', error);
    }
}

// Download PDF report
async function downloadPdfReport(testId) {
    try {
        const token = getToken();
        if (!token) {
            alert('Please log in to download reports');
            return;
        }

        // Show loading indicator
        const loadingMsg = document.createElement('div');
        loadingMsg.id = 'pdfLoading';
        loadingMsg.innerHTML = '<div style="position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(0,0,0,0.8);color:white;padding:20px 40px;border-radius:10px;z-index:9999;">⏳ Generating PDF report...</div>';
        document.body.appendChild(loadingMsg);

        const response = await fetch(`/api/results/${testId}/pdf`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        // Remove loading indicator
        document.getElementById('pdfLoading')?.remove();

        if (response.ok) {
            // Get the filename from Content-Disposition header or use default
            const contentDisposition = response.headers.get('Content-Disposition');
            let filename = 'neuroscan_report.pdf';
            if (contentDisposition) {
                const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
                if (filenameMatch && filenameMatch[1]) {
                    filename = filenameMatch[1].replace(/['"]/g, '');
                }
            }

            // Download the PDF
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);

            console.log('PDF downloaded successfully');
        } else {
            const error = await response.json();
            alert(error.message || 'Failed to generate PDF report');
        }
    } catch (error) {
        document.getElementById('pdfLoading')?.remove();
        console.error('PDF download error:', error);
        alert('Failed to download PDF. Please try again.');
    }
}

// Load profile
async function loadProfile() {
    const user = getUser();
    if (!user) return;

    document.getElementById('profileFirstName').value = user.first_name || '';
    document.getElementById('profileLastName').value = user.last_name || '';
    document.getElementById('profileEmail').value = user.email || '';
    document.getElementById('profileDob').value = user.date_of_birth || '';
}

// Update profile
async function updateProfile(event) {
    event.preventDefault();

    const firstName = document.getElementById('profileFirstName').value;
    const lastName = document.getElementById('profileLastName').value;
    const dob = document.getElementById('profileDob').value;

    try {
        const response = await apiRequest('/api/user/profile', {
            method: 'PUT',
            body: JSON.stringify({
                first_name: firstName,
                last_name: lastName,
                date_of_birth: dob || null
            })
        });

        if (response && response.ok) {
            const data = await response.json();
            setUser(data.user);
            alert('Profile updated successfully!');
        } else {
            const data = await response.json();
            alert(data.message || 'Update failed');
        }
    } catch (error) {
        console.error('Profile update error:', error);
        alert('Connection error. Please try again.');
    }
}

/* ========================================
   Progress Tracking & Charts
======================================== */

let trendChart = null;
let riskDistChart = null;
let diseaseCompChart = null;
let currentTimeRange = 30;
let progressData = null;

// Load progress data
async function loadProgressData() {
    try {
        const resultsResponse = await apiRequest('/api/results?per_page=100');
        if (resultsResponse && resultsResponse.ok) {
            const data = await resultsResponse.json();
            progressData = data.results || [];

            if (progressData.length >= 2) {
                document.getElementById('noTrendData').style.display = 'none';
                document.getElementById('trendChart').style.display = 'block';
                renderCharts();
            } else {
                document.getElementById('noTrendData').style.display = 'block';
                document.getElementById('trendChart').style.display = 'none';
            }

            updateProgressStats();
        }
    } catch (error) {
        console.error('Error loading progress data:', error);
    }
}

// Set time range
function setTimeRange(range) {
    currentTimeRange = range;

    // Update button states
    document.querySelectorAll('.range-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.range == range);
    });

    renderCharts();
}

// Filter data by time range
function filterDataByRange(data) {
    if (currentTimeRange === 'all') return data;

    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - currentTimeRange);

    return data.filter(item => new Date(item.test_date) >= cutoff);
}

// Render all charts
function renderCharts() {
    if (!progressData) return;

    const filteredData = filterDataByRange(progressData);

    renderTrendChart(filteredData);
    renderRiskDistributionChart(filteredData);
    renderDiseaseComparisonChart(filteredData);
}

// Render trend line chart
function renderTrendChart(data) {
    const ctx = document.getElementById('trendChart');
    if (!ctx) return;

    // Destroy existing chart
    if (trendChart) {
        trendChart.destroy();
    }

    // Prepare data - sort by date
    const sortedData = [...data].sort((a, b) => new Date(a.test_date) - new Date(b.test_date));

    const labels = sortedData.map(d => {
        const date = new Date(d.test_date);
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    });

    trendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Parkinson's",
                    data: sortedData.map(d => (d.parkinsons_risk || 0) * 100),
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    tension: 0.4,
                    fill: false,
                    pointRadius: 4,
                    pointHoverRadius: 6
                },
                {
                    label: "Alzheimer's",
                    data: sortedData.map(d => (d.alzheimers_risk || 0) * 100),
                    borderColor: '#8b5cf6',
                    backgroundColor: 'rgba(139, 92, 246, 0.1)',
                    tension: 0.4,
                    fill: false,
                    pointRadius: 4,
                    pointHoverRadius: 6
                },
                {
                    label: 'ASD',
                    data: sortedData.map(d => (d.asd_risk || 0) * 100),
                    borderColor: '#ec4899',
                    backgroundColor: 'rgba(236, 72, 153, 0.1)',
                    tension: 0.4,
                    fill: false,
                    pointRadius: 4,
                    pointHoverRadius: 6
                },
                {
                    label: 'ADHD',
                    data: sortedData.map(d => (d.adhd_risk || 0) * 100),
                    borderColor: '#22c55e',
                    backgroundColor: 'rgba(34, 197, 94, 0.1)',
                    tension: 0.4,
                    fill: false,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 15, 20, 0.95)',
                    titleColor: '#fff',
                    bodyColor: '#a0a0b0',
                    borderColor: 'rgba(139, 92, 246, 0.3)',
                    borderWidth: 1,
                    padding: 12,
                    displayColors: true,
                    callbacks: {
                        label: function (context) {
                            return `${context.dataset.label}: ${context.raw.toFixed(1)}%`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.5)'
                    }
                },
                y: {
                    min: 0,
                    max: 100,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.5)',
                        callback: function (value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });
}

// Render risk distribution pie chart
function renderRiskDistributionChart(data) {
    const ctx = document.getElementById('riskDistributionChart');
    if (!ctx) return;

    if (riskDistChart) {
        riskDistChart.destroy();
    }

    const distribution = {
        Low: data.filter(d => d.overall_risk_level === 'Low').length,
        Moderate: data.filter(d => d.overall_risk_level === 'Moderate').length,
        High: data.filter(d => d.overall_risk_level === 'High').length
    };

    riskDistChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Low Risk', 'Moderate Risk', 'High Risk'],
            datasets: [{
                data: [distribution.Low, distribution.Moderate, distribution.High],
                backgroundColor: [
                    'rgba(34, 197, 94, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(239, 68, 68, 0.8)'
                ],
                borderColor: [
                    '#22c55e',
                    '#f59e0b',
                    '#ef4444'
                ],
                borderWidth: 2,
                hoverOffset: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: 'rgba(255, 255, 255, 0.7)',
                        padding: 15,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 15, 20, 0.95)',
                    titleColor: '#fff',
                    bodyColor: '#a0a0b0',
                    callbacks: {
                        label: function (context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = total > 0 ? ((context.raw / total) * 100).toFixed(1) : 0;
                            return `${context.label}: ${context.raw} tests (${percentage}%)`;
                        }
                    }
                }
            },
            cutout: '60%'
        }
    });
}

// Render disease comparison bar chart
function renderDiseaseComparisonChart(data) {
    const ctx = document.getElementById('diseaseComparisonChart');
    if (!ctx) return;

    if (diseaseCompChart) {
        diseaseCompChart.destroy();
    }

    // Calculate averages
    const avgParkinsons = data.length > 0 ? (data.reduce((sum, d) => sum + (d.parkinsons_risk || 0), 0) / data.length) * 100 : 0;
    const avgAlzheimers = data.length > 0 ? (data.reduce((sum, d) => sum + (d.alzheimers_risk || 0), 0) / data.length) * 100 : 0;
    const avgAsd = data.length > 0 ? (data.reduce((sum, d) => sum + (d.asd_risk || 0), 0) / data.length) * 100 : 0;
    const avgAdhd = data.length > 0 ? (data.reduce((sum, d) => sum + (d.adhd_risk || 0), 0) / data.length) * 100 : 0;

    diseaseCompChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ["Parkinson's", "Alzheimer's", 'ASD', 'ADHD'],
            datasets: [{
                label: 'Average Risk Score',
                data: [avgParkinsons, avgAlzheimers, avgAsd, avgAdhd],
                backgroundColor: [
                    'rgba(245, 158, 11, 0.7)',
                    'rgba(139, 92, 246, 0.7)',
                    'rgba(236, 72, 153, 0.7)',
                    'rgba(34, 197, 94, 0.7)'
                ],
                borderColor: [
                    '#f59e0b',
                    '#8b5cf6',
                    '#ec4899',
                    '#22c55e'
                ],
                borderWidth: 2,
                borderRadius: 6,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 15, 20, 0.95)',
                    titleColor: '#fff',
                    bodyColor: '#a0a0b0',
                    callbacks: {
                        label: function (context) {
                            return `Avg Risk: ${context.raw.toFixed(1)}%`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.6)'
                    }
                },
                y: {
                    min: 0,
                    max: 100,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.5)',
                        callback: function (value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });
}

// Update progress stats
function updateProgressStats() {
    if (!progressData || progressData.length === 0) return;

    // Find best improvement
    if (progressData.length >= 2) {
        const sortedData = [...progressData].sort((a, b) => new Date(a.test_date) - new Date(b.test_date));
        const first = sortedData[0];
        const last = sortedData[sortedData.length - 1];

        const improvements = {
            "Parkinson's": ((first.parkinsons_risk || 0) - (last.parkinsons_risk || 0)) * 100,
            "Alzheimer's": ((first.alzheimers_risk || 0) - (last.alzheimers_risk || 0)) * 100,
            'ASD': ((first.asd_risk || 0) - (last.asd_risk || 0)) * 100,
            'ADHD': ((first.adhd_risk || 0) - (last.adhd_risk || 0)) * 100
        };

        const bestKey = Object.keys(improvements).reduce((a, b) => improvements[a] > improvements[b] ? a : b);
        const bestValue = improvements[bestKey];

        if (bestValue > 0) {
            document.getElementById('bestImprovement').textContent = `-${bestValue.toFixed(1)}%`;
            document.getElementById('bestImprovementDetail').textContent = bestKey;
        } else {
            document.getElementById('bestImprovement').textContent = 'Stable';
            document.getElementById('bestImprovementDetail').textContent = 'No significant changes';
        }
    }

    // Test consistency - tests this month
    const thisMonth = new Date();
    thisMonth.setDate(1);
    const testsThisMonth = progressData.filter(d => new Date(d.test_date) >= thisMonth).length;
    document.getElementById('testConsistency').textContent = testsThisMonth;
    document.getElementById('testConsistencyDetail').textContent = 'Tests this month';

    // Calculate streak (weeks with at least one test)
    const weekMap = new Map();
    progressData.forEach(d => {
        const date = new Date(d.test_date);
        const weekStart = new Date(date);
        weekStart.setDate(date.getDate() - date.getDay());
        const weekKey = weekStart.toISOString().split('T')[0];
        weekMap.set(weekKey, true);
    });

    let streak = 0;
    let currentWeek = new Date();
    currentWeek.setDate(currentWeek.getDate() - currentWeek.getDay());

    while (weekMap.has(currentWeek.toISOString().split('T')[0])) {
        streak++;
        currentWeek.setDate(currentWeek.getDate() - 7);
    }

    document.getElementById('testStreak').textContent = streak;

    // Overall trend
    if (progressData.length >= 2) {
        const sortedData = [...progressData].sort((a, b) => new Date(a.test_date) - new Date(b.test_date));
        const recentHalf = sortedData.slice(Math.floor(sortedData.length / 2));
        const olderHalf = sortedData.slice(0, Math.floor(sortedData.length / 2));

        const recentAvg = recentHalf.reduce((sum, d) => sum + (d.parkinsons_risk || 0) + (d.alzheimers_risk || 0) + (d.asd_risk || 0) + (d.adhd_risk || 0), 0) / (recentHalf.length * 4);
        const olderAvg = olderHalf.reduce((sum, d) => sum + (d.parkinsons_risk || 0) + (d.alzheimers_risk || 0) + (d.asd_risk || 0) + (d.adhd_risk || 0), 0) / (olderHalf.length * 4);

        if (recentAvg < olderAvg - 0.02) {
            document.getElementById('overallTrend').textContent = '📉 Improving';
            document.getElementById('overallTrendDetail').textContent = 'Risk scores decreasing';
        } else if (recentAvg > olderAvg + 0.02) {
            document.getElementById('overallTrend').textContent = '📈 Increasing';
            document.getElementById('overallTrendDetail').textContent = 'Monitor closely';
        } else {
            document.getElementById('overallTrend').textContent = '➡️ Stable';
            document.getElementById('overallTrendDetail').textContent = 'Consistent readings';
        }
    }
}
