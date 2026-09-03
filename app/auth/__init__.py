from flask import Blueprint

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

# Backward-compatible alias used by app factory imports.
bp = auth_bp

from app.auth import routes

from app.auth import routes
