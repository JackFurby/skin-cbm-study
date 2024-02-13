from flask import Flask
from config import Config
from sassutils.wsgi import SassMiddleware
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()


import study_app.models
import study_app.forms


def create_app(config_class=Config):
	"""
	Construct Flash application without a global variable. This make it easier
	to run unit tests
	"""
	app = Flask(__name__)
	# Add SCSS to CSS while in development
	app.wsgi_app = SassMiddleware(app.wsgi_app, {
		'study_app': ('static/scss', 'static/css', '/static/css')
	})
	app.config.from_object(config_class)

	db.init_app(app)
	migrate.init_app(app, db)
	mail.init_app(app)

	# Study
	from study_app.study import bp as study_bp
	app.register_blueprint(study_bp)

	# Error pages and functions
	from study_app.errors import bp as errors_bp
	app.register_blueprint(errors_bp)

	from study_app.cli import bp as cli_bp
	app.register_blueprint(cli_bp)

	# Normal app startup
	if not app.debug and not app.testing:
		pass

	return app
