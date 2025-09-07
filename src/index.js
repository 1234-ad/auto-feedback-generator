const express = require('express');
const cors = require('cors');
require('dotenv').config();

const FeedbackGenerator = require('./services/feedbackGenerator');
const Validator = require('./utils/validator');

const app = express();
const PORT = process.env.PORT || 3000;

// Initialize feedback generator
const feedbackGenerator = new FeedbackGenerator();

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.get('/', (req, res) => {
  res.json({
    message: 'Auto-Feedback Generator API',
    version: '1.0.0',
    author: 'Adithya',
    endpoints: {
      health: '/health',
      generateFeedback: '/generate-feedback'
    }
  });
});

app.get('/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Feedback generation endpoint
app.post('/generate-feedback', (req, res) => {
  try {
    const { studentData, criteria = {} } = req.body;
    
    // Validate input data
    const studentValidation = Validator.validateStudentData(studentData);
    if (!studentValidation.isValid) {
      return res.status(400).json({
        error: 'Validation failed',
        details: studentValidation.errors
      });
    }
    
    const criteriaValidation = Validator.validateCriteria(criteria);
    if (!criteriaValidation.isValid) {
      return res.status(400).json({
        error: 'Validation failed',
        details: criteriaValidation.errors
      });
    }
    
    // Sanitize input
    const sanitizedStudentData = Validator.sanitizeInput(studentData);
    const sanitizedCriteria = Validator.sanitizeInput(criteria);
    
    // Generate feedback
    const feedback = feedbackGenerator.generateFeedback(sanitizedStudentData, sanitizedCriteria);
    
    res.json(feedback);
    
  } catch (error) {
    console.error('Error generating feedback:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: 'An unexpected error occurred while generating feedback'
    });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'Something went wrong!',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Internal server error'
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not found',
    message: `Route ${req.originalUrl} not found`
  });
});

app.listen(PORT, () => {
  console.log(`🚀 Auto-Feedback Generator server running on port ${PORT}`);
  console.log(`📚 API Documentation: http://localhost:${PORT}/`);
  console.log(`💚 Health Check: http://localhost:${PORT}/health`);
});

module.exports = app;