from django.views.generic import View
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse, QueryDict
from django.db import DatabaseError
from django.db import connection
from django.db import transaction
from django.db import models
from django.db.models import Count, F, Sum

from datetime import datetime
from TaskApp.models import *
from TaskManagement.utils import *

class ProjectView(View):
    ''''''
    def __init__(self):
        ''''''
        self.response = {
            'data': 'Done'
        }

    def dispatch(self, *args, **kwargs):
        return super(self.__class__, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
    	''''''
        # import pdb; pdb.set_trace()
        params = request.POST
        #self.response['data'] = params
        #print params
        print request.META.get('HTTP_REQUEST_TOKEN')
        print request.META.get('HTTP_UID')
        try:
            token = request.META.get('HTTP_REQUEST_TOKEN')
            mobile = request.META.get('HTTP_UID')
            access_bit = token_authentication(token,mobile)
            print access_bit
            if access_bit == True:
                org = Organization.objects.get(pk=params.get('org_id'))
                project_data = {
                    'project_name':params.get('project_name'),
                    'description':params.get('description'),
                    'status':params.get('status'),
                    'organization':org,
                }
                Project.objects.create(**project_data)
                return JsonResponse(self.response, status=200)
            else:
                self.response = {
                    'res_str':'Permission denied',
                    'res_data':{}
                }
                return JsonResponse(self.response, status=403)
        except Exception as ex:
            print str(ex)
            self.response = {
                'res_str':'Incorrect post request',
                'res_data':{}
            }
            return JsonResponse(self.response, status=400)

    def put(self, request, *args, **kwargs):
        ''''''
        # import pdb; pdb.set_trace()
        params = QueryDict(request.body)
        # self.response['data'] = params
        try:
            token = request.META.get('HTTP_REQUEST_TOKEN')
            mobile = request.META.get('HTTP_UID')
            access_bit = token_authentication(token,mobile)
            if access_bit == True:
                project_id = params.get('project_id')
                project = Project.objects.get(pk=project_id)
                # print project
                if params.get('project_name'):
                    project.project_name = params.get('project_name')
                if params.get('description'):
                    project.description = params.get('description')
                if params.get('status'):
                    project.status = params.get('status')
                project.save()
                return JsonResponse(self.response, status=200)
            else:
                self.response = {
                    'res_str':'Permission denied',
                    'res_data':{}
                }
                return JsonResponse(self.response, status=403)
        except Exception:
            self.response = {
                'res_str':'Incorrect request',
                'res_data':{}
            }
            return JsonResponse(self.response, status=400)

    def delete(self, request, *args, **kwargs):
        ''''''
        # import pdb; pdb.set_trace()
        params = QueryDict(request.body)
        # self.response['data'] = params
        try:
            token = request.META.get('HTTP_REQUEST_TOKEN')
            mobile = request.META.get('HTTP_UID')
            access_bit = token_authentication(token,mobile)
            if access_bit == True:
                project_id = params.get('project_id')
                project = Project.objects.get(pk=project_id)
                # print project
                if params.get('status') == '3':
                    project.status = params.get('status')
                project.save()
                return JsonResponse(self.response, status=200)
            else:
                self.response = {
                    'res_str':'Permission denied',
                    'res_data':{}
                }
                return JsonResponse(self.response, status=403)
        except Exception:
            self.response = {
                'res_str':'Incorrect request',
                'res_data':{}
            }
            return JsonResponse(self.response, status=400) 

    def get(self, request, *args, **kwrags):
    	''''''
    	params = request.GET
        try:
            token = request.META.get('HTTP_REQUEST_TOKEN')
            mobile = request.META.get('HTTP_UID')
            access_bit = token_authentication(token,mobile)
            if access_bit == True:
            	pid = params.get('project_id')
            	project = Project.objects.get(pk=pid)
                tasks = Task.objects.filter(project=project)
                #a = list()
                tasks_data = []
                for task in tasks:
                    tasks_data.append({
                        'name': task.task_name,
                        'id': task.id,
                        'description': task.description,
                        'status': task.status,
                        'task_type':task.task_type,
                        'user_name':task.user.get_name,
                        'user_id': task.user.pk
                        })
                # project_data = project._seraliser()
            	project_data = {
            		'name': project.project_name,
            		'description': project.description,
                    'tasks': tasks_data,
                    'created_by':'',
                    'status': project.status,
                    'id':project.id,
            	}
            	self.response = project_data
            	return JsonResponse(self.response, status=200)
            else:
                self.response = {
                    'res_str':'Permission denied',
                    'res_data':{}
                }
                return JsonResponse(self.response, status=403)
        except Exception:
            self.response = {
                'res_str':'Incorrect request',
                'res_data':{}
            }
            return JsonResponse(self.response, status=400)

class OrgProjectView(View):
    ''''''
    def __init__(self):
        ''''''
        self.response = {
            'data': 'Done'
        }

    def dispatch(self, *args, **kwargs):
        return super(self.__class__, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        ''''''
        params = request.GET
        try:
            token = request.META.get('HTTP_REQUEST_TOKEN')
            mobile = request.META.get('HTTP_UID')
            access_bit = token_authentication(token,mobile)
            if access_bit == True:
                org_id = params.get('org_id')
                org = Organization.objects.get(pk=org_id)
                projects = Project.objects.filter(organization=org)
                data = list()
                for project in projects:
                    data.append({
                            'project_name':project.project_name,
                            'project_desc':project.description,
                            'project_status':project.status,
                            'id':project.pk
                        })
                self.response = {
                    'res_str':'Success',
                    'res_data':data
                }
                return JsonResponse(self.response, status=200)
            else:
                self.response = {
                    'res_str':'Permission denied',
                    'res_data':{}
                }
                return JsonResponse(self.response, status=403)
        except Exception as e:
            self.response = {
                'res_str':'Invalid request',
                'res_data':{}
            }
            return JsonResponse(self.response, status=400)

class TaskView(View):
    ''''''
    def __init__(self):
        ''''''
        self.response = {
            'data': 'Done'
        }

    def dispatch(self, *args, **kwargs):
        return super(self.__class__, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        ''''''
        # import pdb; pdb.set_trace()
        params = request.POST
        try:
            token = request.META.get('HTTP_REQUEST_TOKEN')
            mobile = request.META.get('HTTP_UID')
            access_bit = token_authentication(token,mobile)
            if access_bit == True:
                project = Project.objects.get(pk=params.get('project_id'))
                #self.response['data'] = params
                # print params
                task_data = {
                    'task_name':params.get('name'),
                    'description':params.get('description'),
                    'status':params.get('status'),
                    'project_id':params.get('project_id'),
                    'task_type':params.get('task_type'),
                    'user_id':params.get('user_id')
                }
                Task.objects.create(**task_data)
                return JsonResponse(self.response, status=200)
            else:
                self.response = {
                    'res_str':'Permission denied',
                    'res_data':{}
                }
                return JsonResponse(self.response, status=403)
        except Exception:
            self.response = {
                'res_str':'Incorrect request',
                'res_data':{}
            }
            return JsonResponse(self.response, status=400)

    def put(self, request, *args, **kwargs):
        ''''''
        # import pdb; pdb.set_trace()
        params = QueryDict(request.body)
        # self.response['data'] = params
        try:
            token = request.META.get('HTTP_REQUEST_TOKEN')
            mobile = request.META.get('HTTP_UID')
            access_bit = token_authentication(token,mobile)
            if access_bit == True:
                task_id = params.get('task_id')
                task = Task.objects.get(pk=task_id)
                project = Project.objects.get(pk=params.get('project_id'))
                # print project
                if params.get('name'):
                    task.task_name = params.get('name')
                if params.get('description'):
                    task.description = params.get('description')
                if params.get('status'):
                    task.status = params.get('status')
                if params.get('project'):
                    task.project_id = params.get('project_id')
                if params.get('task_type'):
                    task.task_type = params.get('task_type')
                if params.get('user_id'):
                    task.user_id = params.get('user_id')
                    # task.project = project
                task.save()
                return JsonResponse(self.response, status=200)
            else:
                self.response = {
                    'res_str':'Permission denied',
                    'res_data':{}
                }
                return JsonResponse(self.response, status=403)
        except Exception:
            self.response = {
                'res_str':'Incorrect request',
                'res_data':{}
            }
            return JsonResponse(self.response, status=400)

    def delete(self, request, *args, **kwargs):
        ''''''
        # import pdb; pdb.set_trace()
        params = QueryDict(request.body)
        # self.response['data'] = params
        try:
            token = request.META.get('HTTP_REQUEST_TOKEN')
            mobile = request.META.get('HTTP_UID')
            access_bit = token_authentication(token,mobile)
            if access_bit == True:
                task_id = params.get('task_id')
                task = Task.objects.get(pk=task_id)
                # print project
                if params.get('status') == '6':
                    task.status = params.get('status')
                task.save()
                return JsonResponse(self.response, status=200)
            else:
                self.response = {
                    'res_str':'Permission denied',
                    'res_data':{}
                }
                return JsonResponse(self.response, status=403)
        except Exception:
            self.response = {
                'res_str':'Incorrect request',
                'res_data':{}
            }
            return JsonResponse(self.response, status=400)

    def get(self, request, *args, **kwrags):
        ''''''
        params = request.GET
        try:
            token = request.META.get('HTTP_REQUEST_TOKEN')
            mobile = request.META.get('HTTP_UID')
            access_bit = token_authentication(token,mobile)
            if access_bit == True:
                tid = params.get('task_id')
                task = Task.objects.get(pk=tid)
                project = task.project
                project_dict = {
                    'name':project.project_name,
                    'id':project.id
                }
                user = task.user
                user_dict = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'user_id': user.pk
                }
                # import pdb; pdb.set_trace()
                task_data = {
                    'name': task.task_name,
                    'description': task.description,
                    'created_by':'',
                    'status': task.status,
                    'id':task.id,
                    'project':project_dict,
                    'task_type':task.task_type,
                    'user':user_dict
                }
                self.response = task_data
                return JsonResponse(self.response, status=200)
            else:
                self.response = {
                    'res_str':'Permission denied',
                    'res_data':{}
                }
                return JsonResponse(self.response, status=403)
        except Exception, ex:
            self.response = {
                'res_str': str(ex),
                'res_data':{}
            }
            return JsonResponse(self.response, status=400)

class UserTasks(View):
    ''''''
    def __init__(self):
        ''''''
        self.response = {
            'data': 'Done'
        }

    def dispatch(self, *args, **kwargs):
        return super(self.__class__, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwrags):
        ''''''
        params = request.GET
        try:
            token = request.META.get('HTTP_REQUEST_TOKEN')
            mobile = request.META.get('HTTP_UID')
            access_bit = token_authentication(token,mobile)
            if access_bit == True:
                uid = params.get('user_id')
                tasks = Task.objects.filter(user_id = uid)
                
                
                # import pdb; pdb.set_trace()
                tasks_list = list()
                for task in tasks:

                    user = task.user
                    user_dict = {
                        'name': user.get_name,
                        'user_id': user.pk
                    }

                    project = task.project
                    project_dict = {
                        'name':project.project_name,
                        'id':project.id
                    }
                    
                    task_data = {
                        'name': task.task_name,
                        'description': task.description,
                        'created_by':'',
                        'status': task.status,
                        'id':task.id,
                        'project':project_dict,
                        'task_type':task.task_type,
                        'user':user_dict
                    }
                    tasks_list.append(task_data)
                self.response['data'] = tasks_list
                return JsonResponse(self.response, status=200)
            else:
                self.response = {
                    'res_str':'Permission denied',
                    'res_data':{}
                }
                return JsonResponse(self.response, status=403)
        except Exception, ex:
            self.response = {
                'res_str': str(ex),
                'res_data':{}
            }
            return JsonResponse(self.response, status=400)
class ProjectStatus(View):
    ''''''
    def __init__(self):
        ''''''
        self.response = {
            'data': 'Done'
        }

    def dispatch(self, *args, **kwargs):
        return super(self.__class__, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        ''''''
        # import pdb; pdb.set_trace()
        params = request.POST
        #self.response['data'] = params
        # print params
        try:
            token = request.META.get('HTTP_REQUEST_TOKEN')
            mobile = request.META.get('HTTP_UID')
            access_bit = token_authentication(token,mobile)
            if access_bit == True:
                project_id = params.get('project_id')
                project = Project.objects.get(pk=project_id)
                if params.get('status'):
                    project.status = params.get('status')
                project.save()
                return JsonResponse(self.response, status=200)
            else:
                self.response = {
                    'res_str':'Permission denied',
                    'res_data':{}
                }
                return JsonResponse(self.response, status=403)
        except Exception:
            self.response = {
                'res_str':'Incorrect request',
                'res_data':{}
            }
            return JsonResponse(self.response, status=400)

class TaskStatus(View):
    ''''''
    def __init__(self):
        ''''''
        self.response = {
            'data': 'Done'
        }

    def dispatch(self, *args, **kwargs):
        return super(self.__class__, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        ''''''
        # import pdb; pdb.set_trace()
        params = request.POST
        #self.response['data'] = params
        # print params
        try:
            token = request.META.get('HTTP_REQUEST_TOKEN')
            mobile = request.META.get('HTTP_UID')
            access_bit = token_authentication(token,mobile)
            if access_bit == True:
                task_id = params.get('task_id')
                task = Task.objects.get(pk=task_id)
                if params.get('status'):
                    task.status = params.get('status')
                task.save()
                return JsonResponse(self.response, status=200)
            else:
                self.response = {
                    'res_str':'Permission denied',
                    'res_data':{}
                }
                return JsonResponse(self.response, status=403)
        except Exception:
            self.response = {
                'res_str':'Incorrect request',
                'res_data':{}
            }
            return JsonResponse(self.response, status=400)