# API Documentation - Disease Detection System

## Base URL

```
Production: https://api.yourdomain.com
Development: http://localhost:5000
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Response Format

All responses follow this general structure:

### Success Response
```json
{
  "message": "Success message",
  "data": { ... }
}
```

### Error Response
```json
{
  "message": "Error description"
}
```

## Endpoints

### 1. Health Check

Check API health status.

**Endpoint:** `GET /api/health`

**Authentication:** None required

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-25T05:04:47.123Z",
  "version": "1.0.0"
}
```

---

### 2. User Registration

Register a new user account.

**Endpoint:** `POST /api/auth/register`

**Authentication:** None required

**Request Body:**
```json
{
  "email": "patient@example.com",
  "password": "SecurePassword123!",
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-01-15"
}
```

**Required Fields:**
- `email` (string): Valid email address
- `password` (string): Minimum 8 characters
- `first_name` (string): User's first name
- `last_name` (string): User's last name

**Optional Fields:**
- `date_of_birth` (string): ISO 8601 date format

**Success Response (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "patient@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-01-15",
    "created_at": "2026-01-25T05:04:47.123Z",
    "last_login": null
  }
}
```

**Error Responses:**
- `400`: Missing required fields or invalid data
- `400`: Email already registered

---

### 3. User Login

Authenticate and receive JWT token.

**Endpoint:** `POST /api/auth/login`

**Authentication:** None required

**Request Body:**
```json
{
  "email": "patient@example.com",
  "password": "SecurePassword123!"
}
```

**Success Response (200):**
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "patient@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-01-15",
    "created_at": "2026-01-25T05:04:47.123Z",
    "last_login": "2026-01-25T05:04:47.123Z"
  }
}
```

**Error Responses:**
- `400`: Email and password required
- `401`: Invalid credentials
- `401`: Account is inactive

---

### 4. Get User Profile

Retrieve current user's profile information.

**Endpoint:** `GET /api/user/profile`

**Authentication:** Required

**Success Response (200):**
```json
{
  "id": 1,
  "email": "patient@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-01-15",
  "created_at": "2026-01-25T05:04:47.123Z",
  "last_login": "2026-01-25T05:04:47.123Z"
}
```

**Error Responses:**
- `401`: Token is missing or invalid

---

### 5. Update User Profile

Update user profile information.

**Endpoint:** `PUT /api/user/profile`

**Authentication:** Required

