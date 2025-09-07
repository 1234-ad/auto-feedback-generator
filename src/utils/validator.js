/**
 * Input Validation Utilities
 * Author: Adithya
 */

class Validator {
  /**
   * Validate student data input
   * @param {Object} studentData - Student information to validate
   * @returns {Object} Validation result with errors if any
   */
  static validateStudentData(studentData) {
    const errors = [];
    const required = ['name', 'performance', 'subject'];
    
    // Check required fields
    required.forEach(field => {
      if (!studentData[field]) {
        errors.push(`${field} is required`);
      }
    });
    
    // Validate performance score
    if (studentData.performance !== undefined) {
      const performance = Number(studentData.performance);
      if (isNaN(performance) || performance < 0 || performance > 100) {
        errors.push('Performance must be a number between 0 and 100');
      }
    }
    
    // Validate name
    if (studentData.name && typeof studentData.name !== 'string') {
      errors.push('Name must be a string');
    }
    
    // Validate subject
    if (studentData.subject && typeof studentData.subject !== 'string') {
      errors.push('Subject must be a string');
    }
    
    // Validate arrays
    if (studentData.weakAreas && !Array.isArray(studentData.weakAreas)) {
      errors.push('Weak areas must be an array');
    }
    
    if (studentData.strengths && !Array.isArray(studentData.strengths)) {
      errors.push('Strengths must be an array');
    }
    
    return {
      isValid: errors.length === 0,
      errors: errors
    };
  }
  
  /**
   * Validate assessment criteria
   * @param {Object} criteria - Assessment criteria to validate
   * @returns {Object} Validation result
   */
  static validateCriteria(criteria) {
    const errors = [];
    
    if (!criteria || typeof criteria !== 'object') {
      errors.push('Criteria must be an object');
      return { isValid: false, errors };
    }
    
    // Validate rubric if provided
    if (criteria.rubric && typeof criteria.rubric !== 'object') {
      errors.push('Rubric must be an object');
    }
    
    // Validate weight if provided
    if (criteria.weight !== undefined) {
      const weight = Number(criteria.weight);
      if (isNaN(weight) || weight < 0 || weight > 1) {
        errors.push('Weight must be a number between 0 and 1');
      }
    }
    
    return {
      isValid: errors.length === 0,
      errors: errors
    };
  }
  
  /**
   * Sanitize input data
   * @param {Object} data - Data to sanitize
   * @returns {Object} Sanitized data
   */
  static sanitizeInput(data) {
    const sanitized = {};
    
    Object.keys(data).forEach(key => {
      if (typeof data[key] === 'string') {
        // Basic string sanitization
        sanitized[key] = data[key].trim().replace(/[<>]/g, '');
      } else {
        sanitized[key] = data[key];
      }
    });
    
    return sanitized;
  }
}

module.exports = Validator;