const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.get('/', (req, res) => {
  res.json({
    message: 'Auto-Feedback Generator API',
    version: '1.0.0',
    author: 'Adithya'
  });
});

app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// Feedback generation endpoint
app.post('/generate-feedback', (req, res) => {
  const { studentData, criteria } = req.body;
  
  // TODO: Implement feedback generation logic
  res.json({
    message: 'Feedback generation endpoint',
    studentData,
    criteria,
    feedback: 'Generated feedback will appear here'
  });
});

app.listen(PORT, () => {
  console.log(`Auto-Feedback Generator server running on port ${PORT}`);
});

module.exports = app;