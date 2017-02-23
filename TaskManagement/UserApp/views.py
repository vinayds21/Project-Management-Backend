from django.views.generic import View
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse, QueryDict
from django.db import DatabaseError
from django.db import connection
from django.db import transaction
from django.db import models
from django.db.models import Count, F, Sum
from datetime import datetime
from UserApp.models import *
import hashlib
import uuid

# Create your views here.

class OrganizationView(View):
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
        params = request.POST

        org_data = {
            'name': params.get('name'),
            'company_type': params.get('company_type'),
            'company_website': params.get('company_website'),
            'address_line_1':params.get('address_line_1'),
            'address_line_2':params.get('address_line_2'),
            'state':params.get('state'),
            'city':params.get('city'),
            'pin':params.get('pin'),
        }
        Organization.objects.create(**org_data)
        return JsonResponse(self.response, status=200)

    def put(self, request, *args, **kwargs):
        ''''''
        # import pdb; pdb.set_trace()
        params = QueryDict(request.body)
        # self.response['data'] = params
        # print params
        org_id = params.get('org_id')
        org = Organization.objects.get(pk=org_id)
        # print project
        if params.get('name'):
            org.name = params.get('name')
        if params.get('company_type'):
            org.company_type = params.get('company_type')
        if params.get('company_website'):
            org.company_website = params.get('company_website')
        if params.get('address_line_1'):
            org.address_line_1 = params.get('address_line_1')
        if params.get('address_line_2'):
            org.address_line_2 = params.get('address_line_2')
        if params.get('state'):
            org.state = params.get('state')
        if params.get('city'):
            org.city = params.get('city')
        if params.get('pin'):
            org.pin = params.get('pin')
        org.save()
        return JsonResponse(self.response, status=200)

    def get(self, request, *args, **kwargs):
        ''''''
        params = request.GET

        org_id = params.get('org_id')
        org = Organization.objects.get(pk=org_id)
        org_data = {
            'name': org.name,
            'company_type': org.company_type,
            'company_website': org.company_website,
            'org_id':org.id,
            'address_line_1':org.address_line_1,
            'address_line_2':org.address_line_2,
            'state':org.state,
            'city':org.city,
            'pin':org.pin,
        }
        self.response = org_data
        return JsonResponse(self.response, status=200)

class UserView(View):
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
        params = request.POST
        org = Organization.objects.get(pk=params.get('org_id'))
        if params.get('password'):
            hash_password = self.gen_password_hash(params.get('password'))
        else:
            self.response = {
                'res_str':'Please enter a password',
                'res_data':{}
            }
            return JsonResponse(self.response, status=400)
        user_data = {
            'first_name': params.get('first_name'),
            'last_name': params.get('last_name'),
            'user_mobile': params.get('user_mobile'),
            'user_mail':params.get('user_mail'),
            'user_designation':params.get('user_designation'),
            'user_type':params.get('user_type'),
            'organization':org,
            'user_password':hash_password
        }
        User.objects.create(**user_data)
        return JsonResponse(self.response, status=200)

    def gen_password_hash(self, passwd):
        return str(hashlib.sha256(passwd).hexdigest())

    def put(self, request, *args, **kwargs):
        ''''''
        # import pdb; pdb.set_trace()
        #mand = ['first_name', 'last_name', 'user_mail', 'user_designation', 'user_type']
        params = QueryDict(request.body)
        # param_keys = params.keys()
        # missing_params = list(set(mand) - set(param_keys))
        # if missing_params:
        # return error
        # self.response['data'] = params
        user_id = params.get('user_id')
        user = User.objects.get(pk=user_id)
        # print project
        if params.get('first_name'):
            user.first_name = params.get('first_name')
        if params.get('last_name'):
            user.last_name = params.get('last_name')
        if params.get('user_mail'):
            user.user_mail = params.get('user_mail')
        if params.get('user_designation'):
            user.user_designation = params.get('user_designation')
        if params.get('user_type'):
            user.user_type = params.get('user_type')
        user.save()
        return JsonResponse(self.response, status=200)

    def get(self, request, *args, **kwargs):
        ''''''
    	params = request.GET
        user_id = params.get('user_id')
        user = User.objects.get(pk=user_id)
        org = user.organization
        org_dict={
            'org_id':org.id,
            'org_name':org.name
        }
        user_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_mobile': user.user_mobile,
            'user_mail': user.user_mail,
            'user_designation': user.user_designation,
            'user_type': user.user_type,
            'org':org_dict
        }
        self.response = user_data
    	return JsonResponse(self.response, status=200)

class LoginView(View):
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
        params = request.POST
        if params.get('mobile'):
            mobile = params.get('mobile')
        else:
            self.response = {
                'res_str':'Please enter mobile number',
                'res_data':{}
            }
            return JsonResponse(self.response, status=400)
        if params.get('password'):
            hash_user_password = self.gen_password_hash(params.get('password'))
            try:
                user = User.objects.get(user_mobile=mobile)
            except User.DoesNotExists as ex:
                self.response = {
                    'res_str':'This mobile number is not registered',
                    'res_data':{}
                }
                return JsonResponse(self.response, status=400)
            hash_db_password = user.user_password
            if hash_user_password == hash_db_password:
                token = str(uuid.uuid4())
                user.token = token
                user.save()
                self.response = {
                    'res_str':'Login successful',
                    'res_data':{
                        'token': user.token
                    }
                }
                return JsonResponse(self.response, status=200)
            else:
                self.response = {
                    'res_str':'Password entered is incorrect',
                    'res_data':{}
                }
                return JsonResponse(self.response, status=400)
        else:
            self.response = {
                'res_str':'Please enter a password',
                'res_data':{}
            }
            return JsonResponse(self.response, status=400)