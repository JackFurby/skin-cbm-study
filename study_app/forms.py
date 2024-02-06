from wtforms import StringField, BooleanField, RadioField, IntegerField, SelectField, HiddenField, TextAreaField, EmailField
from wtforms.validators import DataRequired, length
from flask import flash
from flask_wtf import FlaskForm
from werkzeug.local import LocalProxy
from flask import current_app


class ConsentForm(FlaskForm):
	read_pis = StringField('Please initial box', validators=[DataRequired()])
	understood_pis = StringField('Please initial box', validators=[DataRequired()])
	participation_voluntary = StringField('Please initial box', validators=[DataRequired()])
	information_consent = StringField('Please initial box', validators=[DataRequired()])
	data_access = StringField('Please initial box', validators=[DataRequired()])
	anonymised_excerpts = StringField('Please initial box', validators=[DataRequired()])
	results_published = StringField('Please initial box', validators=[DataRequired()])
	take_part = StringField('Please initial box', validators=[DataRequired()])
	participant_name = StringField('Name of participant', validators=[DataRequired()])
	email = EmailField('Email', validators=[DataRequired()])
	keep_me_updated = BooleanField('Keep me updated when this research is published', validators=[])


class DemographicForm(FlaskForm):
	skin_experience = RadioField('I am an experienced at identifying skin disease from images', choices=["Strongly agree", "agree", "Neutral", "Disagree", "Strongly Disagree"], validators=[DataRequired()])
	computer_experience = RadioField('I am experienced in computer science / computing', choices=["Strongly agree", "agree", "Neutral", "Disagree", "Strongly Disagree"], validators=[DataRequired()])
	age = IntegerField('Age', validators=[DataRequired()])
	gender = SelectField('Gender', choices=[("", "Choose..."), ("Male", "male"), ("Female", "female"), ("Other", "other"),], validators=[DataRequired()])


class SampleForm(FlaskForm):
	start_time = HiddenField('start time', validators=[DataRequired()])


class SurveyForm(FlaskForm):
	text = TextAreaField('Comments about the AI and explanations', validators=[DataRequired(), length(max=5000)])
