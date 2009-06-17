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


from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
from conference import views
import os
PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Example:
	# (r'^conf/', include('conf.foo.urls')),

	# Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
	# to INSTALLED_APPS to enable admin documentation:
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	(r'^admin/(.*)', admin.site.root),
	(r'^$', views.home),
	(r'^user_create/$', views.user_create),
	(r'^text_submit/$', views.text_submit),
	(r'^for_review/$', views.for_review),
	(r'^for_review/(?P<review_id>\d+)$', views.review_text),
	(r'^download/(?P<path>.*)$', 'django.views.static.serve',
		{'document_root': os.path.join(PROJECT_ROOT_PATH,
			'conference/files') } ),
	(r'^(.*/)?auth/$', views.login_auth),
	(r'^logout/$', views.logout),

	(r'^(.*/)?(?P<path>.*\.css)$', 'django.views.static.serve', {'document_root': os.path.join(PROJECT_ROOT_PATH,'templates/css/') }),
	(r'^(.*/)?(?P<path>.*\.(jpg|png|gif))$', 'django.views.static.serve', {'document_root': os.path.join(PROJECT_ROOT_PATH,'templates/img/') }),


)
