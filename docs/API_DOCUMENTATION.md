# 📚 API Documentation

## Overview

The Auto Feedback Generator API provides endpoints for generating personalized feedback based on student performance rubrics. The API is built with Flask and uses OpenAI GPT-4 for natural language generation.

**Base URL**: `http://localhost:5000` (development)

## Authentication

Currently, the API doesn't require authentication for basic usage. However, you need to configure your OpenAI API key in the backend environment.

## Endpoints

### 1. Health Check

**GET** `/api/health`

Check the health status of the API and verify configuration.

#### Response
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "api_key_configured": true
}
```

#### Status Codes
- `200` - Service is healthy
- `500` - Service is unhealthy

---

### 2. Generate Feedback

**POST** `/api/generate-feedback`

Generate personalized feedback based on rubric data.

#### Request Body
```json
{
  "student_name": "John Doe",
  "assignment_title": "Math Quiz 1",
  "subject": "Mathematics",
  "feedback_type": "constructive",
  "rubric_data": {
    "problem_solving": {
      "score": 8,
      "max_score": 10
    },
    "communication": {
      "score": 7,
      "max_score": 10
    },
    "accuracy": {
      "score": 9,
      "max_score": 10
    }
  }
}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `student_name` | string | Yes | Name of the student (1-100 characters) |
| `assignment_title` | string | No | Title of the assignment (max 200 characters) |
| `subject` | string | No | Subject area (see valid subjects below) |
| `feedback_type` | string | No | Type of feedback (see valid types below) |
| `rubric_data` | object | Yes | Rubric scores and criteria |

#### Valid Subjects
- `General` (default)
- `Mathematics`
- `Science`
- `English`
- `History`
- `Art`
- `Physical Education`

#### Valid Feedback Types
- `constructive` (default)
- `encouraging`
- `detailed`
- `brief`

#### Rubric Data Format

Each criterion in `rubric_data` should follow this format:
```json
{
  "criterion_name": {
    "score": 8.5,
    "max_score": 10
  }
}
```

**Constraints:**
- Maximum 20 criteria per rubric
- Scores must be non-negative
- Scores cannot exceed max_score
- Max_score must be positive

#### Success Response
```json
{
  "success": true,
  "feedback": "Great work on your math quiz, John! Your accuracy is excellent, showing strong attention to detail and mathematical precision. Your problem-solving approach demonstrates solid understanding of the concepts. To further improve, consider explaining your reasoning more clearly in your written work, as this will help demonstrate your thought process. Keep up the excellent work in accuracy - it's one of your strongest skills!",
  "metadata": {
    "student_name": "John Doe",
    "assignment_title": "Math Quiz 1",
    "generated_at": "2024-01-15T10:30:00.000Z",
    "feedback_type": "constructive",
    "subject": "Mathematics"
  }
}
```

#### Error Response
```json
{
  "error": "Validation failed",
  "details": [
    "Missing required field: student_name",
    "Score cannot exceed max score for criterion: problem_solving"
  ]
}
```

#### Status Codes
- `200` - Success
- `400` - Bad Request (validation errors)
- `429` - Rate limit exceeded
- `500` - Internal server error

---

### 3. Get Feedback Templates

**GET** `/api/feedback-templates`

Get information about available feedback types, subjects, and sample rubric format.

#### Response
```json
{
  "feedback_types": [
    "constructive",
    "encouraging",
    "detailed",
    "brief"
  ],
  "subjects": [
    "Mathematics",
    "Science",
    "English",
    "History",
    "Art",
    "Physical Education",
    "General"
  ],
  "sample_rubric": {
    "communication": {
      "score": 8,
      "max_score": 10
    },
    "teamwork": {
      "score": 6,
      "max_score": 10
    },
    "creativity": {
      "score": 9,
      "max_score": 10
    },
    "technical_skills": {
      "score": 7,
      "max_score": 10
    }
  }
}
```

---

## Error Handling

The API uses standard HTTP status codes and returns detailed error messages.

### Common Error Responses

