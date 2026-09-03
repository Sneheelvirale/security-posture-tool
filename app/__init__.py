import os
import click
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_name=None):
    """Application factory."""
    app = Flask(__name__)

    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')

    from config import config as config_dict
    app.config.from_object(config_dict[config_name])

    # Initialise extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'
    csrf.init_app(app)

    # User loader for Flask-Login
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register blueprints
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import main_bp
    app.register_blueprint(main_bp)

    from app.assessment import assessment_bp
    app.register_blueprint(assessment_bp, url_prefix='/assessment')

    from app.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    from app.report import report_bp
    app.register_blueprint(report_bp, url_prefix='/report')

    # CLI command to initialise the database and seed data
    @app.cli.command('init-db')
    @click.option('--seed', is_flag=True, help='Seed controls and sample data')
    def init_db(seed):
        """Create tables and optionally seed data."""
        db.create_all()
        click.echo('Database tables created.')
        if seed:
            from seeds.seed_data import seed_all
            seed_all(db)
            click.echo('Seed data loaded.')

    return app
