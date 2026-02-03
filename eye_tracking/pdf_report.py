"""
PDF Report Generation Module for Disease Detection System.

This module generates professional PDF reports with:
- Analysis summary and risk levels
- Disease-specific breakdowns with charts
- Eye tracking feature statistics
- Recommendations based on findings
"""

import io
from datetime import datetime
from typing import Dict, Any, Optional

# Try to import PDF generation libraries
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, cm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        Image, PageBreak, HRFlowable
    )
    from reportlab.graphics.shapes import Drawing, Rect, String
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.graphics.charts.piecharts import Pie
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


# Color scheme matching the web interface
COLORS = {
    'primary': colors.HexColor('#8b5cf6'),
    'secondary': colors.HexColor('#ec4899'),
    'success': colors.HexColor('#22c55e'),
    'warning': colors.HexColor('#f59e0b'),
    'danger': colors.HexColor('#ef4444'),
    'dark': colors.HexColor('#0a0a0f'),
    'light': colors.HexColor('#f8fafc'),
    'muted': colors.HexColor('#64748b'),
}


def get_risk_color(risk_level: str) -> colors.Color:
    """Get color based on risk level."""
    risk_level = risk_level.lower()
    if risk_level == 'high':
        return COLORS['danger']
    elif risk_level == 'moderate':
        return COLORS['warning']
    else:
        return COLORS['success']


def create_styles():
    """Create custom paragraph styles."""
    styles = getSampleStyleSheet()
    
    # Title style
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Title'],
        fontSize=28,
        textColor=COLORS['primary'],
        spaceAfter=30,
        alignment=TA_CENTER
    ))
    
    # Heading style
    styles.add(ParagraphStyle(
        name='CustomHeading',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=COLORS['primary'],
        spaceBefore=20,
        spaceAfter=12
    ))
    
    # Subheading style
    styles.add(ParagraphStyle(
        name='CustomSubheading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#4b5563'),
        spaceBefore=15,
        spaceAfter=8
    ))
    
    # Body text style
    styles.add(ParagraphStyle(
        name='CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#374151'),
        spaceAfter=8,
        alignment=TA_JUSTIFY
    ))
    
    # Risk badge style
    styles.add(ParagraphStyle(
        name='RiskBadge',
        parent=styles['Normal'],
        fontSize=16,
        textColor=colors.white,
        alignment=TA_CENTER,
        spaceBefore=10,
        spaceAfter=10
    ))
    
    # Disclaimer style
    styles.add(ParagraphStyle(
        name='Disclaimer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=COLORS['muted'],
        alignment=TA_CENTER,
        spaceBefore=20
    ))
    
    return styles


def create_risk_bar_chart(disease_data: Dict[str, Any]) -> Drawing:
    """Create a horizontal bar chart showing risk levels for each disease."""
    drawing = Drawing(400, 200)
    
    chart = VerticalBarChart()
    chart.x = 50
    chart.y = 30
    chart.width = 300
    chart.height = 140
    
    # Extract data
    diseases = []
    scores = []
    bar_colors = []
    
    disease_names = {
        'parkinsons': "Parkinson's",
        'alzheimers': "Alzheimer's",
        'asd': 'ASD',
        'adhd': 'ADHD'
    }
    
    for key, info in disease_data.items():
        if isinstance(info, dict):
            diseases.append(disease_names.get(key, key))
            score = info.get('risk_score', 0) * 100
            scores.append(score)
            risk_level = info.get('risk_level', 'low')
            bar_colors.append(get_risk_color(risk_level))
    
    if not scores:
        return drawing
    
    chart.data = [scores]
    chart.categoryAxis.categoryNames = diseases
    chart.categoryAxis.labels.fontName = 'Helvetica'
    chart.categoryAxis.labels.fontSize = 10
    chart.categoryAxis.labels.angle = 0
    
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 100
    chart.valueAxis.valueStep = 20
    chart.valueAxis.labels.fontName = 'Helvetica'
    chart.valueAxis.labels.fontSize = 9
    
    chart.bars.strokeWidth = 0
    for i, color in enumerate(bar_colors):
        chart.bars[0].fillColor = COLORS['primary']
    
    # Add percentage labels
    for i, score in enumerate(scores):
        label = String(chart.x + (i + 0.5) * (chart.width / len(scores)),
                      chart.y + (score / 100) * chart.height + 5,
                      f'{score:.1f}%',
                      fontSize=9,
                      fillColor=colors.HexColor('#374151'),
                      textAnchor='middle')
        drawing.add(label)
    
    drawing.add(chart)
    return drawing


