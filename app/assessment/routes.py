from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.assessment import bp
from app.models import Assessment, Organisation, Control, AssessmentResponse, AuditLog
from app import db
from datetime import datetime


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_assessment():
    """Create a new assessment."""
    if request.method == 'POST':
        org_id = request.form.get('organisation_id')
        notes = request.form.get('notes', '')

        if not org_id:
            flash('Please select an organisation.', 'danger')
            return redirect(url_for('assessment.new_assessment'))

        assessment = Assessment(
            organisation_id=org_id,
            assessor_id=current_user.id,
            status='in_progress',
            started_at=datetime.utcnow(),
            notes=notes
        )
        db.session.add(assessment)
        db.session.commit()

        # Initialize responses for all controls
        controls = Control.query.all()
        for control in controls:
            response = AssessmentResponse(
                assessment_id=assessment.id,
                control_id=control.id,
                maturity_score=0,
                evidence_status='none'
            )
            db.session.add(response)

        db.session.commit()

        AuditLog.log_action(
            current_user.id,
            'create',
            'assessment',
            assessment.id,
            f'Started assessment for {assessment.organisation.name}'
        )

        flash('Assessment created successfully.', 'success')
        return redirect(url_for('assessment.conduct', assessment_id=assessment.id))

    organisations = Organisation.query.order_by(Organisation.name).all()
    return render_template('assessment/new_assessment.html', organisations=organisations)


@bp.route('/<int:assessment_id>')
@login_required
def view_assessment(assessment_id):
    """View assessment summary."""
    assessment = Assessment.query.get_or_404(assessment_id)

    # Get responses grouped by function
    functions = ['Identify', 'Protect', 'Detect', 'Respond', 'Recover']
    responses_by_function = {}

    for function in functions:
        responses_by_function[function] = db.session.query(
            AssessmentResponse, Control
        ).join(Control).filter(
            AssessmentResponse.assessment_id == assessment_id,
            Control.function == function
        ).order_by(Control.control_ref).all()

    return render_template('assessment/view_assessment.html',
                         assessment=assessment,
                         functions=functions,
                         responses_by_function=responses_by_function)


@bp.route('/<int:assessment_id>/conduct')
@login_required
def conduct(assessment_id):
    """Conduct assessment - evaluate controls."""
    assessment = Assessment.query.get_or_404(assessment_id)

    if assessment.status == 'completed':
        flash('This assessment is already completed.', 'info')
        return redirect(url_for('assessment.view_assessment', assessment_id=assessment_id))

    # Get all responses with controls, grouped by function
    functions = ['Identify', 'Protect', 'Detect', 'Respond', 'Recover']
    responses_by_function = {}

    for function in functions:
        responses_by_function[function] = db.session.query(
            AssessmentResponse, Control
        ).join(Control).filter(
            AssessmentResponse.assessment_id == assessment_id,
            Control.function == function
        ).order_by(Control.control_ref).all()

    return render_template('assessment/conduct.html',
                         assessment=assessment,
                         functions=functions,
                         responses_by_function=responses_by_function)


@bp.route('/<int:assessment_id>/update-response/<int:response_id>', methods=['POST'])
@login_required
def update_response(assessment_id, response_id):
    """Update a single control response via AJAX."""
    response = AssessmentResponse.query.get_or_404(response_id)
    assessment = Assessment.query.get_or_404(assessment_id)

    if assessment.status == 'completed':
        return jsonify({'success': False, 'message': 'Assessment is completed'}), 400

    # Update fields
    maturity_score = request.json.get('maturity_score')
    evidence_status = request.json.get('evidence_status')
    evidence_description = request.json.get('evidence_description', '')
    notes = request.json.get('notes', '')

    if maturity_score is not None:
        response.maturity_score = int(maturity_score)
    if evidence_status:
        response.evidence_status = evidence_status
    if evidence_description is not None:
        response.evidence_description = evidence_description
    if notes is not None:
        response.notes = notes

    response.updated_at = datetime.utcnow()
    db.session.commit()

    AuditLog.log_action(
        current_user.id,
        'update',
        'assessment_response',
        response.id,
        f'Updated {response.control.control_ref} in assessment {assessment_id}'
    )

    return jsonify({'success': True})


@bp.route('/<int:assessment_id>/complete', methods=['POST'])
@login_required
def complete_assessment(assessment_id):
    """Mark assessment as completed."""
    assessment = Assessment.query.get_or_404(assessment_id)

    if assessment.status == 'completed':
        flash('Assessment is already completed.', 'info')
        return redirect(url_for('assessment.view_assessment', assessment_id=assessment_id))

    assessment.status = 'completed'
    assessment.completed_at = datetime.utcnow()
    db.session.commit()

    AuditLog.log_action(
        current_user.id,
        'complete',
        'assessment',
        assessment.id,
        f'Completed assessment for {assessment.organisation.name}'
    )

    flash('Assessment marked as completed.', 'success')
    return redirect(url_for('dashboard.view', assessment_id=assessment_id))


@bp.route('/list')
@login_required
def list_assessments():
    """List all assessments."""
    assessments = Assessment.query.order_by(Assessment.started_at.desc()).all()
    return render_template('assessment/list.html', assessments=assessments)
