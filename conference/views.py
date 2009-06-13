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

def get_default_template_vars(request):
	if request.user.is_authenticated():
		return {'user_type' : request.user.user_type,
				'user_name' : request.user.username,}
	else:
		return {}

def show_user_page(request):
		return render_to_response('conference/user_page.html', {})

def home(request):
	if request.user.is_authenticated():
		return show_user_page(request)
	else:
		ret = get_default_template_vars(request).update({'error' : False,})
		return render_to_response('conference/home.html', ret)


def login_auth(request):
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
		return render_to_response('conference/home.html', {'error' : True,})

def user_create(request):
	pass

def text_submit(request):
	pass

def logout(request):
	auth.logout(request)
	return home(request)
