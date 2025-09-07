"""
Prompt Templates - Engineered prompts for different feedback types and subjects
"""

class PromptTemplates:
    def __init__(self):
        """Initialize prompt templates for different feedback scenarios"""
        self.base_templates = {
            'constructive': self._constructive_template(),
            'encouraging': self._encouraging_template(),
            'detailed': self._detailed_template(),
            'brief': self._brief_template()
        }
        
        self.subject_modifiers = {
            'Mathematics': self._math_modifier(),
            'Science': self._science_modifier(),
            'English': self._english_modifier(),
            'History': self._history_modifier(),
            'Art': self._art_modifier(),
            'Physical Education': self._pe_modifier(),
            'General': self._general_modifier()
        }
    
    def get_template(self, feedback_type: str, subject: str) -> str:
        """
        Get the appropriate template based on feedback type and subject
        
        Args:
            feedback_type: Type of feedback (constructive, encouraging, etc.)
            subject: Subject area
            
        Returns:
            Formatted prompt template
        """
        base_template = self.base_templates.get(feedback_type, self.base_templates['constructive'])
        subject_modifier = self.subject_modifiers.get(subject, self.subject_modifiers['General'])
        
        return base_template + "\\n\\n" + subject_modifier
    
    def _constructive_template(self) -> str:
        """Template for constructive feedback"""
        return """
You are an experienced educator providing constructive feedback to a student. Based on the rubric scores provided, generate personalized, actionable feedback that:

1. Acknowledges the student's strengths
2. Identifies specific areas for improvement
3. Provides concrete suggestions for enhancement
4. Maintains an encouraging and supportive tone
5. Is appropriate for the educational level

Student: {student_name}
Assignment: {assignment_title}
Subject: {subject}

Rubric Scores:
{rubric_data}

Please provide feedback that is:
- Specific and actionable
- Balanced (highlighting both strengths and areas for improvement)
- Encouraging and motivational
- Professional yet warm in tone
- Approximately 150-250 words

Format the feedback as a cohesive paragraph or two, addressing the student directly.
"""
    
    def _encouraging_template(self) -> str:
        """Template for encouraging feedback"""
        return """
You are a supportive educator focused on building student confidence. Based on the rubric scores, generate encouraging feedback that:

1. Celebrates achievements and progress
2. Frames challenges as growth opportunities
3. Builds confidence and motivation
4. Provides gentle guidance for improvement
5. Emphasizes the student's potential

Student: {student_name}
Assignment: {assignment_title}
Subject: {subject}

Rubric Scores:
{rubric_data}

Please provide feedback that is:
- Highly encouraging and positive
- Focuses on growth and potential
- Acknowledges effort and progress
- Provides supportive suggestions
- Builds confidence
- Approximately 120-200 words

Use an uplifting, motivational tone throughout.
"""
    
    def _detailed_template(self) -> str:
        """Template for detailed feedback"""
        return """
You are a thorough educator providing comprehensive feedback. Based on the rubric scores, generate detailed feedback that:

1. Analyzes each rubric criterion specifically
2. Provides in-depth commentary on performance
3. Offers detailed improvement strategies
4. Explains the reasoning behind scores
5. Gives comprehensive guidance for future work

Student: {student_name}
Assignment: {assignment_title}
Subject: {subject}

Rubric Scores:
{rubric_data}

Please provide feedback that is:
- Comprehensive and thorough
- Addresses each rubric criterion
- Provides detailed explanations
- Offers specific improvement strategies
- Maintains professional tone
- Approximately 250-400 words

Structure the feedback with clear sections for each major area.
"""
    
    def _brief_template(self) -> str:
        """Template for brief feedback"""
        return """
You are an efficient educator providing concise feedback. Based on the rubric scores, generate brief but meaningful feedback that:

1. Highlights key strengths
2. Identifies main areas for improvement
3. Provides essential guidance
4. Maintains encouraging tone
5. Is clear and to the point

Student: {student_name}
Assignment: {assignment_title}
Subject: {subject}

Rubric Scores:
{rubric_data}

Please provide feedback that is:
- Concise but meaningful
- Highlights key points only
- Maintains positive tone
- Provides essential guidance
- Approximately 80-120 words

Keep it brief but impactful.
"""
    
    def _math_modifier(self) -> str:
        """Subject-specific modifier for Mathematics"""
        return """
Mathematics-specific considerations:
- Focus on problem-solving approaches and mathematical reasoning
- Address computational accuracy and method selection
- Emphasize understanding of concepts over memorization
- Suggest practice strategies for skill development
- Use mathematical terminology appropriately
"""
    
    def _science_modifier(self) -> str:
        """Subject-specific modifier for Science"""
        return """
Science-specific considerations:
- Emphasize scientific method and inquiry skills
- Address experimental design and data analysis
- Focus on understanding of scientific concepts and principles
- Encourage curiosity and further exploration
- Use scientific vocabulary and terminology
"""
    
    def _english_modifier(self) -> str:
        """Subject-specific modifier for English"""
        return """
English-specific considerations:
- Focus on writing clarity, organization, and style
- Address reading comprehension and analysis skills
- Emphasize grammar, vocabulary, and language mechanics
- Encourage creative expression and critical thinking
- Suggest reading and writing improvement strategies
"""
    
    def _history_modifier(self) -> str:
        """Subject-specific modifier for History"""
        return """
History-specific considerations:
- Emphasize critical analysis of historical sources
- Address understanding of cause and effect relationships
- Focus on chronological thinking and historical context
- Encourage connections between past and present
- Use historical terminology and concepts appropriately
"""
    
    def _art_modifier(self) -> str:
        """Subject-specific modifier for Art"""
        return """
Art-specific considerations:
- Focus on creativity, originality, and artistic expression
- Address technical skills and use of materials/tools
- Emphasize visual composition and design principles
- Encourage artistic exploration and risk-taking
- Appreciate individual artistic voice and style
"""
    
    def _pe_modifier(self) -> str:
        """Subject-specific modifier for Physical Education"""
        return """
Physical Education-specific considerations:
- Focus on skill development and physical improvement
- Address teamwork, sportsmanship, and cooperation
- Emphasize effort, participation, and attitude
- Encourage healthy lifestyle choices
- Recognize individual progress and achievement
"""
    
    def _general_modifier(self) -> str:
        """General modifier for all subjects"""
        return """
General considerations:
- Maintain age-appropriate language and expectations
- Focus on learning process and growth mindset
- Encourage continued effort and engagement
- Provide actionable next steps
- Build confidence while promoting improvement
"""
    
    def get_sample_prompts(self) -> dict:
        """Get sample prompts for testing and demonstration"""
        return {
            'sample_data': {
                'student_name': 'Alex Johnson',
                'assignment_title': 'Research Project',
                'subject': 'Science',
                'rubric_data': {
                    'research_quality': {'score': 8, 'max_score': 10},
                    'presentation': {'score': 7, 'max_score': 10},
                    'analysis': {'score': 9, 'max_score': 10},
                    'collaboration': {'score': 6, 'max_score': 10}
                }
            },
            'expected_elements': [
                'Student name mentioned',
                'Specific rubric criteria addressed',
                'Balanced feedback (strengths and improvements)',
                'Actionable suggestions',
                'Encouraging tone',
                'Subject-appropriate language'
            ]
        }