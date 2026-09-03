from flask import Blueprint

bp = Blueprint('main', __name__)
main_bp = bp

from app.main import routes
