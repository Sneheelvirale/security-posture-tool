from flask import render_template, make_response
from flask_login import login_required
from app.report import bp
from app.models import Assessment, AssessmentResponse, Control
from app import db
from datetime import datetime


@bp.route('/<int:assessment_id>')
@login_required
def view(assessment_id):
    """Generate printable report for an assessment."""
    assessment = Assessment.query.get_or_404(assessment_id)

    if assessment.status != 'completed':
        from flask import flash, redirect, url_for
        flash('Assessment must be completed before generating a report.', 'warning')
        return redirect(url_for('assessment.view_assessment', assessment_id=assessment_id))

    # Get all responses grouped by function
    functions = ['Identify', 'Protect', 'Detect', 'Respond', 'Recover']
    responses_by_function = {}

    for function in functions:
        responses_by_function[function] = db.session.query(
            AssessmentResponse, Control
        ).join(Control).filter(
            AssessmentResponse.assessment_id == assessment_id,
            Control.function == function
        ).order_by(Control.control_ref).all()

    # Get function scores
    function_scores = assessment.function_scores

    # Get gaps
    gaps = assessment.gaps

    # Group gaps by severity
    critical_gaps = [g for g in gaps if g['severity'] == 'Critical']
    high_gaps = [g for g in gaps if g['severity'] == 'High']
    medium_gaps = [g for g in gaps if g['severity'] == 'Medium']

    # Evidence summary
    evidence_summary = {
        'none': sum(1 for r in assessment.responses if r.evidence_status == 'none'),
        'partial': sum(1 for r in assessment.responses if r.evidence_status == 'partial'),
        'full': sum(1 for r in assessment.responses if r.evidence_status == 'full'),
    }

    # Roadmap items (top 10 priorities)
    roadmap_items = sorted(gaps, key=lambda x: (
        {'Critical': 0, 'High': 1, 'Medium': 2}.get(x['severity'], 3),
        {'Low': 0, 'Medium': 1, 'High': 2}.get(x['control'].effort_band, 3)
    ))[:10]

    response = make_response(render_template('report/view.html',
                         assessment=assessment,
                         functions=functions,
                         responses_by_function=responses_by_function,
                         function_scores=function_scores,
                         gaps=gaps,
                         critical_gaps=critical_gaps,
                         high_gaps=high_gaps,
                         medium_gaps=medium_gaps,
                         evidence_summary=evidence_summary,
                         roadmap_items=roadmap_items,
                         report_date=datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')))

    return response


@bp.route('/<int:assessment_id>/methodology')
@login_required
def methodology(assessment_id):
    """Explain the scoring methodology."""
    assessment = Assessment.query.get_or_404(assessment_id)

    from flask import current_app
    maturity_levels = current_app.config['MATURITY_LEVELS']
    effort_bands = current_app.config['EFFORT_BANDS']
    function_weights = current_app.config['FUNCTION_WEIGHTS']

    return render_template('report/methodology.html',
                         assessment=assessment,
                         maturity_levels=maturity_levels,
                         effort_bands=effort_bands,
                         function_weights=function_weights)
