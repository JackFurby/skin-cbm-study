from wtforms import StringField, BooleanField, RadioField, IntegerField, SelectField, HiddenField, TextAreaField, EmailField
from wtforms.validators import DataRequired, length, NumberRange
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
	age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18)])
	gender = SelectField('Gender', choices=[("", "Choose..."), ("Male", "male"), ("Female", "female"), ("Other", "other"),], validators=[DataRequired()])


class SampleForm(FlaskForm):
	ai_use = RadioField('Select the option that applies', choices=[(1, "I agree with the final AI prediction"), (2, "I disagree with the final AI prediction"), (3, "I disagree with the final AI prediction")], validators=[DataRequired()])


class SurveyForm(FlaskForm):
	factors_in_data = RadioField('I found that the data included all relevant known causal factors with sufficient precision and granularity', choices=[(5, "Strongly agree"), (4, "agree"), (3, "Neutral"), (2, "Disagree"), (1, "Strongly Disagree")], validators=[DataRequired()])
	understood = RadioField('I understood the explanations within the context of my work', choices=[(5, "Strongly agree"), (4, "agree"), (3, "Neutral"), (2, "Disagree"), (1, "Strongly Disagree")], validators=[DataRequired()])
	change_detail_level = RadioField('I could change the level of detail on demand', choices=[(5, "Strongly agree"), (4, "agree"), (3, "Neutral"), (2, "Disagree"), (1, "Strongly Disagree")], validators=[DataRequired()])
	need_support = RadioField('I did not need support to understand the explanations', choices=[(5, "Strongly agree"), (4, "agree"), (3, "Neutral"), (2, "Disagree"), (1, "Strongly Disagree")], validators=[DataRequired()])
	understood_causality = RadioField('I found the explanations helped me to understandcausality', choices=[(5, "Strongly agree"), (4, "agree"), (3, "Neutral"), (2, "Disagree"), (1, "Strongly Disagree")], validators=[DataRequired()])
	use_with_knowledge = RadioField('I was able to use the explanations with my knowledgebase', choices=[(5, "Strongly agree"), (4, "agree"), (3, "Neutral"), (2, "Disagree"), (1, "Strongly Disagree")], validators=[DataRequired()])
	no_inconsistencies = RadioField('I did not find inconsistencies between explanations', choices=[(5, "Strongly agree"), (4, "agree"), (3, "Neutral"), (2, "Disagree"), (1, "Strongly Disagree")], validators=[DataRequired()])
	learn_to_understand = RadioField('I think that most people would learn to understand the explanations very quickly', choices=[(5, "Strongly agree"), (4, "agree"), (3, "Neutral"), (2, "Disagree"), (1, "Strongly Disagree")], validators=[DataRequired()])
	need_references = RadioField('I did not need more references in the explanations: e.g., medical guidelines, regulations', choices=[(5, "Strongly agree"), (4, "agree"), (3, "Neutral"), (2, "Disagree"), (1, "Strongly Disagree")], validators=[DataRequired()])
	efficient = RadioField('I received the explanations in a timely and efficient manner', choices=[(5, "Strongly agree"), (4, "agree"), (3, "Neutral"), (2, "Disagree"), (1, "Strongly Disagree")], validators=[DataRequired()])
	text = TextAreaField('Any other comments about the AI and explanations (max 5000 characters. Write "none" if you have no comments)', validators=[DataRequired(), length(max=5000)])
