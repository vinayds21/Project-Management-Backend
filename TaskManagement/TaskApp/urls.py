import operator
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from TaskApp.views import *

urlpatterns = [
	url(r'^v1/project/$', csrf_exempt(ProjectView.as_view())),
	url(r'^v1/task/$', csrf_exempt(TaskView.as_view())),
	url(r'^v1/projectstatus/$', csrf_exempt(ProjectStatus.as_view())),
	url(r'^v1/taskstatus/$', csrf_exempt(TaskStatus.as_view()))
]
