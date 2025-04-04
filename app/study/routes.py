from flask import Flask, request, Response, flash, make_response, current_app, send_from_directory, jsonify, session
from flask import render_template, url_for, redirect, send_file
import cv2
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from app.study import bp
from app.forms import ConsentForm, DemographicForm, SampleForm, SurveyForm
from app.models import Consent, Demographic, Participant, Action, Sample, Survey, ConceptSort
from app import db
import random
from app.study.utils import get_consent_pdf


def get_datetime(milliseconds):
	return datetime.fromtimestamp(milliseconds/1000.0)


@bp.route('/', methods=["GET"])
@bp.route('/study', methods=["GET"])
def study():
	return render_template('study/study.html', title='CBM Study')


@bp.route('/forms', methods=['GET', 'POST'])
def forms():
	if "consent_form" not in session:
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
				email=form.email.data,
				keep_me_updated=form.keep_me_updated.data,
			)
			db.session.add(consent)
			db.session.commit()

			session["consent_form"] = consent.id
			return redirect('/survey')
	else:
		return redirect('/survey')
	return render_template('study/forms.html', title='Consent form', form=form, date=datetime.now().strftime("%d/%m/%Y"))


@bp.route('/survey', methods=['GET', 'POST'])
def survey():

	if "demographic_survey" not in session:
		form = DemographicForm()
		if form.validate_on_submit():
			explanatons_list = [0, 1]  # 0: no saliency maps, 1: saliency maps

			# place the explanation versions participants have used into buckets
			completed_participants = [participant.participant_id for participant in Demographic.query.filter(Demographic.completed_study==True).all()]
			model_explanatons_counts = []
			for ex in explanatons_list:
				#count = Participant.query.filter(Participant.explanation_version==ex, Participant.model_name==model, Participant.id.in_(completed_participants)).count()  <<<<<< use this if we want to only count complted studies
				count = Participant.query.filter(Participant.explanation_version==ex).count()
				model_explanatons_counts.append(count)
			min_value_index = model_explanatons_counts.index(min(model_explanatons_counts))

			participant = Participant(
				explanation_version=min_value_index  # explanation version is selected so the count is balanced between the two explanation versions
			)
			db.session.add(participant)
			db.session.commit()

			demographic = Demographic(
				skin_experience=form.skin_experience.data,
				computer_experience=form.computer_experience.data,
				age=form.age.data,
				gender=form.gender.data,
				participant_id=participant.id
			)
			db.session.add(demographic)
			db.session.commit()

			session["participant_id"] = participant.id
			session["demographic_id"] = demographic.id
			session["explanation_version"] = participant.explanation_version
			session["demographic_survey"] = True
			return redirect('/ai_intro')
	else:
		return redirect('/ai_intro')
	return render_template('study/survey.html', title='Demographic survey', form=form)


@bp.route('/ai_intro', methods=["GET"])
def ai_brief():
	return render_template('study/ai_intro.html', title='AI introduction')


@bp.route('/tutorial')
def tutorial():
	# get concept predictions and explanatons
	concept_preds = []
	# open txt file with concept predictions and concept explanation file names
	with bp.open_resource(f"static/tutorial/out.txt") as f:
		content = (f.read().decode('latin1').strip()).split("\n")
		for line in content:
			concept = line.split(" ")
			concept_preds.append([int(concept[0].strip()), concept[1].strip(), float(concept[2].strip())])  # concept index, concept explanation file name, concept prediction, concept string

	# open txt file with concept predictions and concept explanation file names
	with bp.open_resource(f"static/samples/concept_desc.txt") as f:
		content = (f.read().decode('latin1').strip()).split("\n")
		for idx, line in enumerate(content):
			line = [i.strip() for i in line.split('|')]  # concept string, concept description
			concept_preds[idx].append(line[0])  # Add concept string to concept item
			concept_preds[idx].append(line[1])  # Add concept description to concept item

	model_name = "CtoY_indi_dense_404_onnx_model.onnx"

	return render_template('study/tutorial.html', title='Tutorial', concept_out=concept_preds, model_name=model_name, explanation_version=session["explanation_version"])


