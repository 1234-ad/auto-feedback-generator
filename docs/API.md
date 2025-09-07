# Auto-Feedback Generator API Documentation

## Overview
The Auto-Feedback Generator API provides endpoints for generating personalized feedback for students based on their performance data.

**Author:** Adithya  
**Version:** 1.0.0

## Base URL
```
http://localhost:3000
```

## Endpoints

### Health Check
**GET** `/health`

Returns the health status of the API.

**Response:**
```json
{
  "status": "OK",
  "timestamp": "2025-09-07T07:32:51.000Z"
}
```

### Generate Feedback
**POST** `/generate-feedback`

Generates personalized feedback for a student based on their performance data.

**Request Body:**
```json
{
  "studentData": {
    "name": "John Doe",
    "performance": 85,
    "subject": "Mathematics",
    "weakAreas": ["Geometry", "Word problems"],
    "strengths": ["Algebra", "Problem solving"],
    "learningStyle": "visual"
  },
  "criteria": {
    "rubric": {
      "excellence": 85,
      "good": 70,
      "improvement": 50
    },
    "weight": 1.0
  }
}
```

**Response:**
```json
{
  "studentName": "John Doe",
  "subject": "Mathematics",
  "performanceLevel": "good",
  "feedback": "Good progress! John Doe shows solid grasp of Mathematics with room for improvement in Geometry, Word problems.",
  "recommendations": [
    "Target improvement areas: Geometry, Word problems",
    "Build upon strengths: Algebra, Problem solving",
    "Adapt teaching methods for visual learning style"
  ],
  "nextSteps": [
    "Practice additional exercises in identified areas",
    "Seek clarification on challenging concepts"
  ],
  "timestamp": "2025-09-07T07:32:51.000Z"
}
```

## Data Models

### Student Data
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Student's full name |
| performance | number | Yes | Performance score (0-100) |
| subject | string | Yes | Subject being assessed |
| weakAreas | array | No | Areas needing improvement |
| strengths | array | No | Student's strong areas |
| learningStyle | string | No | Preferred learning style |

### Criteria
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| rubric | object | No | Assessment rubric with thresholds |
| weight | number | No | Weight factor (0-1) |

## Error Responses

### 400 Bad Request
```json
{
  "error": "Validation failed",
  "details": [
    "name is required",
    "Performance must be a number between 0 and 100"
  ]
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred"
}
```

## Usage Examples

### cURL Example
```bash
curl -X POST http://localhost:3000/generate-feedback \
  -H "Content-Type: application/json" \
  -d '{
    "studentData": {
      "name": "Alice Johnson",
      "performance": 92,
      "subject": "Science",
      "weakAreas": [],
      "strengths": ["Lab work", "Analysis"]
    },
    "criteria": {}
  }'
```

### JavaScript Example
```javascript
const response = await fetch('http://localhost:3000/generate-feedback', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    studentData: {
      name: 'Alice Johnson',
      performance: 92,
      subject: 'Science',
      weakAreas: [],
      strengths: ['Lab work', 'Analysis']
    },
    criteria: {}
  })
});

const feedback = await response.json();
console.log(feedback);
```