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
from TaskManagement.utils import *

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
        try:
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
            org = Organization.objects.get(name=params.get('name'))
            res_data_obj = {'org_id':org.id}
            self.response = {
                'res_str':'Organization registered successfully',
                'res_data': res_data_obj
            }
            return JsonResponse(self.response, status=200)
        except Organization.DoesNotExists as ex:
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
        # print params
        try:
            token = request.META.get('HTTP_REQUEST_TOKEN')
            mobile = request.META.get('HTTP_UID')
            access_bit = token_authentication(token,mobile)
            if access_bit == True:
                org_id = params.get('org_id')
                org = Organization.objects.get(pk=org_id)
                org.name = params.get('name')
                org.company_type = params.get('company_type')
                org.company_website = params.get('company_website')
                org.address_line_1 = params.get('address_line_1')
                org.address_line_2 = params.get('address_line_2')
                org.state = params.get('state')
                org.city = params.get('city')
                org.pin = params.get('pin')
                org.save()
                return JsonResponse(self.response, status=200)
            else:
                self.response = {
                    'res_str':'Permission denied',
                    'res_data':{}
                }
                return JsonResponse(self.response, status=403)
        except Organization.DoesNotExists as ex:
            self.response = {
                'res_str':'Incorrect post request',
                'res_data':{}
            }
            return JsonResponse(self.response, status=400)

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
            else:
                self.response = {
                    'res_str':'Permission denied',
                    'res_data':{}
                }
                return JsonResponse(self.response, status=403)
        except Exception:
            self.response = {
                'res_str':'Invalid',
                'res_data':{}
            }
            return JsonResponse(self.response, status=400)

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
        if params.get('first_user_bit'):
            try:
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
            except Organization.DoesNotExists as ex:
                self.response = {
                    'res_str':'Invalid request',
                    'res_data':{}
                }
                return JsonResponse(self.response, status=400)
        else:
            try:
                token = request.META.get('HTTP_REQUEST_TOKEN')
                mobile = request.META.get('HTTP_UID')
                access_bit = token_authentication(token,mobile)
                if access_bit == True:
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
                else:
                    self.response = {
                        'res_str':'Permission denied',
                        'res_data':{}
                    }
                    return JsonResponse(self.response, status=403)
            except Exception:
                self.response = {
                    'res_str':'Invalid request',
                    'res_data':{}
                }
                return JsonResponse(self.response, status=400)


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
        try:
            token = request.META.get('HTTP_REQUEST_TOKEN')
            mobile = request.META.get('HTTP_UID')
            access_bit = token_authentication(token,mobile)
            if access_bit == True:
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
            else:
                self.response = {
                    'res_str':'Permission denied',
                    'res_data':{}
                }
                return JsonResponse(self.response, status=403)
        except User.DoesNotExists as ex:
            self.response = {
                'res_str':'Invalid request',
                'res_data':{}
            }
            return JsonResponse(self.response, status=400)

    def get(self, request, *args, **kwargs):
        ''''''
    	params = request.GET
        try:
            token = request.META.get('HTTP_REQUEST_TOKEN')
            mobile = request.META.get('HTTP_UID')
            access_bit = token_authentication(token,mobile)
            if access_bit == True:
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
            else:
                self.response = {
                    'res_str':'Permission denied',
                    'res_data':{}
                }
                return JsonResponse(self.response, status=403)
        except User.DoesNotExists as ex:
            self.response = {
                'res_str':'Invalid request',
                'res_data':{}
            }
            return JsonResponse(self.response, status=400)

class OrgUsersView(View):
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
            data = list()
            if access_bit == True:
                org_id = params.get('org_id')
                org = Organization.objects.get(pk=org_id)
                users = User.objects.filter(organization=org)
                for user in users:
                    data.append({
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'user_mobile': user.user_mobile,
                            'user_mail': user.user_mail,
                            'user_designation':user.user_designation,
                            'user_type':user.user_type,
                            'user_id':user.id
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
        except Exception:
            self.response = {
                'res_str':'Invalid request',
                'res_data':{}
            }
            return JsonResponse(self.response, status=400)

class LoginView(View):
    ''''''
    def __init__(self):
        ''''''
        self.response = {
            'data': 'Done'
        }

    def dispatch(self, *args, **kwargs):
        return super(self.__class__, self).dispatch(*args, **kwargs)

    def gen_password_hash(self, passwd):
        return str(hashlib.sha256(passwd).hexdigest())

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
                        'token':user.token,
                        'uid':user.user_mobile
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

class LogoutView(View):
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
        try:
            token = request.META.get('HTTP_REQUEST_TOKEN')
            mobile = request.META.get('HTTP_UID')
            access_bit = token_authentication(token,mobile)
            if access_bit == True:
                user = User.objects.get(user_mobile=mobile)
                user.token = ''
                user.save()
                self.response = {
                    'res_str':'Logout suceess! See you soon',
                    'res_data':{}
                }
                return JsonResponse(self.response, status=200)
            else:
                self.response = {
                    'res_str':'Permission denied',
                    'res_data':{}
                }
                return JsonResponse(self.response, status=403)
        except Exception:
            self.response = {
                'res_str':'Invalid request',
                'res_data':{}
            }
            return JsonResponse(self.response, status=400)