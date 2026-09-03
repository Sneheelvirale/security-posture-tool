from flask import Blueprint

bp = Blueprint('assessment', __name__, url_prefix='/assessment')
assessment_bp = bp

from app.assessment import routes
