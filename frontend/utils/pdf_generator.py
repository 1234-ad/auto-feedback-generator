"""
PDF Generator for Feedback Reports
Creates professional PDF documents from feedback data
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO
from datetime import datetime
from typing import Dict, Any

def generate_feedback_pdf(feedback_data: Dict[str, Any]) -> bytes:
    """
    Generate a PDF document from feedback data
    
    Args:
        feedback_data: Dictionary containing feedback information
        
    Returns:
        PDF document as bytes
    """
    
    # Create a BytesIO buffer
    buffer = BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#667eea')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.HexColor('#333333')
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        leading=18
    )
    
    info_style = ParagraphStyle(
        'InfoStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#666666')
    )
    
    # Build the document content
    story = []
    
    # Title
    story.append(Paragraph("📝 Student Feedback Report", title_style))
    story.append(Spacer(1, 20))
    
    # Student Information Table
    student_info = [
        ['Student Name:', feedback_data.get('student_name', 'N/A')],
        ['Assignment:', feedback_data.get('assignment_title', 'N/A')],
        ['Subject:', feedback_data.get('subject', 'N/A')],
        ['Feedback Type:', feedback_data.get('feedback_type', 'N/A').title()],
        ['Generated:', feedback_data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M'))]
    ]
    
    info_table = Table(student_info, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#333333')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e0e0e0')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(info_table)
    story.append(Spacer(1, 30))
    
    # Rubric Summary (if available)
    if 'rubric_data' in feedback_data and feedback_data['rubric_data']:
        story.append(Paragraph("📊 Rubric Scores", heading_style))
        
        rubric_data = feedback_data['rubric_data']
        rubric_table_data = [['Criterion', 'Score', 'Max Score', 'Percentage']]
        
        total_score = 0
        total_max = 0
        
        for criterion, data in rubric_data.items():
            criterion_name = criterion.replace('_', ' ').title()
            score = data['score']
            max_score = data['max_score']
            percentage = (score / max_score * 100) if max_score > 0 else 0
            
            total_score += score
            total_max += max_score
            
            rubric_table_data.append([
                criterion_name,
                f"{score:.1f}",
                f"{max_score:.1f}",
                f"{percentage:.1f}%"
            ])
        
        # Add total row
        overall_percentage = (total_score / total_max * 100) if total_max > 0 else 0
        rubric_table_data.append([
            'Overall',
            f"{total_score:.1f}",
            f"{total_max:.1f}",
            f"{overall_percentage:.1f}%"
        ])
        
        rubric_table = Table(rubric_table_data, colWidths=[2.5*inch, 1*inch, 1*inch, 1*inch])
        rubric_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            
            # Total row
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f8f9fa')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            
            # All cells
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e0e0e0')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        story.append(rubric_table)
        story.append(Spacer(1, 30))
    
    # Feedback Content
    story.append(Paragraph("💬 Personalized Feedback", heading_style))
    
    # Split feedback into paragraphs for better formatting
    feedback_text = feedback_data.get('feedback', 'No feedback available.')
    feedback_paragraphs = feedback_text.split('\n\n')
    
    for paragraph in feedback_paragraphs:
        if paragraph.strip():
            story.append(Paragraph(paragraph.strip(), body_style))
    
    story.append(Spacer(1, 30))
    
    # Footer
    footer_text = f"""
    <i>This feedback was generated using the Auto Feedback Generator - 
    an AI-powered tool designed to help educators provide personalized, 
    constructive feedback to students. Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}.</i>
    """
    story.append(Paragraph(footer_text, info_style))
    
    # Build the PDF
    doc.build(story)
    
    # Get the PDF data
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data

def generate_simple_feedback_pdf(student_name: str, feedback_text: str) -> bytes:
    """
    Generate a simple PDF with just student name and feedback
    
    Args:
        student_name: Name of the student
        feedback_text: Feedback content
        
    Returns:
        PDF document as bytes
    """
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    story = []
    
    # Title
    title = Paragraph(f"Feedback for {student_name}", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 20))
    
    # Feedback
    feedback = Paragraph(feedback_text, styles['Normal'])
    story.append(feedback)
    
    # Build PDF
    doc.build(story)
    
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data

def create_feedback_template() -> Dict[str, Any]:
    """
    Create a template for feedback data structure
    
    Returns:
        Template dictionary
    """
    return {
        'student_name': 'Student Name',
        'assignment_title': 'Assignment Title',
        'subject': 'Subject',
        'feedback_type': 'constructive',
        'feedback': 'Feedback content goes here...',
        'rubric_data': {
            'criterion_1': {'score': 8, 'max_score': 10},
            'criterion_2': {'score': 7, 'max_score': 10}
        },
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
    }