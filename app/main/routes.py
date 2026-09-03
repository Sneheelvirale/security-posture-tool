from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.main import bp
from app.models import Organisation, Assessment, Control, User, AuditLog
from app import db
from datetime import datetime


@bp.route('/')
@login_required
def index():
    """Dashboard home page."""
    # Get summary statistics
    total_orgs = Organisation.query.count()
    total_assessments = Assessment.query.count()
    completed_assessments = Assessment.query.filter_by(status='completed').count()
    total_controls = Control.query.count()

    # Recent assessments
    recent_assessments = Assessment.query.order_by(
        Assessment.started_at.desc()
    ).limit(5).all()

    # Recent activity from audit log
    recent_activity = AuditLog.query.order_by(
        AuditLog.timestamp.desc()
    ).limit(10).all()

    return render_template('main/index.html',
                         total_orgs=total_orgs,
                         total_assessments=total_assessments,
                         completed_assessments=completed_assessments,
                         total_controls=total_controls,
                         recent_assessments=recent_assessments,
                         recent_activity=recent_activity)


@bp.route('/organisations')
@login_required
def organisations():
    """List all organisations."""
    orgs = Organisation.query.order_by(Organisation.name).all()
    return render_template('main/organisations.html', organisations=orgs)


@bp.route('/organisations/<int:org_id>')
@login_required
def organisation_detail(org_id):
    """View organisation details and assessment history."""
    org = Organisation.query.get_or_404(org_id)
    assessments = Assessment.query.filter_by(organisation_id=org_id).order_by(
        Assessment.started_at.desc()
    ).all()

    return render_template('main/organisation_detail.html',
                         organisation=org,
                         assessments=assessments)


@bp.route('/organisations/new', methods=['GET', 'POST'])
@login_required
def new_organisation():
    """Create a new organisation."""
    if request.method == 'POST':
        name = request.form.get('name')
        industry = request.form.get('industry')
        size = request.form.get('size')
        description = request.form.get('description')

        if not name:
            flash('Organisation name is required.', 'danger')
            return redirect(url_for('main.new_organisation'))

        org = Organisation(
            name=name,
            industry=industry,
            size=size,
            description=description,
            created_by=current_user.id
        )
        db.session.add(org)
        db.session.commit()

        AuditLog.log_action(
            current_user.id,
            'create',
            'organisation',
            org.id,
            f'Created organisation: {org.name}'
        )

        flash(f'Organisation "{name}" created successfully.', 'success')
        return redirect(url_for('main.organisations'))

    return render_template('main/organisation_form.html')


@bp.route('/controls')
@login_required
def controls():
    """List all security controls."""
    # Group controls by function
    functions = ['Identify', 'Protect', 'Detect', 'Respond', 'Recover']
    controls_by_function = {}

    for function in functions:
        controls_by_function[function] = Control.query.filter_by(
            function=function
        ).order_by(Control.control_ref).all()

    return render_template('main/controls.html',
                         functions=functions,
                         controls_by_function=controls_by_function)


@bp.route('/controls/<int:control_id>')
@login_required
def control_detail(control_id):
    """View control details."""
    control = Control.query.get_or_404(control_id)
    return render_template('main/control_detail.html', control=control)
