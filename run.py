import os
from app import create_app, db
from app.models import User, Organisation, Control, Assessment, AssessmentResponse, AuditLog

app = create_app(os.environ.get('FLASK_CONFIG', 'default'))


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Organisation': Organisation,
        'Control': Control,
        'Assessment': Assessment,
        'AssessmentResponse': AssessmentResponse,
        'AuditLog': AuditLog,
    }


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
