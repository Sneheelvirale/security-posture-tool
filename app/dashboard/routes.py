from flask import render_template, jsonify
from flask_login import login_required
from app.dashboard import bp
from app.models import Assessment, AssessmentResponse, Control
from app import db
from sqlalchemy import func


@bp.route('/<int:assessment_id>')
@login_required
def view(assessment_id):
    """View assessment dashboard with charts and gap analysis."""
    assessment = Assessment.query.get_or_404(assessment_id)

    # Calculate function scores
    function_scores = assessment.function_scores

    # Get gaps (controls with low maturity)
    gaps = assessment.gaps

    # Get evidence distribution
    evidence_stats = db.session.query(
        AssessmentResponse.evidence_status,
        func.count(AssessmentResponse.id)
    ).filter_by(assessment_id=assessment.id).group_by(AssessmentResponse.evidence_status).all()

    return render_template('dashboard/view.html',
                         assessment=assessment,
                         function_scores=function_scores,
                         gaps=gaps,
                         evidence_stats=evidence_stats)


@bp.route('/<int:assessment_id>/data')
@login_required
def chart_data(assessment_id):
    """Return chart data as JSON for dynamic loading."""
    assessment = Assessment.query.get_or_404(assessment_id)

    # Function scores for radar chart
    function_scores = assessment.function_scores
    radar_data = {
        'labels': list(function_scores.keys()),
        'values': list(function_scores.values())
    }

    # Maturity distribution for bar chart
    maturity_distribution = {}
    for i in range(6):
        count = sum(1 for r in assessment.responses if r.maturity_score == i)
        maturity_distribution[f'Level {i}'] = count

    # Evidence status for doughnut
    evidence_counts = {'none': 0, 'partial': 0, 'full': 0}
    for response in assessment.responses:
        evidence_counts[response.evidence_status] = evidence_counts.get(response.evidence_status, 0) + 1

    # Gap severity distribution
    gaps = assessment.gaps
    critical_gaps = [g for g in gaps if g['severity'] == 'Critical']
    high_gaps = [g for g in gaps if g['severity'] == 'High']
    medium_gaps = [g for g in gaps if g['severity'] == 'Medium']

    return jsonify({
        'radar': radar_data,
        'maturity': {
            'labels': list(maturity_distribution.keys()),
            'values': list(maturity_distribution.values())
        },
        'evidence': {
            'labels': ['None', 'Partial', 'Full'],
            'values': [evidence_counts['none'], evidence_counts['partial'], evidence_counts['full']]
        },
        'gaps': {
            'critical': len(critical_gaps),
            'high': len(high_gaps),
            'medium': len(medium_gaps)
        },
        'overall_score': assessment.overall_score,
        'completion': assessment.completion_percentage
    })


@bp.route('/<int:assessment_id>/roadmap')
@login_required
def roadmap(assessment_id):
    """View improvement roadmap."""
    assessment = Assessment.query.get_or_404(assessment_id)

    # Get prioritised gaps
    gaps = assessment.gaps

    # Group by effort and priority
    quick_wins = []
    short_term = []
    medium_term = []
    long_term = []

    for gap in gaps:
        control = gap['control']
        item = {
            'control': control,
            'gap': gap,
            'effort': control.effort_band
        }

        # Prioritize critical/high severity with low effort
        if gap['severity'] in ['Critical', 'High'] and control.effort_band == 'Low':
            quick_wins.append(item)
        elif control.effort_band == 'Low' or (control.effort_band == 'Medium' and gap['severity'] == 'Critical'):
            short_term.append(item)
        elif control.effort_band == 'Medium':
            medium_term.append(item)
        else:
            long_term.append(item)

    return render_template('dashboard/roadmap.html',
                         assessment=assessment,
                         quick_wins=quick_wins,
                         short_term=short_term,
                         medium_term=medium_term,
                         long_term=long_term)
