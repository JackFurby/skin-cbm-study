from flask import Flask, request, Response, flash, make_response, current_app, send_from_directory, jsonify, session
from flask import render_template, url_for, redirect
import cv2
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from study_app.study import bp
from study_app.forms import ConsentForm, DemographicForm
from study_app.models import Consent, Demographic, Participant, Action
from study_app import db


@bp.route('/', methods=["GET"])
@bp.route('/study', methods=["GET"])
def study():
	return render_template('study/study.html', title='CBM Study')


@bp.route('/forms', methods=['GET', 'POST'])
def forms():
	form = ConsentForm()
	if form.validate_on_submit():
		consent = Consent(
			read_pis=form.read_pis.data,
			understood_pis=form.understood_pis.data,
			participation_voluntary=form.participation_voluntary.data,
			information_consent=form.information_consent.data,
			data_access=form.data_access.data,
			anonymised_excerpts=form.anonymised_excerpts.data,
			results_published=form.results_published.data,
			take_part=form.take_part.data,
			participant_name=form.participant_name.data,
			date=form.date.data,
			email=form.email.data,
			keep_me_updated=form.keep_me_updated.data,
		)
		db.session.add(consent)
		db.session.commit()
		return redirect('/survey')
	return render_template('study/forms.html', title='Consent form', form=form)


@bp.route('/survey', methods=['GET', 'POST'])
def survey():
	form = DemographicForm()
	if form.validate_on_submit():
		demographic = Demographic(
			skin_experience=form.skin_experience.data,
			computer_experience=form.computer_experience.data,
			age=form.age.data,
			gender=form.gender.data
		)
		db.session.add(demographic)
		db.session.commit()

		participant = Participant()
		db.session.add(participant)
		db.session.commit()

		session["participant_id"] = participant.id
		session["demographic_id"] = demographic.id
		return redirect('/tutorial')
	return render_template('study/survey.html', title='Demographic survey', form=form)


@bp.route('/tutorial')
def tutorial():
	return render_template('study/tutorial.html', title='Tutorial')


@bp.route('/samples')
def samples():

	if "participant_id" in session:

		sample_id = 0
		task_out = "Malignant"
		concept_preds = []
		# open txt file with concept predictions and concept explanation file names
		with bp.open_resource(f"static/samples/{sample_id}/out.txt") as f:
			content = (f.read().decode('latin1').strip()).split("\n")
			for line in content:
				concept = line.split(" ")
				concept_preds.append((int(concept[0].strip()), concept[1].strip(), float(concept[2].strip())))  # concept index, concept explanation file name, concept prediction
		return render_template('study/samples.html', title='CBM Study', sample_id=sample_id, task_out=task_out, concept_out=concept_preds)
	else:
		return redirect(url_for('study.survey'))


@bp.route('/sample_survey')
def sample_survey():
	return render_template('study/sample_survey.html', title='Closing survey')


@bp.route('/get_image/<path:filename>')
def get_image(filename):
	return send_from_directory(bp.static_folder, f"samples/{filename}")


@bp.route('/log_range_update/', methods=['POST'])
def log_range_update():
	action = Action(
		participant_id=int(session["participant_id"]),
		type=request.form.get("type"),
		last_action_time=int(request.form.get("last_action_time")),
		action_time=int(request.form.get("action_time")),
		update_value=int(float(request.form.get("update_value")) * 100),
		concept_id=int(request.form.get("concept_id")),
		sample_id=int(request.form.get("sample_id")),
		reset_pressed=True if request.form.get("reset_pressed") == 'true' else False
	)
	db.session.add(action)
	db.session.commit()

	print(action)

	return jsonify("Action logged")


@bp.route('/log_concept_seen/', methods=['POST'])
def log_concept_seen():
	action = Action(
		participant_id=int(session["participant_id"]),
		type=request.form.get("type"),
		action_time=int(request.form.get("action_time")),
		concept_id=int(request.form.get("concept_id")),
		sample_id=int(request.form.get("sample_id"))
	)
	db.session.add(action)
	db.session.commit()

	print(action)
	
	return jsonify("Action logged")