def generate_pdf_report(
    analysis_results: Dict[str, Any],
    user_info: Optional[Dict[str, str]] = None,
    output_stream: Optional[io.BytesIO] = None
) -> io.BytesIO:
    """
    Generate a PDF report from analysis results.
    
    Args:
        analysis_results: The analysis results dictionary
        user_info: Optional user information (name, email, etc.)
        output_stream: Optional BytesIO stream (created if not provided)
    
    Returns:
        BytesIO stream containing the PDF
    """
    if not PDF_AVAILABLE:
        raise ImportError("ReportLab is required for PDF generation. Install with: pip install reportlab")
    
    if output_stream is None:
        output_stream = io.BytesIO()
    
    # Create the document
    doc = SimpleDocTemplate(
        output_stream,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )
    
    styles = create_styles()
    story = []
    
    # --- Header Section ---
    story.append(Paragraph("👁️ NeuroScan", styles['CustomTitle']))
    story.append(Paragraph("Eye Tracking Analysis Report", styles['CustomSubheading']))
    story.append(Spacer(1, 20))
    
    # Report metadata
    report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    story.append(Paragraph(f"<b>Report Generated:</b> {report_date}", styles['CustomBody']))
    
    if user_info:
        if user_info.get('name'):
            story.append(Paragraph(f"<b>Patient:</b> {user_info['name']}", styles['CustomBody']))
        if user_info.get('email'):
            story.append(Paragraph(f"<b>Email:</b> {user_info['email']}", styles['CustomBody']))
    
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=COLORS['muted']))
    story.append(Spacer(1, 20))
    
    # --- Summary Section ---
    summary = analysis_results.get('summary', {})
    risk_level = summary.get('risk_level', 'Low')
    risk_color = get_risk_color(risk_level)
    
    story.append(Paragraph("Overall Assessment", styles['CustomHeading']))
    
    # Risk level badge as a table
    risk_badge_data = [[f"🔬 {risk_level} Risk"]]
    risk_badge = Table(risk_badge_data, colWidths=[200])
    risk_badge.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), risk_color),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 16),
        ('PADDING', (0, 0), (-1, -1), 15),
        ('ROUNDEDCORNERS', [10, 10, 10, 10]),
    ]))
    story.append(risk_badge)
    story.append(Spacer(1, 15))
    
    # Summary text
    risk_messages = {
        'low': 'Your eye movement patterns appear within normal ranges. No significant indicators of neurological conditions were detected.',
        'moderate': 'Some eye movement patterns show mild variations that may warrant further monitoring. Consider consulting with a healthcare provider for a comprehensive evaluation.',
        'high': 'Several eye movement patterns show significant variations that may indicate potential neurological concerns. We strongly recommend consulting with a qualified healthcare professional for proper clinical assessment.'
    }
    story.append(Paragraph(risk_messages.get(risk_level.lower(), risk_messages['low']), styles['CustomBody']))
    story.append(Spacer(1, 20))
    
    # --- Disease Analysis Section ---
    disease_data = analysis_results.get('disease_analysis', {})
    
    if disease_data:
        story.append(Paragraph("Disease Risk Analysis", styles['CustomHeading']))
        story.append(Paragraph(
            "The following analysis shows the risk assessment for various neurological conditions based on your eye movement patterns:",
            styles['CustomBody']
        ))
        story.append(Spacer(1, 10))
        
        # Risk chart
        try:
            chart = create_risk_bar_chart(disease_data)
            story.append(chart)
            story.append(Spacer(1, 20))
        except Exception as e:
            print(f"Chart generation error: {e}")
        
        # Detailed breakdown table
        disease_names = {
            'parkinsons': ("Parkinson's Disease", "🧠"),
            'alzheimers': ("Alzheimer's Disease", "🧩"),
            'asd': ("Autism Spectrum Disorder", "💜"),
            'adhd': ("ADHD", "⚡")
        }
        
        table_data = [["Condition", "Risk Level", "Score", "Key Indicators"]]
        
        for key, info in disease_data.items():
            if isinstance(info, dict):
                name, icon = disease_names.get(key, (key.title(), "📊"))
                risk = info.get('risk_level', 'Low')
                score = f"{info.get('risk_score', 0) * 100:.1f}%"
                indicators = info.get('indicators', [])
                indicator_text = "; ".join(indicators[:2]) if indicators else "None detected"
                if len(indicator_text) > 50:
                    indicator_text = indicator_text[:47] + "..."
                table_data.append([f"{icon} {name}", risk, score, indicator_text])
        
        disease_table = Table(table_data, colWidths=[150, 80, 60, 200])
        disease_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), COLORS['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (2, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ]))
        story.append(disease_table)
        story.append(Spacer(1, 20))
    
    # --- Feature Statistics Section ---
    features = analysis_results.get('features', {})
    if features:
        story.append(Paragraph("Eye Movement Metrics", styles['CustomHeading']))
        story.append(Paragraph(
            "Key measurements extracted from your eye tracking data:",
            styles['CustomBody']
        ))
        story.append(Spacer(1, 10))
        
        feature_names = {
            'mean_fixation_duration': ('Avg. Fixation Duration', 'ms'),
            'fixation_count': ('Total Fixations', ''),
            'mean_saccade_velocity': ('Avg. Saccade Velocity', '°/s'),
            'saccade_count': ('Total Saccades', ''),
            'saccade_rate': ('Saccade Rate', '/s'),
            'coverage_area': ('Visual Coverage', 'px²'),
        }
        
        feature_data = [["Metric", "Value", "Description"]]
        descriptions = {
            'mean_fixation_duration': 'Time spent focusing on points',
            'fixation_count': 'Number of eye pauses',
            'mean_saccade_velocity': 'Speed of eye movements',
            'saccade_count': 'Number of rapid eye jumps',
            'saccade_rate': 'Eye movements per second',
            'coverage_area': 'Area of visual exploration',
        }
        
        for key, (name, unit) in feature_names.items():
            if key in features:
                value = features[key]
                if isinstance(value, float):
                    value_str = f"{value:.2f} {unit}".strip()
                else:
                    value_str = f"{value} {unit}".strip()
                desc = descriptions.get(key, '')
                feature_data.append([name, value_str, desc])
        
        if len(feature_data) > 1:
            feature_table = Table(feature_data, colWidths=[150, 100, 200])
            feature_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), COLORS['secondary']),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('TOPPADDING', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fdf4ff')]),
            ]))
            story.append(feature_table)
            story.append(Spacer(1, 20))
    
    # --- Recommendations Section ---
    story.append(Paragraph("Recommendations", styles['CustomHeading']))
    
    recommendations = []
    for disease_key, info in disease_data.items():
        if isinstance(info, dict):
            recs = info.get('recommendations', [])
            recommendations.extend(recs)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_recs = []
    for rec in recommendations:
        if rec not in seen:
            seen.add(rec)
            unique_recs.append(rec)
    
    if unique_recs:
        for rec in unique_recs[:5]:  # Limit to 5 recommendations
            story.append(Paragraph(f"• {rec}", styles['CustomBody']))
    else:
        story.append(Paragraph(
            "• Continue regular health monitoring",
            styles['CustomBody']
        ))
        story.append(Paragraph(
            "• Maintain healthy lifestyle habits",
            styles['CustomBody']
        ))
        story.append(Paragraph(
            "• Schedule routine eye exams",
            styles['CustomBody']
        ))
    
    story.append(Spacer(1, 30))
    
    # --- Disclaimer ---
    story.append(HRFlowable(width="100%", thickness=1, color=COLORS['muted']))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>IMPORTANT DISCLAIMER</b>",
        styles['Disclaimer']
    ))
    story.append(Paragraph(
        "This report is generated by an AI-powered screening tool and is intended for informational purposes only. "
        "It should NOT be used as a substitute for professional medical advice, diagnosis, or treatment. "
        "Always consult with a qualified healthcare provider for any health concerns or before making any "
        "decisions related to your health or treatment.",
        styles['Disclaimer']
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        f"© {datetime.now().year} NeuroScan - Eye Tracking Disease Detection System",
        styles['Disclaimer']
    ))
    
    # Build the PDF
    doc.build(story)
    
    # Reset stream position
    output_stream.seek(0)
    
    return output_stream


def generate_report_filename(user_id: Optional[str] = None) -> str:
    """Generate a unique filename for the report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if user_id:
        return f"neuroscan_report_{user_id}_{timestamp}.pdf"
    return f"neuroscan_report_{timestamp}.pdf"
