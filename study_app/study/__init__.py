from flask import Blueprint, current_app
import os
import glob
from config import Config  # this is probably a bad way of doing things

bp = Blueprint('study', __name__, static_folder='static')

from study_app.study import routes
