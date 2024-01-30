from flask import Blueprint

bp = Blueprint('errors', __name__)

from study_app.errors import routes
