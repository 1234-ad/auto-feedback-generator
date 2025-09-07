"""
Auto Feedback Generator - Streamlit Frontend
Main Streamlit application for the feedback generator interface
"""

import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import pyperclip
from io import BytesIO
import os
from typing import Dict, Any

# Import utility functions
from utils.pdf_generator import generate_feedback_pdf
from utils.ui_components import (
    render_header, render_rubric_input, render_feedback_display,
    render_sidebar, show_success_message, show_error_message
)

# Page configuration
st.set_page_config(
    page_title="Auto Feedback Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .feedback-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .rubric-input {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #5a6fd8 0%, #6a4190 100%);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'feedback_history' not in st.session_state:
    st.session_state.feedback_history = []

if 'current_feedback' not in st.session_state:
    st.session_state.current_feedback = None

# Configuration
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000')

def main():
    """Main application function"""
    
    # Render header
    render_header()
    
    # Sidebar
    render_sidebar()
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📋 Student Information & Rubric")
        
        # Student information form
        with st.form("feedback_form"):
            student_name = st.text_input(
                "Student Name *",
                placeholder="Enter student's full name",
                help="The name of the student receiving feedback"
            )
            
            assignment_title = st.text_input(
                "Assignment Title",
                placeholder="e.g., Math Quiz 1, Science Project",
                help="Title or name of the assignment being evaluated"
            )
            
            subject = st.selectbox(
                "Subject",
                options=[
                    "General", "Mathematics", "Science", "English", 
                    "History", "Art", "Physical Education"
                ],
                help="Subject area for context-appropriate feedback"
            )
            
            feedback_type = st.selectbox(
                "Feedback Type",
                options=["constructive", "encouraging", "detailed", "brief"],
                help="Style of feedback to generate"
            )
            
            st.subheader("📊 Rubric Scores")
            st.write("Add evaluation criteria and scores:")
            
            # Dynamic rubric input
            rubric_data = render_rubric_input()
            
            # Form submission
            submitted = st.form_submit_button(
                "🚀 Generate Feedback",
                use_container_width=True
            )
            
            if submitted:
                if student_name and rubric_data:
                    generate_feedback(
                        student_name, assignment_title, subject, 
                        feedback_type, rubric_data
                    )
                else:
                    show_error_message("Please fill in student name and at least one rubric criterion.")
    
    with col2:
        st.header("💬 Generated Feedback")
        
        if st.session_state.current_feedback:
            render_feedback_display(st.session_state.current_feedback)
        else:
            st.info("👈 Fill out the form and click 'Generate Feedback' to see results here.")
            
            # Show sample feedback
            st.subheader("📝 Sample Feedback")
            st.markdown("""
            **Sample for Alex Johnson - Science Project:**
            
            *Great work on your science project, Alex! Your research quality was excellent, showing thorough investigation and reliable sources. Your analysis demonstrated strong critical thinking skills. 
            
            For future projects, consider enhancing your presentation skills by practicing your delivery and making more eye contact with the audience. Your collaboration could also be strengthened by taking more initiative in group discussions.
            
            Keep up the excellent analytical work - it's one of your strongest skills!*
            """)
    
    # Feedback history
    if st.session_state.feedback_history:
        st.header("📚 Feedback History")
        
        for i, feedback in enumerate(reversed(st.session_state.feedback_history[-5:])):
            with st.expander(f"{feedback['student_name']} - {feedback['assignment_title']} ({feedback['timestamp']})"):
                st.write(feedback['feedback'])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button(f"📋 Copy", key=f"copy_{i}"):
                        copy_to_clipboard(feedback['feedback'])
                        st.success("Copied to clipboard!")
                
                with col2:
                    pdf_data = generate_feedback_pdf(feedback)
                    st.download_button(
                        "📄 Download PDF",
                        data=pdf_data,
                        file_name=f"feedback_{feedback['student_name'].replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        key=f"download_{i}"
                    )

def generate_feedback(student_name: str, assignment_title: str, subject: str, 
                     feedback_type: str, rubric_data: Dict[str, Any]):
    """Generate feedback using the backend API"""
    
    with st.spinner("🤖 Generating personalized feedback..."):
        try:
            # Prepare request data
            request_data = {
                "student_name": student_name,
                "assignment_title": assignment_title or "Assignment",
                "subject": subject,
                "feedback_type": feedback_type,
                "rubric_data": rubric_data
            }
            
            # Call backend API
            response = requests.post(
                f"{BACKEND_URL}/api/generate-feedback",
                json=request_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('success'):
                    feedback_data = {
                        'student_name': student_name,
                        'assignment_title': assignment_title or "Assignment",
                        'subject': subject,
                        'feedback_type': feedback_type,
                        'feedback': result['feedback'],
                        'rubric_data': rubric_data,
                        'metadata': result.get('metadata', {}),
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    
                    # Store in session state
                    st.session_state.current_feedback = feedback_data
                    st.session_state.feedback_history.append(feedback_data)
                    
                    show_success_message("✅ Feedback generated successfully!")
                    st.rerun()
                else:
                    show_error_message(f"Failed to generate feedback: {result.get('error', 'Unknown error')}")
            
            else:
                error_data = response.json() if response.content else {}
                error_message = error_data.get('message', f'HTTP {response.status_code} error')
                show_error_message(f"API Error: {error_message}")
                
        except requests.exceptions.Timeout:
            show_error_message("⏰ Request timeout. Please try again.")
        except requests.exceptions.ConnectionError:
            show_error_message("🔌 Cannot connect to backend. Please check if the server is running.")
        except Exception as e:
            show_error_message(f"❌ Unexpected error: {str(e)}")

def copy_to_clipboard(text: str):
    """Copy text to clipboard"""
    try:
        pyperclip.copy(text)
        return True
    except:
        return False

def test_backend_connection():
    """Test connection to backend API"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
        return response.status_code == 200
    except:
        return False

# Sidebar content
def render_app_sidebar():
    """Render sidebar content"""
    st.sidebar.title("🎯 Quick Actions")
    
    # Backend status
    if test_backend_connection():
        st.sidebar.success("✅ Backend Connected")
    else:
        st.sidebar.error("❌ Backend Disconnected")
        st.sidebar.write(f"Backend URL: {BACKEND_URL}")
    
    # Clear history
    if st.sidebar.button("🗑️ Clear History"):
        st.session_state.feedback_history = []
        st.session_state.current_feedback = None
        st.success("History cleared!")
        st.rerun()
    
    # Export all feedback
    if st.session_state.feedback_history:
        if st.sidebar.button("📊 Export All as CSV"):
            df = pd.DataFrame(st.session_state.feedback_history)
            csv = df.to_csv(index=False)
            st.sidebar.download_button(
                "Download CSV",
                data=csv,
                file_name=f"feedback_history_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    # Instructions
    st.sidebar.markdown("---")
    st.sidebar.subheader("📖 How to Use")
    st.sidebar.markdown("""
    1. **Enter student information** - Name and assignment details
    2. **Add rubric criteria** - Click '+' to add evaluation criteria
    3. **Set scores** - Enter scores for each criterion
    4. **Choose feedback style** - Select the type of feedback
    5. **Generate** - Click the button to create feedback
    6. **Copy or Download** - Use the feedback as needed
    """)
    
    # Tips
    st.sidebar.markdown("---")
    st.sidebar.subheader("💡 Tips")
    st.sidebar.markdown("""
    - Use specific criterion names (e.g., "Problem Solving" vs "Math")
    - Scores can be out of any maximum (e.g., 8/10, 15/20)
    - Try different feedback types for variety
    - Save important feedback using the download feature
    """)

if __name__ == "__main__":
    render_app_sidebar()
    main()