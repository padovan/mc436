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
from django.forms.models import modelformset_factory
from django.contrib.admin.views.decorators import staff_member_required
from django.forms.util import ErrorList

class DivErrorList(ErrorList):

	def __unicode__(self):
		return self.as_divs()
	def as_divs(self):
		if not self: return u''
		return u'<div class="errorlist">%s</div>' % ''.join([u'<div class="error">%s</div>' % e for e in self])

def get_default_template_vars(request):
	if request.user.is_authenticated():
		return {'user_type' : request.user.user_type,
			'user_name' : request.user.username,
			'error' : False,}
	else:
		return {'user_type' : 'A',}

def show_user_page(request):
		ret = get_default_template_vars(request)
		return render_to_response('conference/user_page.html', ret)

def home(request):
	if request.user.is_authenticated():
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
				user = formset.save()
				ret = get_default_template_vars(request)
				ret['user_created'] = True
				ret['login_name'] = user.username
				return render_to_response('conference/home.html', ret)
		# if any errors or unfilled form
		if not formset:
			# ok, so we have something from the POST
			formset = models.SiteUserForm()
		ret = get_default_template_vars(request)
		ret['formset'] = formset
		return render_to_response('conference/form.html', ret)
	except:
		ret = get_default_template_vars(request)
		return render_to_response('conference/home.html', ret)

def text_submit(request):
	try:
		TextFormSet = modelformset_factory(models.Text,
				fields = ('title', 'content', 'area', 'type',))
		if request.method == 'POST':
			formset = TextFormSet(request.POST, request.FILES)
			if formset.is_valid():
				formset.save()
				ret = get_default_template_vars(request)
				ret['text_submitted'] = True
				return render_to_response('conference/home.html', ret)
		# if any errors or unfilled form
		formset = TextFormSet()
		ret = get_default_template_vars(request)
		ret['formset'] = formset
		return render_to_response('conference/form.html', ret)
	except:
		ret = get_default_template_vars(request)
		return render_to_response('conference/home.html', ret)

@staff_member_required
def pick_reviewers(request):
	if request.method == 'POST':
		if request.POST['text']:
			revs = models.Reviewer.objects.filter(status=True)
		else:
			request.POST['reviewers']
	else:
		texts = models.Text.objects.filter(published=False)
		ret = get_default_template_vars(request)
		ret.update({'texts' : texts})
		return render_to_response('conference/pick_reviewers.html', ret)

def logout(request):
	auth.logout(request)
	return home(request)
