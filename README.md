# 🎓 Auto Feedback Generator

An AI-powered tool that helps teachers and trainers quickly generate personalized feedback for students based on performance rubrics. Built with **Streamlit** frontend and **Flask** backend, powered by **OpenAI GPT-4**.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Features

- **🤖 AI-Powered Feedback Generation** - Uses OpenAI GPT-4 to create human-like, personalized feedback
- **📊 Rubric-Based Input** - Accepts structured rubric scores and criteria
- **🎨 Multiple Feedback Styles** - Constructive, encouraging, detailed, or brief feedback types
- **📱 User-Friendly Interface** - Clean Streamlit web interface for educators
- **📄 PDF Export** - Download feedback as professional PDF reports
- **📋 Copy to Clipboard** - Quick copy functionality for immediate use
- **📚 Feedback History** - Track and manage previously generated feedback
- **🔧 Subject-Specific Templates** - Tailored prompts for different academic subjects
- **⚡ Real-time Generation** - Instant feedback creation with progress indicators
- **🛡️ Input Validation** - Comprehensive validation and error handling

## 🏗️ Architecture

```
┌─────────────────┐    HTTP/JSON    ┌─────────────────┐    OpenAI API    ┌─────────────────┐
│   Streamlit     │ ──────────────► │   Flask         │ ──────────────► │   OpenAI        │
│   Frontend      │                 │   Backend       │                 │   GPT-4         │
│                 │ ◄────────────── │                 │ ◄────────────── │                 │
└─────────────────┘                 └─────────────────┘                 └─────────────────┘
        │                                   │
        │                                   │
        ▼                                   ▼
┌─────────────────┐                 ┌─────────────────┐
│   PDF Generator │                 │   Prompt        │
│   UI Components │                 │   Templates     │
└─────────────────┘                 └─────────────────┘
```

## 📋 Requirements

### System Requirements
- Python 3.8 or higher
- OpenAI API key
- 2GB RAM minimum
- Internet connection

### Dependencies
- **Frontend**: Streamlit, Plotly, ReportLab, PyPDF2
- **Backend**: Flask, OpenAI, Python-dotenv, Requests
- **Testing**: Pytest, Pytest-Flask
- **Deployment**: Gunicorn (production)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/1234-ad/auto-feedback-generator.git
cd auto-feedback-generator
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your configuration
nano .env
```

**Required Environment Variables:**
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
FLASK_ENV=development
PORT=5000
BACKEND_URL=http://localhost:5000
```

## 🚀 Quick Start

### Option 1: Run Both Services Separately

**Terminal 1 - Backend:**
```bash
python run_backend.py
```

**Terminal 2 - Frontend:**
```bash
python run_frontend.py
```

### Option 2: Development Mode
```bash
# Backend with auto-reload
cd backend
python -m flask run --debug

# Frontend with auto-reload
cd frontend
streamlit run app.py
```

### 3. Access the Application
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:5000
- **API Documentation**: http://localhost:5000/api/feedback-templates

## 📖 Usage Guide

### 1. **Student Information**
- Enter student's full name
- Add assignment title (optional)
- Select subject area
- Choose feedback type

### 2. **Rubric Input**
- Click "➕ Add Criterion" to add evaluation criteria
- Enter criterion name (e.g., "Problem Solving", "Communication")
- Set score and maximum score for each criterion
- View real-time rubric summary and visualization

### 3. **Generate Feedback**
- Click "🚀 Generate Feedback"
- Wait for AI processing (typically 3-10 seconds)
- Review generated feedback in the right panel

### 4. **Export Options**
- **📋 Copy to Clipboard** - For immediate use
- **📄 Download PDF** - Professional report format
- **📊 Export CSV** - Bulk export of feedback history

## 🎯 Feedback Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Constructive** | Balanced feedback with strengths and improvements | General assignments and assessments |
| **Encouraging** | Positive, confidence-building feedback | Struggling students or early learners |
| **Detailed** | Comprehensive analysis with specific guidance | Complex projects or advanced students |
| **Brief** | Concise, essential feedback points | Quick assessments or time constraints |