**Request Body:**
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "date_of_birth": "1992-03-20"
}
```

**Success Response (200):**
```json
{
  "message": "Profile updated successfully",
  "user": {
    "id": 1,
    "email": "patient@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "date_of_birth": "1992-03-20",
    "created_at": "2026-01-25T05:04:47.123Z",
    "last_login": "2026-01-25T05:04:47.123Z"
  }
}
```

**Error Responses:**
- `401`: Token is missing or invalid
- `500`: Update failed

---

### 6. Analyze Eye Tracking Data

Submit eye tracking data for disease analysis.

**Endpoint:** `POST /api/analyze`

**Authentication:** Required

**Request Body:**
```json
{
  "timestamps": [0, 1, 2, 3, 4, 5, ...],
  "x_positions": [100, 102, 105, 108, ...],
  "y_positions": [200, 198, 195, 193, ...],
  "pupil_sizes": [3.0, 3.1, 3.2, ...],
  "sampling_rate": 1000.0,
  "task_type": "visual_search"
}
```

**Required Fields:**
- `timestamps` (array of numbers): Timestamps in milliseconds
- `x_positions` (array of numbers): X-coordinates of gaze
- `y_positions` (array of numbers): Y-coordinates of gaze

**Optional Fields:**
- `pupil_sizes` (array of numbers): Pupil diameter measurements
- `sampling_rate` (number): Sampling rate in Hz (default: 1000.0)
- `task_type` (string): Type of task performed

**Success Response (200):**
```json
{
  "message": "Analysis completed successfully",
  "test_id": 42,
  "results": {
    "disease_analysis": {
      "parkinsons": {
        "risk_score": 0.45,
        "risk_level": "Moderate",
        "indicators": [
          "Reduced saccade velocity detected",
          "Prolonged fixations detected"
        ],
        "recommendations": [
          "Consider neurological consultation",
          "Monitor motor symptoms"
        ]
      },
      "alzheimers": {
        "risk_score": 0.30,
        "risk_level": "Low",
        "indicators": [],
        "recommendations": []
      },
      "asd": {
        "risk_score": 0.15,
        "risk_level": "Low",
        "indicators": [],
        "recommendations": []
      },
      "adhd": {
        "risk_score": 0.25,
        "risk_level": "Low",
        "indicators": [],
        "recommendations": []
      }
    },
    "summary": {
      "highest_risk_disease": "parkinsons",
      "highest_risk_score": 0.45,
      "risk_level": "Moderate",
      "overall_recommendations": [
        "Consider neurological consultation",
        "Monitor motor symptoms"
      ]
    },
    "test_date": "2026-01-25T05:04:47.123Z"
  }
}
```

**Error Responses:**
- `400`: Missing required fields
- `401`: Token is missing or invalid
- `500`: Analysis failed

---

### 7. Get All Test Results

Retrieve all test results for the current user with pagination.

**Endpoint:** `GET /api/results`

**Authentication:** Required

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `per_page` (integer): Results per page (default: 10, max: 100)

**Example:** `GET /api/results?page=1&per_page=20`

**Success Response (200):**
```json
{
  "results": [
    {
      "id": 42,
      "user_id": 1,
      "test_date": "2026-01-25T05:04:47.123Z",
      "task_type": "visual_search",
      "duration_ms": 5000.0,
      "num_samples": 5000,
      "risk_scores": {
        "parkinsons": 0.45,
        "alzheimers": 0.30,
        "asd": 0.15,
        "adhd": 0.25
      },
      "overall_risk_level": "Moderate",
      "highest_risk_disease": "parkinsons"
    },
    ...
  ],
  "total": 50,
  "pages": 5,
  "current_page": 1
}
```

**Error Responses:**
- `401`: Token is missing or invalid
- `500`: Failed to retrieve results

---

### 8. Get Specific Test Result

Retrieve detailed information for a specific test.

**Endpoint:** `GET /api/results/<test_id>`

**Authentication:** Required

**Success Response (200):**
```json
{
  "test_info": {
    "id": 42,
    "user_id": 1,
    "test_date": "2026-01-25T05:04:47.123Z",
    "task_type": "visual_search",
    "duration_ms": 5000.0,
    "num_samples": 5000,
    "risk_scores": {
      "parkinsons": 0.45,
      "alzheimers": 0.30,
      "asd": 0.15,
      "adhd": 0.25
    },
    "overall_risk_level": "Moderate",
    "highest_risk_disease": "parkinsons"
  },
  "disease_analysis": {
    "parkinsons": {
      "risk_score": 0.45,
      "risk_level": "Moderate",
      "indicators": [...],
      "recommendations": [...]
    },
    ...
  },
  "features": {
    "mean_saccade_velocity": 320.5,
    "mean_fixation_duration": 280.3,
    ...
  }
}
```

**Error Responses:**
- `401`: Token is missing or invalid
- `404`: Test result not found
- `500`: Failed to retrieve result

---

### 9. Get Test Report

Generate and retrieve a detailed text report for a test.

**Endpoint:** `GET /api/results/<test_id>/report`

**Authentication:** Required

**Success Response (200):**
```json
{
  "report": "======================================================================\nEYE TRACKING DISEASE DETECTION REPORT\n======================================================================\n\nSubject ID: USER_1\n...",
  "test_date": "2026-01-25T05:04:47.123Z"
}
```

**Error Responses:**
- `401`: Token is missing or invalid
- `404`: Test result not found
- `500`: Failed to generate report

---

### 10. Get User Statistics

Get statistical summary of user's test history.

**Endpoint:** `GET /api/statistics`

**Authentication:** Required

**Success Response (200):**
```json
{
  "statistics": {
    "total_tests": 15,
    "latest_test_date": "2026-01-25T05:04:47.123Z",
    "risk_trends": {
      "parkinsons": [0.45, 0.42, 0.38, ...],
      "alzheimers": [0.30, 0.28, 0.25, ...],
      "asd": [0.15, 0.12, 0.10, ...],
      "adhd": [0.25, 0.22, 0.20, ...]
    },
    "risk_level_distribution": {
      "Low": 8,
      "Moderate": 5,
      "High": 2
    }
  }
}
```

**Error Responses:**
- `401`: Token is missing or invalid
- `500`: Failed to calculate statistics

---

## Data Models

### Risk Levels

- **Low**: Risk score < 0.3
- **Moderate**: Risk score 0.3 - 0.6
- **High**: Risk score > 0.6

### Disease Types

- `parkinsons`: Parkinson's Disease
- `alzheimers`: Alzheimer's Disease
- `asd`: Autism Spectrum Disorder
- `adhd`: Attention Deficit Hyperactivity Disorder

### Task Types

Common task types for eye tracking:
- `visual_search`: Visual search task
- `reading`: Reading task
- `smooth_pursuit`: Smooth pursuit tracking
- `fixation`: Fixation stability task
- `saccade`: Saccadic eye movement task
- `general`: General/unspecified task

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created successfully |
| 400 | Bad request - invalid input |
| 401 | Unauthorized - missing or invalid token |
| 404 | Resource not found |
| 429 | Too many requests - rate limit exceeded |
| 500 | Internal server error |

---

## Rate Limiting

API endpoints are rate-limited to prevent abuse:

- **General API endpoints**: 10 requests per second
- **Login endpoint**: 5 requests per minute
- **Burst allowance**: 20 requests

When rate limit is exceeded, the API returns a `429` status code.

---

## Example Usage

### Python Example

```python
import requests
import json