#### 400 Bad Request
```json
{
  "error": "Validation failed",
  "message": "Input validation failed",
  "details": [
    "Student name cannot be empty",
    "Invalid feedback type. Must be one of: constructive, encouraging, detailed, brief"
  ],
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

#### 429 Rate Limit Exceeded
```json
{
  "error": "API Error",
  "message": "API rate limit exceeded. Please try again in a moment.",
  "type": "RateLimitError",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

#### 500 Internal Server Error
```json
{
  "error": "API Error",
  "message": "An unexpected error occurred. Please try again.",
  "type": "InternalServerError",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse:
- **Development**: 60 requests per minute per IP
- **Production**: Configurable based on deployment

When rate limit is exceeded, the API returns a `429` status code with retry information.

## Examples

### cURL Examples

#### Generate Feedback
```bash
curl -X POST http://localhost:5000/api/generate-feedback \
  -H "Content-Type: application/json" \
  -d '{
    "student_name": "Alice Smith",
    "assignment_title": "Science Project",
    "subject": "Science",
    "feedback_type": "encouraging",
    "rubric_data": {
      "research_quality": {"score": 8, "max_score": 10},
      "presentation": {"score": 7, "max_score": 10},
      "creativity": {"score": 9, "max_score": 10}
    }
  }'
```

#### Health Check
```bash
curl http://localhost:5000/api/health
```

### Python Examples

#### Using Requests Library
```python
import requests

# Generate feedback
url = "http://localhost:5000/api/generate-feedback"
data = {
    "student_name": "Bob Johnson",
    "assignment_title": "Essay Assignment",
    "subject": "English",
    "feedback_type": "detailed",
    "rubric_data": {
        "grammar": {"score": 8, "max_score": 10},
        "content": {"score": 9, "max_score": 10},
        "organization": {"score": 7, "max_score": 10}
    }
}

response = requests.post(url, json=data)
if response.status_code == 200:
    result = response.json()
    print(result["feedback"])
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

### JavaScript Examples

#### Using Fetch API
```javascript
const generateFeedback = async (feedbackData) => {
  try {
    const response = await fetch('http://localhost:5000/api/generate-feedback', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(feedbackData)
    });

    if (response.ok) {
      const result = await response.json();
      console.log('Feedback:', result.feedback);
      return result;
    } else {
      const error = await response.json();
      console.error('Error:', error);
      throw new Error(error.message);
    }
  } catch (error) {
    console.error('Network error:', error);
    throw error;
  }
};

// Usage
const feedbackData = {
  student_name: "Carol Davis",
  assignment_title: "Art Project",
  subject: "Art",
  feedback_type: "constructive",
  rubric_data: {
    creativity: { score: 9, max_score: 10 },
    technique: { score: 7, max_score: 10 },
    presentation: { score: 8, max_score: 10 }
  }
};

generateFeedback(feedbackData);
```

## Best Practices

### 1. Input Validation
Always validate input data before sending requests:
- Check required fields
- Validate score ranges
- Ensure proper data types

### 2. Error Handling
Implement proper error handling:
- Check response status codes
- Parse error messages
- Implement retry logic for rate limits

### 3. Rate Limiting
Respect rate limits:
- Implement exponential backoff
- Cache responses when appropriate
- Monitor usage patterns

### 4. Security
- Never expose API keys in client-side code
- Use HTTPS in production
- Validate and sanitize all inputs

## Testing the API

### Using Postman

1. **Import Collection**: Create a Postman collection with the endpoints
2. **Set Environment Variables**: Configure base URL and test data
3. **Test Scenarios**: Create tests for success and error cases

### Using pytest

```python
import pytest
import requests

def test_generate_feedback():
    url = "http://localhost:5000/api/generate-feedback"
    data = {
        "student_name": "Test Student",
        "rubric_data": {
            "test_criterion": {"score": 8, "max_score": 10}
        }
    }
    
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert "feedback" in response.json()
```

## Changelog

### Version 1.0.0
- Initial API release
- Basic feedback generation
- Health check endpoint
- Template information endpoint
- Comprehensive error handling
- Input validation
- Rate limiting support