## 📚 Subject Templates

The system includes specialized prompt templates for:
- **Mathematics** - Problem-solving, computational accuracy
- **Science** - Scientific method, experimental design
- **English** - Writing clarity, grammar, analysis
- **History** - Critical analysis, historical context
- **Art** - Creativity, technical skills, composition
- **Physical Education** - Skill development, teamwork
- **General** - Universal feedback principles

## 🔧 API Documentation

### Generate Feedback Endpoint
```http
POST /api/generate-feedback
Content-Type: application/json

{
  "student_name": "John Doe",
  "assignment_title": "Math Quiz 1",
  "subject": "Mathematics",
  "feedback_type": "constructive",
  "rubric_data": {
    "problem_solving": {"score": 8, "max_score": 10},
    "communication": {"score": 7, "max_score": 10},
    "accuracy": {"score": 9, "max_score": 10}
  }
}
```

### Response Format
```json
{
  "success": true,
  "feedback": "Great work on your math quiz, John! Your accuracy is excellent...",
  "metadata": {
    "student_name": "John Doe",
    "assignment_title": "Math Quiz 1",
    "generated_at": "2024-01-15T10:30:00",
    "feedback_type": "constructive",
    "subject": "Mathematics"
  }
}
```

## 🧪 Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test Categories
```bash
# Backend API tests
pytest tests/test_backend.py -v

# Validation tests
pytest tests/test_backend.py::TestValidators -v

# Prompt template tests
pytest tests/test_backend.py::TestPromptTemplates -v
```

### Test Coverage
```bash
pytest --cov=backend tests/
```

## 🚀 Deployment

### Local Production
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app

# Run Streamlit in production mode
streamlit run frontend/app.py --server.headless true
```

### Docker Deployment
```dockerfile
# Dockerfile example
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000 8501

CMD ["python", "run_backend.py"]
```

### Cloud Deployment Options
- **Render** - Easy deployment with automatic builds
- **Heroku** - Simple git-based deployment
- **Railway** - Modern deployment platform
- **Streamlit Cloud** - Native Streamlit hosting
- **AWS/GCP/Azure** - Enterprise cloud solutions

## 🔒 Security Considerations

- **API Key Protection** - Store OpenAI API key securely in environment variables
- **Input Validation** - Comprehensive validation prevents injection attacks
- **Rate Limiting** - Implement rate limiting for production use
- **HTTPS** - Use HTTPS in production environments
- **CORS** - Configure CORS policies appropriately

## 🐛 Troubleshooting

### Common Issues

**1. OpenAI API Key Error**
```
Error: OpenAI API key not found
Solution: Set OPENAI_API_KEY in your .env file
```

**2. Backend Connection Failed**
```
Error: Cannot connect to backend
Solution: Ensure backend is running on correct port (5000)
```

**3. Module Import Error**
```
Error: No module named 'backend'
Solution: Run from project root directory
```

**4. Rate Limit Exceeded**
```
Error: API rate limit exceeded
Solution: Wait a moment and try again, or upgrade OpenAI plan
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit changes** (`git commit -m 'Add amazing feature'`)
4. **Push to branch** (`git push origin feature/amazing-feature`)
5. **Open Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation
- Use meaningful commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for providing the GPT-4 API
- **Streamlit** for the amazing frontend framework
- **Flask** for the robust backend framework
- **ReportLab** for PDF generation capabilities

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/1234-ad/auto-feedback-generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/1234-ad/auto-feedback-generator/discussions)
- **Email**: [Contact Developer](mailto:adithya@example.com)

## 🗺️ Roadmap

- [ ] **Multi-language Support** - Support for multiple languages
- [ ] **Batch Processing** - Process multiple students at once
- [ ] **Integration APIs** - Connect with LMS platforms
- [ ] **Advanced Analytics** - Feedback quality metrics
- [ ] **Custom Templates** - User-defined prompt templates
- [ ] **Voice Feedback** - Text-to-speech capabilities
- [ ] **Mobile App** - Native mobile applications

---

**Made with ❤️ by Adithya for educators worldwide**