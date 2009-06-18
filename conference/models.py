#
#  Conference System - django didatical system
#
#  Copyright (C) 2009  Gustavo Serra Scalet <gut@las.ic.unicamp.br>
#					  Gustavo F. Padovan <gustavo@las.ic.unicamp.br>
#
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
import os
PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

class Area(models.Model):

	area = models.CharField(max_length=256)
	description = models.CharField(max_length=2048)

	def __unicode__(self):
		return self.area


class SiteUser(User):
	user_choice = (
		('A', 'Anonymous'),
		('U', 'SiteUser'),
		('S', 'Sponsor'),
		('T', 'Staff'),
		('P', 'Participant'),
		('E', 'Speaker'),
		('R', 'Reviewer'),
	)

	first_name = models.CharField(max_length=256)
	last_name = models.CharField(max_length=256)
	user_type= models.CharField(max_length=1, choices=user_choice)
	cpf = models.IntegerField()
	organization = models.CharField(max_length=256)
	email = models.EmailField(null=False, verbose_name="E-mail address")
	newsletter = models.BooleanField(
			help_text="Check the box to choose receive newsletters")

	def __unicode__(self):
		return self.username


class SiteUserForm(UserCreationForm):
	accept_terms = forms.BooleanField(
			help_text="I accept the terms of use")
	class Meta:
		model = SiteUser
		fields = ('first_name', 'last_name', 'username',
				'email', 'cpf', 'organization',
				'newsletter', 'accept_terms')


class SponsorType(models.Model):

	interesting = models.ManyToManyField(Area)
	name = models.CharField(max_length=256)
	amount = models.PositiveIntegerField()
	max_invites = models.SmallIntegerField()

	def __unicode__(self):
		return self.name


class Sponsor(SiteUser):

	name = models.CharField(max_length=256)
	type = models.ForeignKey(SponsorType)
	# just for convenience, we can count all invited instead
	num_invited = models.SmallIntegerField()

	def __unicode__(self):
		return self.name


class Participant(SiteUser):
	area = models.ManyToManyField(Area)

class Speaker(Participant):
	cv = models.CharField(max_length=65536)

class Reviewer(Participant):
	status = models.BooleanField()
	deadline = models.DateField()

class Text(models.Model):
	text_type_choice = (
		(True, 'Paper'),
		(False, 'Abstract')
	)
	title = models.CharField(max_length=256)
	file = models.FileField(upload_to=os.path.join(PROJECT_ROOT_PATH, 'files'))
	area = models.ManyToManyField(Area)
	type = models.BooleanField(choices=text_type_choice, default=True)
	author = models.ForeignKey(SiteUser)
	num_review = models.SmallIntegerField(default=0)
	accepted = models.BooleanField(default=False)
	published = models.BooleanField(default=False)

	def __unicode__(self):
		return self.title

class TextForm(forms.ModelForm):
	accept_terms = forms.BooleanField(
			help_text="I accept the terms of use")
	class Meta:
		model = Text
		fields = ('title', 'file', 'type', 'area', 'accept_terms')


class Review(models.Model):
	reviewer = models.ForeignKey(Reviewer)
	text = models.ForeignKey(Text)
	rate = models.SmallIntegerField()
	comment = models.TextField()
	reviewed = models.BooleanField(default=False)

	def __unicode__(self):
		return self.text.title


class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = ('rate', 'comment')


class ConferenceSettings(models.Model):
	max_reviewers = models.PositiveIntegerField()
	def __unicode__(self):
		return None

