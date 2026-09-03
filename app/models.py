import json
from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='assessor')  # admin | assessor
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    organisations = db.relationship('Organisation', back_populates='creator', lazy='dynamic')
    assessments = db.relationship('Assessment', back_populates='assessor', lazy='dynamic')
    audit_entries = db.relationship('AuditLog', back_populates='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username}>'


class Organisation(db.Model):
    __tablename__ = 'organisations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(50), nullable=False)  # e.g. 1-10, 11-50, 51-200
    description = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    creator = db.relationship('User', back_populates='organisations')
    assessments = db.relationship('Assessment', back_populates='organisation', lazy='dynamic',
                                  cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Organisation {self.name}>'


class Control(db.Model):
    __tablename__ = 'controls'

    id = db.Column(db.Integer, primary_key=True)
    control_ref = db.Column(db.String(20), unique=True, nullable=False, index=True)  # e.g. ID.AM-1
    function = db.Column(db.String(20), nullable=False)  # Identify | Protect | Detect | Respond | Recover
    category = db.Column(db.String(100), nullable=False)  # e.g. Asset Management
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    guidance = db.Column(db.Text, default='')
    effort_band = db.Column(db.String(10), nullable=False, default='Medium')  # Low | Medium | High

    # Relationships
    responses = db.relationship('AssessmentResponse', back_populates='control', lazy='dynamic')

    def __repr__(self):
        return f'<Control {self.control_ref}: {self.title}>'


class Assessment(db.Model):
    __tablename__ = 'assessments'

    id = db.Column(db.Integer, primary_key=True)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisations.id'), nullable=False)
    assessor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='draft')  # draft | in_progress | completed
    started_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, default='')

    # Relationships
    organisation = db.relationship('Organisation', back_populates='assessments')
    assessor = db.relationship('User', back_populates='assessments')
    responses = db.relationship('AssessmentResponse', back_populates='assessment', lazy='dynamic',
                                cascade='all, delete-orphan')

    @property
    def completion_percentage(self):
        """Percentage of controls that have been scored (maturity > 0 or explicitly set)."""
        total = self.responses.count()
        if total == 0:
            return 0.0
        scored = self.responses.filter(AssessmentResponse.maturity_score.isnot(None)).count()
        return round((scored / total) * 100, 1)

    @property
    def function_scores(self):
        """Average maturity score per NIST CSF function.

        Returns a dict like {'Identify': 2.5, 'Protect': 3.0, ...}.
        Only includes scored responses (maturity_score is not None).
        """
        scores = {}
        functions = ['Identify', 'Protect', 'Detect', 'Respond', 'Recover']
        for func in functions:
            func_responses = (
                self.responses
                .join(Control)
                .filter(
                    Control.function == func,
                    AssessmentResponse.maturity_score.isnot(None),
                )
                .all()
            )
            if func_responses:
                avg = sum(r.maturity_score for r in func_responses) / len(func_responses)
                scores[func] = round(avg, 2)
            else:
                scores[func] = 0.0
        return scores

    @property
    def overall_score(self):
        """Weighted average of function scores (0-5 scale).

        Uses equal weights by default; weights are configured in Config.FUNCTION_WEIGHTS.
        """
        from flask import current_app
        weights = current_app.config.get('FUNCTION_WEIGHTS', {
            'Identify': 1.0, 'Protect': 1.0, 'Detect': 1.0,
            'Respond': 1.0, 'Recover': 1.0,
        })
        func_scores = self.function_scores
        total_weight = sum(weights.get(f, 1.0) for f in func_scores)
        if total_weight == 0:
            return 0.0
        weighted_sum = sum(
            func_scores[f] * weights.get(f, 1.0) for f in func_scores
        )
        return round(weighted_sum / total_weight, 2)

    @property
    def maturity_label(self):
        """Human-readable label for the overall maturity score."""
        score = self.overall_score
        if score < 1:
            return 'Not Implemented'
        elif score < 2:
            return 'Initial'
        elif score < 3:
            return 'Developing'
        elif score < 4:
            return 'Defined'
        elif score < 5:
            return 'Managed'
        else:
            return 'Optimising'

    @property
    def gaps(self):
        """Controls with maturity_score below 3 (target baseline), sorted by severity."""
        return (
            self.responses
            .join(Control)
            .filter(
                AssessmentResponse.maturity_score.isnot(None),
                AssessmentResponse.maturity_score < 3,
            )
            .order_by(AssessmentResponse.maturity_score.asc())
            .all()
        )

    def __repr__(self):
        return f'<Assessment #{self.id} for {self.organisation_id}>'


class AssessmentResponse(db.Model):
    __tablename__ = 'assessment_responses'

    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    control_id = db.Column(db.Integer, db.ForeignKey('controls.id'), nullable=False)
    maturity_score = db.Column(db.Integer, nullable=True)  # 0-5, None means not yet scored
    evidence_status = db.Column(db.String(10), nullable=False, default='none')  # none | partial | full
    evidence_description = db.Column(db.Text, default='')
    notes = db.Column(db.Text, default='')
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    assessment = db.relationship('Assessment', back_populates='responses')
    control = db.relationship('Control', back_populates='responses')

    __table_args__ = (
        db.UniqueConstraint('assessment_id', 'control_id', name='uq_assessment_control'),
    )

    @property
    def current_score(self):
        """Return the score currently recorded for this response."""
        return self.maturity_score if self.maturity_score is not None else 0

    @property
    def severity(self):
        """Classify the gap by how far below the target maturity baseline it sits."""
        if self.maturity_score is None:
            return 'Critical'
        if self.maturity_score < 1:
            return 'Critical'
        if self.maturity_score < 2:
            return 'High'
        if self.maturity_score < 3:
            return 'Medium'
        return 'Low'

    @property
    def gap_severity(self):
        """How far below the target baseline (3) this control is. 0 means on target or above."""
        if self.maturity_score is None:
            return 3  # treat unscored as maximum gap
        return max(0, 3 - self.maturity_score)

    def __getitem__(self, key):
        """Provide dict-like access for dashboard/report code paths expecting gap metadata."""
        if key == 'control':
            return self.control
        if key == 'response':
            return self
        if key == 'severity':
            return self.severity
        if key == 'current_score':
            return self.current_score
        if key == 'maturity_score':
            return self.maturity_score
        if key == 'gap_severity':
            return self.gap_severity
        raise KeyError(key)

    def __repr__(self):
        return f'<Response assessment={self.assessment_id} control={self.control_id} score={self.maturity_score}>'


class AuditLog(db.Model):
    __tablename__ = 'audit_log'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)  # e.g. login, create_assessment, update_score
    target_type = db.Column(db.String(50), nullable=True)  # e.g. assessment, organisation, control
    target_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, default='')  # JSON-encoded extra information
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # Relationships
    user = db.relationship('User', back_populates='audit_entries')

    @classmethod
    def log_action(cls, user_id, action, target_type=None, target_id=None, details=None):
        """Create an audit log entry and flush it to the session."""
        entry = cls(
            user_id=user_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            details=json.dumps(details) if details else '',
        )
        db.session.add(entry)
        db.session.commit()
        return entry

    @property
    def details_dict(self):
        """Parse the JSON details string back into a dict."""
        if not self.details:
            return {}
        try:
            return json.loads(self.details)
        except (json.JSONDecodeError, TypeError):
            return {}

    def __repr__(self):
        return f'<AuditLog {self.action} by user={self.user_id} at {self.timestamp}>'
