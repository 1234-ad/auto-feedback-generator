"""
UI Components for Streamlit Frontend
Reusable UI components and helper functions
"""

import streamlit as st
from typing import Dict, Any, List
import plotly.express as px
import plotly.graph_objects as go

def render_header():
    """Render the main application header"""
    st.markdown("""
    <div class="main-header">
        <h1>🎓 Auto Feedback Generator</h1>
        <p>AI-Powered Personalized Feedback for Educators</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render sidebar with app information"""
    st.sidebar.title("📚 About")
    st.sidebar.markdown("""
    **Auto Feedback Generator** helps teachers create personalized, 
    constructive feedback for students based on rubric evaluations.
    
    **Features:**
    - 🤖 AI-powered feedback generation
    - 📊 Rubric-based evaluation
    - 📝 Multiple feedback styles
    - 📄 PDF export capability
    - 📋 Copy to clipboard
    """)

def render_rubric_input() -> Dict[str, Any]:
    """Render dynamic rubric input interface"""
    
    # Initialize rubric data in session state
    if 'rubric_criteria' not in st.session_state:
        st.session_state.rubric_criteria = [
            {"name": "Communication", "score": 8, "max_score": 10},
            {"name": "Teamwork", "score": 7, "max_score": 10}
        ]
    
    rubric_data = {}
    
    # Display existing criteria
    for i, criterion in enumerate(st.session_state.rubric_criteria):
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            criterion_name = st.text_input(
                f"Criterion {i+1}",
                value=criterion["name"],
                key=f"criterion_name_{i}",
                placeholder="e.g., Problem Solving"
            )
        
        with col2:
            score = st.number_input(
                "Score",
                min_value=0.0,
                max_value=100.0,
                value=float(criterion["score"]),
                step=0.5,
                key=f"score_{i}"
            )
        
        with col3:
            max_score = st.number_input(
                "Max",
                min_value=1.0,
                max_value=100.0,
                value=float(criterion["max_score"]),
                step=1.0,
                key=f"max_score_{i}"
            )
        
        with col4:
            if st.button("🗑️", key=f"delete_{i}", help="Delete this criterion"):
                st.session_state.rubric_criteria.pop(i)
                st.rerun()
        
        # Update session state
        st.session_state.rubric_criteria[i] = {
            "name": criterion_name,
            "score": score,
            "max_score": max_score
        }
        
        # Add to rubric data if name is provided
        if criterion_name.strip():
            rubric_data[criterion_name.lower().replace(" ", "_")] = {
                "score": score,
                "max_score": max_score
            }
    
    # Add new criterion button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("➕ Add Criterion"):
            st.session_state.rubric_criteria.append({
                "name": "",
                "score": 5,
                "max_score": 10
            })
            st.rerun()
    
    # Show rubric summary if data exists
    if rubric_data:
        render_rubric_summary(rubric_data)
    
    return rubric_data

def render_rubric_summary(rubric_data: Dict[str, Any]):
    """Render a visual summary of rubric scores"""
    
    st.subheader("📊 Rubric Summary")
    
    # Calculate overall statistics
    total_score = sum(item["score"] for item in rubric_data.values())
    total_max = sum(item["max_score"] for item in rubric_data.values())
    overall_percentage = (total_score / total_max * 100) if total_max > 0 else 0
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Score", f"{total_score:.1f}")
    
    with col2:
        st.metric("Max Possible", f"{total_max:.1f}")
    
    with col3:
        st.metric("Overall %", f"{overall_percentage:.1f}%")
    
    with col4:
        performance_level = get_performance_level(overall_percentage)
        st.metric("Level", performance_level)
    
    # Create visualization
    if len(rubric_data) > 1:
        create_rubric_chart(rubric_data)

def create_rubric_chart(rubric_data: Dict[str, Any]):
    """Create a chart visualization of rubric scores"""
    
    # Prepare data for chart
    criteria = []
    scores = []
    max_scores = []
    percentages = []
    
    for criterion, data in rubric_data.items():
        criteria.append(criterion.replace("_", " ").title())
        scores.append(data["score"])
        max_scores.append(data["max_score"])
        percentages.append((data["score"] / data["max_score"]) * 100)
    
    # Create bar chart
    fig = go.Figure()
    
    # Add bars for scores
    fig.add_trace(go.Bar(
        name='Score',
        x=criteria,
        y=scores,
        marker_color='#667eea',
        text=[f"{s:.1f}" for s in scores],
        textposition='auto',
    ))
    
    # Add bars for max scores (as background)
    fig.add_trace(go.Bar(
        name='Max Score',
        x=criteria,
        y=max_scores,
        marker_color='#e0e0e0',
        opacity=0.3,
        text=[f"/{m:.0f}" for m in max_scores],
        textposition='auto',
    ))
    
    fig.update_layout(
        title="Rubric Scores by Criterion",
        xaxis_title="Criteria",
        yaxis_title="Score",
        barmode='overlay',
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_feedback_display(feedback_data: Dict[str, Any]):
    """Render the generated feedback with actions"""
    
    st.markdown(f"""
    <div class="feedback-container">
        <h3>📝 Feedback for {feedback_data['student_name']}</h3>
        <p><strong>Assignment:</strong> {feedback_data['assignment_title']}</p>
        <p><strong>Subject:</strong> {feedback_data['subject']} | <strong>Type:</strong> {feedback_data['feedback_type'].title()}</p>
        <hr>
        <div style="font-size: 16px; line-height: 1.6;">
            {feedback_data['feedback']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Copy to Clipboard", use_container_width=True):
            try:
                import pyperclip
                pyperclip.copy(feedback_data['feedback'])
                st.success("✅ Copied to clipboard!")
            except:
                st.error("❌ Could not copy to clipboard")
    
    with col2:
        # Generate PDF
        from utils.pdf_generator import generate_feedback_pdf
        pdf_data = generate_feedback_pdf(feedback_data)
        
        st.download_button(
            "📄 Download PDF",
            data=pdf_data,
            file_name=f"feedback_{feedback_data['student_name'].replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    
    with col3:
        if st.button("✏️ Edit Feedback", use_container_width=True):
            st.session_state.edit_mode = True
    
    # Edit mode
    if st.session_state.get('edit_mode', False):
        st.subheader("✏️ Edit Feedback")
        edited_feedback = st.text_area(
            "Edit the feedback:",
            value=feedback_data['feedback'],
            height=200
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Changes"):
                feedback_data['feedback'] = edited_feedback
                st.session_state.current_feedback = feedback_data
                st.session_state.edit_mode = False
                st.success("✅ Feedback updated!")
                st.rerun()
        
        with col2:
            if st.button("❌ Cancel"):
                st.session_state.edit_mode = False
                st.rerun()
    
    # Show rubric summary
    if 'rubric_data' in feedback_data:
        with st.expander("📊 View Rubric Details"):
            render_rubric_summary(feedback_data['rubric_data'])

def show_success_message(message: str):
    """Show a success message"""
    st.success(message)

def show_error_message(message: str):
    """Show an error message"""
    st.error(message)

def show_info_message(message: str):
    """Show an info message"""
    st.info(message)

def show_warning_message(message: str):
    """Show a warning message"""
    st.warning(message)

def get_performance_level(percentage: float) -> str:
    """Get performance level based on percentage"""
    if percentage >= 90:
        return "🌟 Excellent"
    elif percentage >= 80:
        return "👍 Good"
    elif percentage >= 70:
        return "✅ Satisfactory"
    elif percentage >= 60:
        return "⚠️ Needs Improvement"
    else:
        return "🔴 Requires Attention"

def render_loading_spinner(message: str = "Processing..."):
    """Render a loading spinner with message"""
    with st.spinner(message):
        return True

def create_feedback_preview(rubric_data: Dict[str, Any]) -> str:
    """Create a preview of what the feedback might look like"""
    
    total_score = sum(item["score"] for item in rubric_data.values())
    total_max = sum(item["max_score"] for item in rubric_data.values())
    percentage = (total_score / total_max * 100) if total_max > 0 else 0
    
    # Find strengths and areas for improvement
    strengths = []
    improvements = []
    
    for criterion, data in rubric_data.items():
        criterion_percentage = (data["score"] / data["max_score"]) * 100
        criterion_name = criterion.replace("_", " ").title()
        
        if criterion_percentage >= 80:
            strengths.append(criterion_name)
        elif criterion_percentage < 70:
            improvements.append(criterion_name)
    
    preview = f"Based on the rubric scores ({percentage:.0f}% overall), "
    
    if strengths:
        preview += f"the feedback will highlight strengths in {', '.join(strengths[:2])}. "
    
    if improvements:
        preview += f"It will suggest improvements in {', '.join(improvements[:2])}."
    
    return preview