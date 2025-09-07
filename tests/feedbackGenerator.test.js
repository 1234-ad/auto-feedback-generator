/**
 * Tests for Feedback Generator Service
 * Author: Adithya
 */

const FeedbackGenerator = require('../src/services/feedbackGenerator');

describe('FeedbackGenerator', () => {
  let generator;

  beforeEach(() => {
    generator = new FeedbackGenerator();
  });

  describe('generateFeedback', () => {
    test('should generate feedback for excellent performance', () => {
      const studentData = {
        name: 'John Doe',
        performance: 90,
        subject: 'Mathematics',
        weakAreas: [],
        strengths: ['Problem solving', 'Analytical thinking']
      };

      const criteria = {
        rubric: { excellence: 85, good: 70, improvement: 50 }
      };

      const result = generator.generateFeedback(studentData, criteria);

      expect(result.studentName).toBe('John Doe');
      expect(result.subject).toBe('Mathematics');
      expect(result.performanceLevel).toBe('excellent');
      expect(result.feedback).toContain('Outstanding work!');
      expect(result.recommendations).toBeDefined();
      expect(result.nextSteps).toBeDefined();
    });

    test('should generate feedback for good performance', () => {
      const studentData = {
        name: 'Jane Smith',
        performance: 75,
        subject: 'Science',
        weakAreas: ['Lab procedures'],
        strengths: ['Theory understanding']
      };

      const criteria = {};

      const result = generator.generateFeedback(studentData, criteria);

      expect(result.performanceLevel).toBe('good');
      expect(result.feedback).toContain('Good progress!');
      expect(result.recommendations).toContain('Lab procedures');
    });

    test('should generate feedback for needs improvement', () => {
      const studentData = {
        name: 'Bob Johnson',
        performance: 60,
        subject: 'English',
        weakAreas: ['Grammar', 'Vocabulary'],
        strengths: ['Creative writing']
      };

      const criteria = {};

      const result = generator.generateFeedback(studentData, criteria);

      expect(result.performanceLevel).toBe('needsImprovement');
      expect(result.feedback).toContain('needs additional support');
      expect(result.nextSteps).toContain('Schedule additional support sessions');
    });
  });

  describe('assessPerformance', () => {
    test('should correctly assess performance levels', () => {
      expect(generator.assessPerformance(90)).toBe('excellent');
      expect(generator.assessPerformance(75)).toBe('good');
      expect(generator.assessPerformance(60)).toBe('needsImprovement');
    });
  });

  describe('generateRecommendations', () => {
    test('should generate recommendations based on weak areas', () => {
      const weakAreas = ['Grammar', 'Spelling'];
      const strengths = ['Creative writing'];
      
      const recommendations = generator.generateRecommendations(weakAreas, strengths);
      
      expect(recommendations).toContain('Grammar');
      expect(recommendations).toContain('Creative writing');
    });

    test('should handle empty weak areas', () => {
      const recommendations = generator.generateRecommendations([], ['Math']);
      
      expect(recommendations).toContain('Continue building');
    });
  });
});