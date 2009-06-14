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
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm

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

	user_type= models.CharField(max_length=1, choices=user_choice)
	cpf = models.CharField(max_length=14)
	organization = models.CharField(max_length=256)
	newsletter = models.BooleanField(
			help_text="Check the box to choose receive newsletters")
	email_verified = models.BooleanField()

	def __unicode__(self):
		return self.username


class SiteUserForm(UserCreationForm):
	class Meta:
		model = SiteUser
		fields = ('first_name', 'last_name', 'username',
				'email', 'cpf', 'organization',
				'newsletters')


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
	# FIXME: We are using Char field to represent a File field (i.e. 'migueh')
	cv = models.CharField(max_length=65536)

class Reviewer(Participant):
	status = models.BooleanField()
	deadline = models.DateField()

class ReviewerForm(ModelForm):
	class Meta:
		model = Reviewer

class Text(models.Model):
	text_type_choice = (
		(True, 'Paper'),
		(False, 'Abstract')
	)
	title = models.CharField(max_length=256)
	# FIXME: We are using Char field to represent a File field (i.e. 'migueh')
	content = models.CharField(max_length=65536)
	area = models.ManyToManyField(Area)
	type = models.BooleanField(choices=text_type_choice)
	author = models.ForeignKey(SiteUser)
	#FIXME: we really need this optimization?
	num_reviewers = models.PositiveSmallIntegerField()
	reviewer = models.ManyToManyField(Reviewer, related_name="reviewer_text")
	# reviewed just for convenience, if false we need to search if all
	# reviewers already reviewed the text
	reviewed = models.BooleanField(default=False)
	accepted = models.BooleanField(default=False)
	published = models.BooleanField(default=False)

	def __unicode__(self):
		return self.title

class TextForm(ModelForm):
	class Meta:
		model = Text

class ConferenceSettings(models.Model):
	max_reviewers = models.PositiveIntegerField()
	def __unicode__(self):
		return None

