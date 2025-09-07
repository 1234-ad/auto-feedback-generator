#!/usr/bin/env python3
"""
Sample Usage Examples for Auto Feedback Generator
Demonstrates how to use the API programmatically
"""

import requests
import json
import time
from typing import Dict, Any

# Configuration
BACKEND_URL = "http://localhost:5000"

def test_api_connection():
    """Test if the API is running and accessible"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is running and accessible")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the backend is running.")
        return False
    except Exception as e:
        print(f"❌ Error testing API: {str(e)}")
        return False

def generate_feedback_example(student_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate feedback for a student
    
    Args:
        student_data: Dictionary containing student information and rubric data
        
    Returns:
        API response dictionary
    """
    try:
        print(f"🤖 Generating feedback for {student_data['student_name']}...")
        
        response = requests.post(
            f"{BACKEND_URL}/api/generate-feedback",
            json=student_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Feedback generated successfully!")
            return result
        else:
            error_data = response.json() if response.content else {}
            print(f"❌ Error: {response.status_code}")
            print(f"Message: {error_data.get('message', 'Unknown error')}")
            return {"success": False, "error": error_data}
            
    except requests.exceptions.Timeout:
        print("⏰ Request timeout. The API might be processing...")
        return {"success": False, "error": "Timeout"}
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return {"success": False, "error": str(e)}

def main():
    """Main demonstration function"""
    
    print("🎓 Auto Feedback Generator - Sample Usage")
    print("=" * 50)
    
    # Test API connection
    if not test_api_connection():
        print("Please start the backend server first: python run_backend.py")
        return
    
    print()
    
    # Example 1: Mathematics feedback
    print("📊 Example 1: Mathematics Assignment")
    math_student = {
        "student_name": "Alice Johnson",
        "assignment_title": "Algebra Quiz 1",
        "subject": "Mathematics",
        "feedback_type": "constructive",
        "rubric_data": {
            "problem_solving": {"score": 8, "max_score": 10},
            "computational_accuracy": {"score": 9, "max_score": 10},
            "showing_work": {"score": 6, "max_score": 10},
            "communication": {"score": 7, "max_score": 10}
        }
    }
    
    result1 = generate_feedback_example(math_student)
    if result1.get("success"):
        print("📝 Generated Feedback:")
        print(f'"{result1["feedback"]}"')
        print()
    
    time.sleep(2)  # Rate limiting courtesy
    
    # Example 2: Science project feedback
    print("🔬 Example 2: Science Project")
    science_student = {
        "student_name": "Bob Chen",
        "assignment_title": "Solar System Model",
        "subject": "Science",
        "feedback_type": "encouraging",
        "rubric_data": {
            "research_quality": {"score": 7, "max_score": 10},
            "creativity": {"score": 9, "max_score": 10},
            "presentation": {"score": 6, "max_score": 10},
            "scientific_accuracy": {"score": 8, "max_score": 10}
        }
    }
    
    result2 = generate_feedback_example(science_student)
    if result2.get("success"):
        print("📝 Generated Feedback:")
        print(f'"{result2["feedback"]}"')
        print()
    
    time.sleep(2)  # Rate limiting courtesy
    
    # Example 3: English essay feedback
    print("📚 Example 3: English Essay")
    english_student = {
        "student_name": "Carol Martinez",
        "assignment_title": "Persuasive Essay",
        "subject": "English",
        "feedback_type": "detailed",
        "rubric_data": {
            "thesis_clarity": {"score": 8, "max_score": 10},
            "evidence_support": {"score": 7, "max_score": 10},
            "organization": {"score": 9, "max_score": 10},
            "grammar_mechanics": {"score": 6, "max_score": 10},
            "voice_style": {"score": 8, "max_score": 10}
        }
    }
    
    result3 = generate_feedback_example(english_student)
    if result3.get("success"):
        print("📝 Generated Feedback:")
        print(f'"{result3["feedback"]}"')
        print()
    
    time.sleep(2)  # Rate limiting courtesy
    
    # Example 4: Brief feedback
    print("⚡ Example 4: Brief Feedback Style")
    brief_student = {
        "student_name": "David Kim",
        "assignment_title": "History Timeline",
        "subject": "History",
        "feedback_type": "brief",
        "rubric_data": {
            "historical_accuracy": {"score": 9, "max_score": 10},
            "timeline_organization": {"score": 8, "max_score": 10},
            "visual_presentation": {"score": 7, "max_score": 10}
        }
    }
    
    result4 = generate_feedback_example(brief_student)
    if result4.get("success"):
        print("📝 Generated Feedback:")
        print(f'"{result4["feedback"]}"')
        print()
    
    # Get available templates
    print("📋 Available Templates and Options:")
    try:
        response = requests.get(f"{BACKEND_URL}/api/feedback-templates")
        if response.status_code == 200:
            templates = response.json()
            print(f"Feedback Types: {', '.join(templates['feedback_types'])}")
            print(f"Subjects: {', '.join(templates['subjects'])}")
        else:
            print("Could not retrieve template information")
    except Exception as e:
        print(f"Error getting templates: {str(e)}")
    
    print("\n🎉 Sample usage completed!")
    print("💡 Tip: Modify the rubric_data and other parameters to see different feedback styles.")

def batch_feedback_example():
    """Example of generating feedback for multiple students"""
    
    print("\n📊 Batch Feedback Generation Example")
    print("-" * 40)
    
    students = [
        {
            "student_name": "Emma Wilson",
            "assignment_title": "Art Project",
            "subject": "Art",
            "feedback_type": "encouraging",
            "rubric_data": {
                "creativity": {"score": 9, "max_score": 10},
                "technique": {"score": 7, "max_score": 10},
                "effort": {"score": 8, "max_score": 10}
            }
        },
        {
            "student_name": "Frank Rodriguez",
            "assignment_title": "PE Skills Assessment",
            "subject": "Physical Education",
            "feedback_type": "constructive",
            "rubric_data": {
                "skill_demonstration": {"score": 6, "max_score": 10},
                "teamwork": {"score": 9, "max_score": 10},
                "effort": {"score": 8, "max_score": 10},
                "sportsmanship": {"score": 10, "max_score": 10}
            }
        }
    ]
    
    for i, student in enumerate(students, 1):
        print(f"\n👤 Student {i}: {student['student_name']}")
        result = generate_feedback_example(student)
        
        if result.get("success"):
            print("✅ Success")
            # In a real application, you might save this to a file or database
        else:
            print("❌ Failed")
        
        # Rate limiting - wait between requests
        if i < len(students):
            time.sleep(2)

def error_handling_examples():
    """Demonstrate error handling scenarios"""
    
    print("\n🚨 Error Handling Examples")
    print("-" * 30)
    
    # Example 1: Missing required field
    print("1. Missing student name:")
    invalid_data1 = {
        "assignment_title": "Test Assignment",
        "rubric_data": {
            "test_criterion": {"score": 8, "max_score": 10}
        }
    }
    generate_feedback_example(invalid_data1)
    
    time.sleep(1)
    
    # Example 2: Invalid score
    print("\n2. Invalid score (exceeds maximum):")
    invalid_data2 = {
        "student_name": "Test Student",
        "rubric_data": {
            "test_criterion": {"score": 15, "max_score": 10}  # Invalid!
        }
    }
    generate_feedback_example(invalid_data2)
    
    time.sleep(1)
    
    # Example 3: Invalid feedback type
    print("\n3. Invalid feedback type:")
    invalid_data3 = {
        "student_name": "Test Student",
        "feedback_type": "invalid_type",  # Invalid!
        "rubric_data": {
            "test_criterion": {"score": 8, "max_score": 10}
        }
    }
    generate_feedback_example(invalid_data3)

if __name__ == "__main__":
    main()
    
    # Uncomment to run additional examples
    # batch_feedback_example()
    # error_handling_examples()