from flask import Blueprint

bp = Blueprint('report', __name__, url_prefix='/report')
report_bp = bp

from app.report import routes
