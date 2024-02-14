from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from datetime import datetime, timezone
import string
import random


class Consent(db.Model):
	id: so.Mapped[int] = so.mapped_column(primary_key=True)
	read_pis: so.Mapped[str] = so.mapped_column(sa.String(16))
	understood_pis: so.Mapped[str] = so.mapped_column(sa.String(16))
	participation_voluntary: so.Mapped[str] = so.mapped_column(sa.String(16))
	information_consent: so.Mapped[str] = so.mapped_column(sa.String(16))
	data_access: so.Mapped[str] = so.mapped_column(sa.String(16))
	anonymised_excerpts: so.Mapped[str] = so.mapped_column(sa.String(16))
	results_published: so.Mapped[str] = so.mapped_column(sa.String(16))
	take_part: so.Mapped[str] = so.mapped_column(sa.String(16))
	participant_name: so.Mapped[str] = so.mapped_column(sa.String(128))
	date: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
	email: so.Mapped[str] = so.mapped_column(sa.String(128))
	keep_me_updated: so.Mapped[bool] = so.mapped_column(sa.Boolean())

	def __repr__(self):
		return '<Consent {}>'.format(self.id)


class Demographic(db.Model):
	id: so.Mapped[int] = so.mapped_column(primary_key=True)
	skin_experience: so.Mapped[str] = so.mapped_column(sa.String(32))
	computer_experience: so.Mapped[str] = so.mapped_column(sa.String(32))
	age: so.Mapped[int] = so.mapped_column(sa.String(16))
	gender: so.Mapped[str] = so.mapped_column(sa.String(16))
	completed_study: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=False)
	created_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
	updated_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

	def __repr__(self):
		return f'<Demographic id:{self.id}, completed_study:{self.completed_study}>'


class Participant(db.Model):
	id: so.Mapped[int] = so.mapped_column(primary_key=True)
	created_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
	updated_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

	def __repr__(self):
		return '<Participant {}>'.format(self.id)


class Action(db.Model):
	id: so.Mapped[int] = so.mapped_column(primary_key=True)
	participant_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Participant.id), index=True)
	type: so.Mapped[str] = so.mapped_column(sa.String(32))
	last_action_time: so.Mapped[Optional[int]] = so.mapped_column()
	action_time: so.Mapped[Optional[int]] = so.mapped_column()
	update_value: so.Mapped[Optional[int]] = so.mapped_column()
	concept_id: so.Mapped[int] = so.mapped_column()
	sample_id: so.Mapped[int] = so.mapped_column()
	reset_pressed: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean())
	created_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
	updated_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

	def __repr__(self):
		return f'<Action {self.id}, {self.participant_id}, {self.type}, {self.last_action_time}, {self.action_time}, {self.update_value}, {self.concept_id}, {self.sample_id}, {self.reset_pressed}>'


class Sample(db.Model):
	id: so.Mapped[int] = so.mapped_column(primary_key=True)
	participant_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Participant.id), index=True)
	malignant: so.Mapped[bool] = so.mapped_column(sa.Boolean())
	start_time: so.Mapped[int] = so.mapped_column()
	complete_time: so.Mapped[int] = so.mapped_column()
	created_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
	updated_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

	def __repr__(self):
		return f'<Sample {self.id}, {self.participant_id}, {self.malignant}, {self.start_time}, {self.complete_time}>'


class Survey(db.Model):
	id: so.Mapped[int] = so.mapped_column(primary_key=True)
	participant_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Participant.id), index=True)
	text: so.Mapped[str] = so.mapped_column(sa.String(5000))
	created_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc))
	updated_at: so.Mapped[datetime] = so.mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

	def __repr__(self):
		return '<Survey {}>'.format(self.id)