# Base URL
base_url = "http://localhost:5000"

# 1. Register
register_data = {
    "email": "patient@example.com",
    "password": "SecurePassword123!",
    "first_name": "John",
    "last_name": "Doe"
}
response = requests.post(f"{base_url}/api/auth/register", json=register_data)
print(response.json())

# 2. Login
login_data = {
    "email": "patient@example.com",
    "password": "SecurePassword123!"
}
response = requests.post(f"{base_url}/api/auth/login", json=login_data)
token = response.json()["token"]

# 3. Set headers for authenticated requests
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# 4. Submit analysis
analysis_data = {
    "timestamps": list(range(5000)),
    "x_positions": [100 + i*0.1 for i in range(5000)],
    "y_positions": [200 + i*0.05 for i in range(5000)],
    "sampling_rate": 1000.0,
    "task_type": "visual_search"
}
response = requests.post(f"{base_url}/api/analyze", json=analysis_data, headers=headers)
test_id = response.json()["test_id"]

# 5. Get results
response = requests.get(f"{base_url}/api/results/{test_id}", headers=headers)
print(json.dumps(response.json(), indent=2))

# 6. Get all results
response = requests.get(f"{base_url}/api/results?page=1&per_page=10", headers=headers)
print(json.dumps(response.json(), indent=2))
```

### JavaScript Example

```javascript
const baseUrl = 'http://localhost:5000';

// 1. Register
async function register() {
  const response = await fetch(`${baseUrl}/api/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: 'patient@example.com',
      password: 'SecurePassword123!',
      first_name: 'John',
      last_name: 'Doe'
    })
  });
  return await response.json();
}

// 2. Login
async function login() {
  const response = await fetch(`${baseUrl}/api/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: 'patient@example.com',
      password: 'SecurePassword123!'
    })
  });
  const data = await response.json();
  return data.token;
}

// 3. Analyze data
async function analyzeData(token) {
  const response = await fetch(`${baseUrl}/api/analyze`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      timestamps: Array.from({length: 5000}, (_, i) => i),
      x_positions: Array.from({length: 5000}, (_, i) => 100 + i * 0.1),
      y_positions: Array.from({length: 5000}, (_, i) => 200 + i * 0.05),
      sampling_rate: 1000.0,
      task_type: 'visual_search'
    })
  });
  return await response.json();
}

// 4. Get results
async function getResults(token, page = 1) {
  const response = await fetch(`${baseUrl}/api/results?page=${page}&per_page=10`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return await response.json();
}

// Usage
(async () => {
  await register();
  const token = await login();
  const analysis = await analyzeData(token);
  const results = await getResults(token);
  console.log(results);
})();
```

### cURL Examples

```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "patient@example.com",
    "password": "SecurePassword123!",
    "first_name": "John",
    "last_name": "Doe"
  }'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "patient@example.com",
    "password": "SecurePassword123!"
  }'

# Analyze (replace TOKEN with actual JWT)
curl -X POST http://localhost:5000/api/analyze \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "timestamps": [0, 1, 2, 3, 4],
    "x_positions": [100, 102, 105, 108, 110],
    "y_positions": [200, 198, 195, 193, 190],
    "sampling_rate": 1000.0,
    "task_type": "visual_search"
  }'

# Get results
curl -X GET http://localhost:5000/api/results?page=1&per_page=10 \
  -H "Authorization: Bearer TOKEN"
```

---

## Best Practices

1. **Token Management**
   - Store tokens securely (e.g., httpOnly cookies, secure storage)
   - Refresh tokens before expiration
   - Don't expose tokens in URLs or logs

2. **Data Validation**
   - Validate all input data before submission
   - Ensure arrays have matching lengths
   - Use appropriate data types

3. **Error Handling**
   - Always check response status codes
   - Handle network errors gracefully
   - Provide user-friendly error messages

4. **Performance**
   - Use pagination for large result sets
   - Cache frequently accessed data
   - Compress large payloads

5. **Security**
   - Always use HTTPS in production
   - Never log or expose sensitive data
   - Implement proper authentication
   - Validate JWT tokens on every request

---

## Support

For API support:
- GitHub Issues: https://github.com/punit745/Disease_deteaction-/issues
- Documentation: See README.md and DEPLOYMENT.md
