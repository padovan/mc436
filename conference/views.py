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


from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render_to_response
from conference import models
from django.forms.util import ErrorList
import os
PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

class DivErrorList(ErrorList):

	def __unicode__(self):
		return self.as_divs()
	def as_divs(self):
		if not self: return u''
		return u'<div class="errorlist">%s</div>' % ''.join([u'<div class="error">%s</div>' % e for e in self])

def get_site_user(request):
	if request.user.is_authenticated():
		site_user = models.SiteUser.objects.filter(
				username = request.user.username)
		if len(site_user) == 1:
			return site_user[0]
	return None

def get_default_template_vars(request):
	site_user = get_site_user(request)
	if site_user:
		ret = {'user_name' : request.user.username,}
		ret['user_type'] = site_user.user_type
		return ret
	else:
		return {'user_type' : 'A',}


def show_user_page(request):
		ret = get_default_template_vars(request)
		return render_to_response('conference/user_page.html', ret)

def home(request):
	if get_site_user(request):
		return show_user_page(request)
	else:
		ret = get_default_template_vars(request)
		return render_to_response('conference/home.html', ret)


def login_auth(request, a):
	try:
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)
		if user is not None and user.is_active:
			auth.login(request, user)
			if not get_site_user(request):
				auth.logout(request)
				raise
			return show_user_page(request)
		else:
			# Show same error as an exception
			raise
	except:
		ret = get_default_template_vars(request)
		ret['login_error'] = True
		return render_to_response('conference/home.html', ret)

def user_create(request):
	try:
		if request.method == 'POST':
			formset = models.SiteUserForm(request.POST, request.FILES,
					error_class=DivErrorList)
			if formset.is_valid():
				user = formset.save(commit=False)
				user.user_type = 'U'
				user.save()
				ret = get_default_template_vars(request)
				ret['user_created'] = True
				ret['login_name'] = user.username
				return render_to_response('conference/home.html', ret)
			else:
				ret = get_default_template_vars(request)
				ret['formset'] = formset
				return render_to_response('conference/form.html', ret)
		else:
			formset = models.SiteUserForm()
			ret = get_default_template_vars(request)
			ret['formset'] = formset
			return render_to_response('conference/form.html', ret)
	except:
		ret = get_default_template_vars(request)
		return render_to_response('conference/home.html', ret)


def text_submit(request):
	try:
		if request.method == 'POST':
			formset = models.TextForm(request.POST, request.FILES,
				error_class=DivErrorList)
			if formset.is_valid():
				text = formset.save(commit=False)
				site_user = models.SiteUser.objects.filter(
					username = request.user.username)[0]
				text.author = site_user
				text.save()
				ret = get_default_template_vars(request)
				ret['text_submitted'] = True
				return render_to_response('conference/home.html', ret)
			else:
				ret = get_default_template_vars(request)
				ret['formset'] = formset
				return render_to_response('conference/form.html', ret)
		formset = models.TextForm()
		ret = get_default_template_vars(request)
		ret['formset'] = formset
		return render_to_response('conference/form.html', ret)
	except:
		ret = get_default_template_vars(request)
		return render_to_response('conference/home.html', ret)

def for_review(request, retadd = {}):
	rev = models.Reviewer.objects.filter(
			username = request.user.username)
	if rev:
		texts = models.Review.objects.filter(reviewed=False, reviewer=rev[0])
		ret = get_default_template_vars(request)
		ret['texts'] = texts
		ret.update(retadd)
		return render_to_response('conference/for_review.html', ret)
	else:
		ret = get_default_template_vars(request)
		return render_to_response('conference/home.html', {})

def review_text(request, review_id):
	review = models.Review.objects.get(pk=review_id)
	text = review.text
	path = text.file.name.split('/')[-1]
	review_form = models.ReviewForm()
	if request.method == 'POST':
		formset = models.ReviewForm(request.POST, request.FILES,
			error_class=DivErrorList)
		review_id = request.POST['review_id']
		review = models.Review.objects.get(pk=review_id)
		if formset.is_valid():
			r = formset.save(commit=False)
			rev = models.Reviewer.objects.filter(
				username = request.user.username)[0]
			review.reviewed = True
			review.comment = r.comment
			review.rate = r.rate
			review.save()
			ret = {}
			ret['text_title'] = review.text.title
			ret['text_reviewed'] = True
			return for_review(request, ret)
		else:
			ret = get_default_template_vars(request)
			ret['title'] = text.title
			ret['formset'] = formset
			return render_to_response('conference/review_page.html', ret)
	formset = models.ReviewForm()
	ret = get_default_template_vars(request)
	ret['title'] = text.title
	ret['formset'] = formset
	ret['text'] = path
	ret['review_id'] = review_id
	return render_to_response('conference/review_page.html', ret)


def logout(request):
	auth.logout(request)
	return home(request)