@bp.route('/samples', methods=['GET', 'POST'])
def samples():
	form = SampleForm()
	# save participant sample classification
	if form.validate_on_submit():

		# update db entery with participant selection
		samples_left = session["samples_left"]
		sample = db.session.query(Sample).filter_by(participant_id=session["participant_id"], sample_id=samples_left[-1]).first()
		sample.participant_malignant = True if request.form['participant_malignant'] == '1' else False
		sample.complete_time = get_datetime(round(((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds())*1000))
		sample.ai_use = ",".join(request.form.getlist("ai_use"))  # save checkboxes selected as a string. Each character is one option selected
		db.session.add(sample)
		db.session.commit()

		# remove sample from samples_left
		del samples_left[-1]
		session["samples_left"] = samples_left

	if "participant_id" in session:  # redirect if participant has not completed demographic survey
		if "samples_left" not in session:  # randomly order samples
			samples = [int(i) for i in next(os.walk(f"{bp.static_folder}/samples"))[1]]
			random.shuffle(samples)
			session["samples_left"] = samples

		if len(session["samples_left"]) == 0:  # if all samples seen; end study and go to closing survey
			return redirect(url_for('study.sample_survey'))

		# get sample id
		samples_left = session["samples_left"]
		sample_id = samples_left[-1]

		# if sample does not exist in db (first time sample is show to participant) then create db entery
		if db.session.query(Sample).filter_by(participant_id=session["participant_id"], sample_id=sample_id).first() is None:
			sample = Sample(
				participant_id=int(session["participant_id"]),
				sample_id=samples_left[-1]
			)
			db.session.add(sample)
			db.session.commit()

		# get concept predictions and explanatons
		concept_preds = []
		# open txt file with concept predictions and concept explanation file names
		with bp.open_resource(f"static/samples/{sample_id}/out.txt") as f:
			content = (f.read().decode('latin1').strip()).split("\n")
			for line in content:
				concept = line.split(" ")
				concept_preds.append([int(concept[0].strip()), concept[1].strip(), float(concept[2].strip())])  # concept index, concept explanation file name, concept prediction

		# open txt file with concept predictions and concept explanation file names
		with bp.open_resource(f"static/samples/concept_desc.txt") as f:
			content = (f.read().decode('latin1').strip()).split("\n")
			for idx, line in enumerate(content):
				line = [i.strip() for i in line.split('|')]  # concept string, concept description
				concept_preds[idx].append(line[0])  # Add concept string to concept item
				concept_preds[idx].append(line[1])  # Add concept description to concept item

		model_name = "CtoY_indi_dense_404_onnx_model.onnx"

		"""
		explanation versions
		====================

		0 = Concept predictions only (with the option to show saliency maps???)
		1 = Concept predictions and saliency maps
		"""

		return render_template('study/samples.html', title='CBM Study', sample_id=sample_id, concept_out=concept_preds, form=form, model_name=model_name, explanation_version=session["explanation_version"], sample_count=f"{10 - len(session['samples_left']) + 1}/10")
	else:
		return redirect(url_for('study.survey'))


# log what the model predicts for the downstream task (discard the log if the value has already been set)
@bp.route('/model_prediction/', methods=['POST'])
def model_prediction():
	sample = db.session.query(Sample).filter_by(participant_id=session["participant_id"], sample_id=request.form.get("sample_id")).first()
	if sample != None:
		if sample.model_malignant == None:
			sample.model_malignant = True if request.form.get("model_malignant") == 'malignant melanoma' else False
			db.session.add(sample)
			db.session.commit()
			return jsonify("Action logged")
		else:  # value has already been set. Do not update.
			return jsonify("Action logged")
	else:
		return jsonify("No action to log")


@bp.route('/sample_survey', methods=['GET', 'POST'])
def sample_survey():
	if "closing_survey" not in session:
		form = SurveyForm()
		if form.validate_on_submit():
			survey = Survey(
				participant_id=int(session["participant_id"]),
				text=form.text.data,
				factors_in_data=int(form.factors_in_data.data),
				understood=int(form.understood.data),
				change_detail_level=int(form.change_detail_level.data),
				need_support=int(form.need_support.data),
				understood_causality=int(form.understood_causality.data),
				use_with_knowledge=int(form.use_with_knowledge.data),
				no_inconsistencies=int(form.no_inconsistencies.data),
				learn_to_understand=int(form.learn_to_understand.data),
				need_references=int(form.need_references.data),
				efficient=int(form.efficient.data)
			)
			db.session.add(survey)
			db.session.commit()

			# update study to complete
			demographic = Demographic.query.filter_by(id=session["demographic_id"]).first()
			demographic.completed_study = True
			db.session.add(demographic)
			db.session.commit()

			session['closing_survey'] = True

			return redirect('/close')
	else:
		return redirect('/close')
	return render_template('study/sample_survey.html', title='Closing survey', form=form)


@bp.route('/close')
def close():
	return render_template('study/close.html', title='Thank you')


@bp.route('/get_image/<path:filename>')
def get_image(filename):
	return send_from_directory(bp.static_folder, f"samples/{filename}")


@bp.route('/get_image_tutorial/<path:filename>')
def get_image_tutorial(filename):
	return send_from_directory(bp.static_folder, f"tutorial/{filename}")


@bp.route('/get_consent_form')
def get_consent_form():
	consent = db.session.query(Consent).filter_by(id=session["consent_form"]).first()
	edits = [
		consent.read_pis,
		consent.understood_pis,
		consent.participation_voluntary,
		consent.information_consent,
		consent.data_access,
		consent.anonymised_excerpts,
		consent.results_published,
		consent.take_part,
		consent.participant_name,
		consent.date.strftime("%d/%m/%Y")
	]
	return send_file(get_consent_pdf(edits, bp.static_folder + "/Consent-Form.pdf"), as_attachment=True, download_name='Consent-Form.pdf', mimetype='application/pdf')



# log concept prediction changes
@bp.route('/log_range_update/', methods=['POST'])
def log_range_update():
	action = Action(
		participant_id=int(session["participant_id"]),
		type=request.form.get("type"),
		last_action_time=get_datetime(int(request.form.get("last_action_time"))),
		action_time=get_datetime(int(request.form.get("action_time"))),
		update_value=int(float(request.form.get("update_value")) * 100),
		concept_id=int(request.form.get("concept_id")),
		sample_id=int(request.form.get("sample_id")),
		reset_pressed=True if request.form.get("reset_pressed") == 'true' else False,
		model_malignant=True if request.form.get("model_malignant") == 'malignant melanoma' else False
	)
	db.session.add(action)
	db.session.commit()

	return jsonify("Action logged")


# log concepts participants see
@bp.route('/log_concept_seen/', methods=['POST'])
def log_concept_seen():
	action = Action(
		participant_id=int(session["participant_id"]),
		type=request.form.get("type"),
		action_time=get_datetime(int(request.form.get("action_time"))),
		concept_id=int(request.form.get("concept_id")),
		sample_id=int(request.form.get("sample_id"))
	)
	db.session.add(action)
	db.session.commit()

	return jsonify("Action logged")


# log when a participants changes the order concepts are displayed
@bp.route('/log_sort_update/', methods=['POST'])
def log_sort_update():
	action = ConceptSort(
		participant_id=int(session["participant_id"]),
		action_time=get_datetime(int(request.form.get("action_time"))),
		update_value=request.form.get("update_value"),
		sample_id=int(request.form.get("sample_id"))
	)
	db.session.add(action)
	db.session.commit()

	return jsonify("Action logged")


# log when a participants shows a concept description
@bp.route('/toggle_concept_desc/', methods=['POST'])
def toggle_concept_desc():
	action = Action(
		participant_id=int(session["participant_id"]),
		type=request.form.get("type"),
		action_time=get_datetime(int(request.form.get("action_time"))),
		concept_id=int(request.form.get("concept_id")),
		sample_id=int(request.form.get("sample_id"))
	)
	db.session.add(action)
	db.session.commit()

	return jsonify("Action logged")


# clear session data
@bp.route('/clear_session')
def clear_session():
	try:
		del session["samples_left"]
	except Exception as e:
		print(f"Could not delete: {e}")
	try:
		del session["participant_id"]
	except Exception as e:
		print(f"Could not delete: {e}")
	try:
		del session["consent_form"]
	except Exception as e:
		print(f"Could not delete: {e}")
	try:
		del session["demographic_survey"]
	except Exception as e:
		print(f"Could not delete: {e}")
	try:
		del session['closing_survey']
	except Exception as e:
		print(f"Could not delete: {e}")
	try:
		del session["explanation_version"]
	except Exception as e:
		print(f"Could not delete: {e}")
	return redirect(url_for('study.study'))
