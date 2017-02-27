import operator
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from UserApp.views import *

urlpatterns = [
	url(r'^v1/orguser/$', csrf_exempt(UserView.as_view())),
	url(r'^v1/org/$', csrf_exempt(OrganizationView.as_view())),
    url(r'^v1/login/$', csrf_exempt(LoginView.as_view())),
	url(r'^v1/logout/$', csrf_exempt(LogoutView.as_view())),
]
