/**
 * Feedback Generator Service
 * Handles the core logic for generating personalized feedback
 * Author: Adithya
 */

class FeedbackGenerator {
  constructor() {
    this.feedbackTemplates = {
      excellent: "Outstanding work! {student} has demonstrated exceptional understanding of {topic}.",
      good: "Good progress! {student} shows solid grasp of {topic} with room for improvement in {areas}.",
      needsImprovement: "{student} needs additional support in {topic}. Consider focusing on {recommendations}."
    };
  }

  /**
   * Generate personalized feedback based on student performance
   * @param {Object} studentData - Student information and performance data
   * @param {Object} criteria - Assessment criteria and rubrics
   * @returns {Object} Generated feedback with recommendations
   */
  generateFeedback(studentData, criteria) {
    const { name, performance, subject, weakAreas, strengths } = studentData;
    
    // Determine performance level
    const performanceLevel = this.assessPerformance(performance);
    
    // Generate base feedback
    let feedback = this.getBaseTemplate(performanceLevel);
    
    // Personalize feedback
    feedback = this.personalizeFeedback(feedback, {
      student: name,
      topic: subject,
      areas: weakAreas?.join(', ') || 'general concepts',
      recommendations: this.generateRecommendations(weakAreas, strengths)
    });

    return {
      studentName: name,
      subject: subject,
      performanceLevel: performanceLevel,
      feedback: feedback,
      recommendations: this.generateDetailedRecommendations(studentData),
      nextSteps: this.generateNextSteps(performanceLevel, weakAreas),
      timestamp: new Date().toISOString()
    };
  }

  assessPerformance(performance) {
    if (performance >= 85) return 'excellent';
    if (performance >= 70) return 'good';
    return 'needsImprovement';
  }

  getBaseTemplate(level) {
    return this.feedbackTemplates[level] || this.feedbackTemplates.needsImprovement;
  }

  personalizeFeedback(template, data) {
    let personalizedFeedback = template;
    Object.keys(data).forEach(key => {
      personalizedFeedback = personalizedFeedback.replace(`{${key}}`, data[key]);
    });
    return personalizedFeedback;
  }

  generateRecommendations(weakAreas, strengths) {
    if (!weakAreas || weakAreas.length === 0) {
      return "Continue building on current strengths";
    }
    return `Focus on ${weakAreas.slice(0, 2).join(' and ')} while leveraging strengths in ${strengths?.join(' and ') || 'identified areas'}`;
  }

  generateDetailedRecommendations(studentData) {
    const { weakAreas, strengths, learningStyle } = studentData;
    
    const recommendations = [];
    
    if (weakAreas && weakAreas.length > 0) {
      recommendations.push(`Target improvement areas: ${weakAreas.join(', ')}`);
    }
    
    if (strengths && strengths.length > 0) {
      recommendations.push(`Build upon strengths: ${strengths.join(', ')}`);
    }
    
    if (learningStyle) {
      recommendations.push(`Adapt teaching methods for ${learningStyle} learning style`);
    }
    
    return recommendations;
  }

  generateNextSteps(performanceLevel, weakAreas) {
    const steps = [];
    
    switch (performanceLevel) {
      case 'excellent':
        steps.push('Explore advanced topics and challenges');
        steps.push('Consider peer tutoring opportunities');
        break;
      case 'good':
        steps.push('Practice additional exercises in identified areas');
        steps.push('Seek clarification on challenging concepts');
        break;
      case 'needsImprovement':
        steps.push('Schedule additional support sessions');
        steps.push('Review fundamental concepts');
        if (weakAreas && weakAreas.length > 0) {
          steps.push(`Focus specifically on: ${weakAreas.slice(0, 2).join(' and ')}`);
        }
        break;
    }
    
    return steps;
  }
}

module.exports = FeedbackGenerator;