import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'securitytool.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Maturity scoring configuration
    MATURITY_LEVELS = {
        0: {'label': 'Not Implemented', 'description': 'Control is not in place'},
        1: {'label': 'Initial', 'description': 'Ad-hoc, reactive processes'},
        2: {'label': 'Developing', 'description': 'Partially implemented, inconsistent'},
        3: {'label': 'Defined', 'description': 'Documented and consistently applied'},
        4: {'label': 'Managed', 'description': 'Measured, monitored, and reviewed'},
        5: {'label': 'Optimising', 'description': 'Continuously improved and automated'},
    }

    # Effort bands for remediation roadmap
    EFFORT_BANDS = {
        'Low':    {'label': 'Low Effort',    'description': 'Quick wins — minimal cost/time', 'weeks': '1-2'},
        'Medium': {'label': 'Medium Effort',  'description': 'Moderate resources required',   'weeks': '3-8'},
        'High':   {'label': 'High Effort',    'description': 'Significant investment needed',  'weeks': '9-26'},
    }

    # NIST CSF function weights (equal by default, can be tuned)
    FUNCTION_WEIGHTS = {
        'Identify':  1.0,
        'Protect':   1.0,
        'Detect':    1.0,
        'Respond':   1.0,
        'Recover':   1.0,
    }


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
