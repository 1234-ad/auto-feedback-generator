#!/usr/bin/env python3
"""
Prompt Testing and Optimization Script
Test different prompt templates and analyze feedback quality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from utils.prompt_templates import PromptTemplates
from services.feedback_service import FeedbackService
import json
from typing import Dict, List, Any

def test_prompt_templates():
    """Test all available prompt templates"""
    
    print("🧪 Testing Prompt Templates")
    print("=" * 50)
    
    templates = PromptTemplates()
    
    # Sample data for testing
    sample_data = {
        'student_name': 'Alex Johnson',
        'assignment_title': 'Research Project',
        'subject': 'Science',
        'rubric_data': {
            'research_quality': {'score': 8, 'max_score': 10},
            'presentation': {'score': 7, 'max_score': 10},
            'analysis': {'score': 9, 'max_score': 10},
            'collaboration': {'score': 6, 'max_score': 10}
        }
    }
    
    feedback_types = ['constructive', 'encouraging', 'detailed', 'brief']
    subjects = ['Mathematics', 'Science', 'English', 'History', 'Art', 'Physical Education', 'General']
    
    print("📋 Available Templates:")
    for feedback_type in feedback_types:
        print(f"  • {feedback_type.title()}")
    
    print(f"\n📚 Available Subjects:")
    for subject in subjects:
        print(f"  • {subject}")
    
    print(f"\n🎯 Testing with sample data:")
    print(f"Student: {sample_data['student_name']}")
    print(f"Assignment: {sample_data['assignment_title']}")
    print(f"Rubric: {len(sample_data['rubric_data'])} criteria")
    
    # Test each feedback type with Science subject
    print(f"\n🔬 Testing all feedback types for Science:")
    for feedback_type in feedback_types:
        print(f"\n--- {feedback_type.upper()} FEEDBACK ---")
        template = templates.get_template(feedback_type, 'Science')
        
        # Format the template with sample data
        rubric_text = format_rubric_for_prompt(sample_data['rubric_data'])
        formatted_prompt = template.format(
            student_name=sample_data['student_name'],
            assignment_title=sample_data['assignment_title'],
            subject='Science',
            rubric_data=rubric_text
        )
        
        print(f"Template length: {len(formatted_prompt)} characters")
        print(f"Preview: {formatted_prompt[:200]}...")
        
        # Analyze template structure
        analyze_template_structure(formatted_prompt)

def format_rubric_for_prompt(rubric_data: Dict[str, Any]) -> str:
    """Format rubric data for prompt templates"""
    rubric_lines = []
    
    for criterion, data in rubric_data.items():
        score = data['score']
        max_score = data['max_score']
        percentage = (score / max_score) * 100
        
        rubric_lines.append(
            f"- {criterion.replace('_', ' ').title()}: {score}/{max_score} ({percentage:.0f}%)"
        )
    
    return "\\n".join(rubric_lines)

def analyze_template_structure(template: str):
    """Analyze the structure and content of a template"""
    
    # Count placeholders
    placeholders = ['{student_name}', '{assignment_title}', '{subject}', '{rubric_data}']
    placeholder_count = sum(template.count(placeholder) for placeholder in placeholders)
    
    # Count words and sentences
    word_count = len(template.split())
    sentence_count = template.count('.') + template.count('!') + template.count('?')
    
    # Check for key instruction words
    instruction_words = ['analyze', 'provide', 'generate', 'address', 'focus', 'emphasize']
    instruction_count = sum(template.lower().count(word) for word in instruction_words)
    
    print(f"  📊 Analysis:")
    print(f"    • Placeholders: {placeholder_count}")
    print(f"    • Words: {word_count}")
    print(f"    • Sentences: {sentence_count}")
    print(f"    • Instruction words: {instruction_count}")

def test_subject_variations():
    """Test how templates vary across different subjects"""
    
    print(f"\n🎨 Testing Subject Variations")
    print("-" * 40)
    
    templates = PromptTemplates()
    subjects = ['Mathematics', 'Science', 'English', 'Art']
    
    for subject in subjects:
        print(f"\n📖 {subject.upper()} TEMPLATE:")
        template = templates.get_template('constructive', subject)
        
        # Extract subject-specific content
        lines = template.split('\\n')
        subject_specific_lines = [line for line in lines if subject.lower() in line.lower() or 'specific' in line.lower()]
        
        if subject_specific_lines:
            print("  Subject-specific content found:")
            for line in subject_specific_lines[:3]:  # Show first 3 relevant lines
                print(f"    • {line.strip()}")
        else:
            print("  No obvious subject-specific content detected")

def compare_feedback_lengths():
    """Compare expected feedback lengths across different types"""
    
    print(f"\n📏 Feedback Length Analysis")
    print("-" * 30)
    
    templates = PromptTemplates()
    feedback_types = ['constructive', 'encouraging', 'detailed', 'brief']
    
    expected_lengths = {
        'constructive': '150-250 words',
        'encouraging': '120-200 words',
        'detailed': '250-400 words',
        'brief': '80-120 words'
    }
    
    for feedback_type in feedback_types:
        template = templates.get_template(feedback_type, 'General')
        
        # Look for length specifications in template
        length_mentions = []
        if 'word' in template.lower():
            words = template.lower().split()
            for i, word in enumerate(words):
                if 'word' in word and i > 0:
                    if words[i-1].isdigit() or '-' in words[i-1]:
                        length_mentions.append(f"{words[i-1]} {word}")
        
        print(f"{feedback_type.title()}:")
        print(f"  Expected: {expected_lengths[feedback_type]}")
        if length_mentions:
            print(f"  Template specifies: {', '.join(length_mentions)}")
        else:
            print(f"  Template: No specific length mentioned")

def test_prompt_effectiveness():
    """Test prompt effectiveness with sample scenarios"""
    
    print(f"\n🎯 Prompt Effectiveness Testing")
    print("-" * 35)
    
    # Test scenarios with different performance levels
    scenarios = [
        {
            'name': 'High Performer',
            'rubric': {
                'criterion_1': {'score': 9, 'max_score': 10},
                'criterion_2': {'score': 8, 'max_score': 10},
                'criterion_3': {'score': 9, 'max_score': 10}
            }
        },
        {
            'name': 'Average Performer',
            'rubric': {
                'criterion_1': {'score': 7, 'max_score': 10},
                'criterion_2': {'score': 6, 'max_score': 10},
                'criterion_3': {'score': 7, 'max_score': 10}
            }
        },
        {
            'name': 'Struggling Student',
            'rubric': {
                'criterion_1': {'score': 4, 'max_score': 10},
                'criterion_2': {'score': 5, 'max_score': 10},
                'criterion_3': {'score': 3, 'max_score': 10}
            }
        }
    ]
    
    templates = PromptTemplates()
    
    for scenario in scenarios:
        print(f"\n👤 {scenario['name']}:")
        
        # Calculate overall performance
        total_score = sum(item['score'] for item in scenario['rubric'].values())
        total_max = sum(item['max_score'] for item in scenario['rubric'].values())
        percentage = (total_score / total_max) * 100
        
        print(f"  Overall Performance: {percentage:.1f}%")
        
        # Test with encouraging feedback for struggling students
        feedback_type = 'encouraging' if percentage < 60 else 'constructive'
        template = templates.get_template(feedback_type, 'General')
        
        print(f"  Recommended feedback type: {feedback_type}")
        print(f"  Template focuses on: ", end="")
        
        # Analyze template focus
        if 'strength' in template.lower():
            print("strengths, ", end="")
        if 'improve' in template.lower():
            print("improvements, ", end="")
        if 'encourage' in template.lower():
            print("encouragement, ", end="")
        if 'potential' in template.lower():
            print("potential", end="")
        print()

def generate_sample_prompts():
    """Generate sample prompts for documentation"""
    
    print(f"\n📝 Sample Prompt Generation")
    print("-" * 30)
    
    templates = PromptTemplates()
    
    sample_data = {
        'student_name': 'Sarah Thompson',
        'assignment_title': 'Environmental Science Report',
        'subject': 'Science',
        'rubric_data': {
            'research_depth': {'score': 8, 'max_score': 10},
            'data_analysis': {'score': 7, 'max_score': 10},
            'conclusions': {'score': 9, 'max_score': 10},
            'presentation': {'score': 6, 'max_score': 10}
        }
    }
    
    rubric_text = format_rubric_for_prompt(sample_data['rubric_data'])
    
    print("📋 Sample Prompt (Constructive Feedback):")
    print("-" * 45)
    
    template = templates.get_template('constructive', 'Science')
    formatted_prompt = template.format(
        student_name=sample_data['student_name'],
        assignment_title=sample_data['assignment_title'],
        subject=sample_data['subject'],
        rubric_data=rubric_text
    )
    
    print(formatted_prompt)
    
    # Save to file for documentation
    with open('sample_prompt.txt', 'w') as f:
        f.write("SAMPLE PROMPT FOR DOCUMENTATION\\n")
        f.write("=" * 40 + "\\n\\n")
        f.write(formatted_prompt)
    
    print(f"\\n💾 Sample prompt saved to 'sample_prompt.txt'")

def main():
    """Main testing function"""
    
    print("🧪 Auto Feedback Generator - Prompt Testing Suite")
    print("=" * 60)
    
    try:
        # Run all tests
        test_prompt_templates()
        test_subject_variations()
        compare_feedback_lengths()
        test_prompt_effectiveness()
        generate_sample_prompts()
        
        print(f"\\n✅ All prompt tests completed successfully!")
        print("💡 Use these insights to optimize your feedback generation.")
        
    except Exception as e:
        print(f"\\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()