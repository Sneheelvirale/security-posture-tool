from flask import Blueprint

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
dashboard_bp = bp

from app.dashboard import routes
